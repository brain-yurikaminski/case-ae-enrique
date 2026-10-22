# Registro de uso de IA

Uma entrada por sessão ou etapa de validação, da mais antiga para a mais recente. Formato e regras definidos em `AGENTS.md`.

---

### 2026-10-21T19:30:00-03:00 · Gemini CLI · Gemini 2.5 Pro
- **Pedido:** *"leia o readme para que você abstraia as regras do desafio"* (leitura e síntese de regras de negócio, metas e entregáveis).
- **O que a IA fez ou sugeriu:**
  - Leu na íntegra `README.md`, `AGENTS.md` e `CLAUDE.md`.
  - Estruturou e apresentou as regras centrais do case: contrato de entrega (branch `entrega`, pastas obrigatórias), metas contratuais do programa Pontua+ (Aéreas $\ge 50\%$, Varejo $\ge 20\%$), a assimetria de custo entre passagens e varejo parceiro, as 3 afirmações da diretoria a serem auditadas e a proibição de dados linha a linha no build do dashboard.
- **O que o candidato conferiu, corrigiu ou rejeitou:**
  - O candidato validou a síntese das regras e autorizou o avanço para a exploração empírica dos dados.
- **Arquivos criados ou alterados:** Nenhum arquivo alterado (apenas leitura e planejamento de escopo).

---

### 2026-10-21T19:45:00-03:00 · Gemini CLI · Gemini 2.5 Pro
- **Pedido:** *"vamos iniciar a exploração dos arquivos CSV"* (investigação estrutural, volumetria, esquemas e auditoria das 3 hipóteses).
- **O que a IA fez ou sugeriu:**
  - Criou e alternou para a branch `entrega` (`git checkout -b entrega`).
  - Instalou e configurou o DuckDB para consultas SQL analíticas diretas sobre os 9 CSVs de `dados/`.
  - Desenvolveu scripts de perfilamento (`scripts/profile_data.py` e `scripts/explore_orders.py`), validando a integridade dos hashes SHA-256 contra o `MANIFESTO_v1.csv`.
  - Descobriu a anomalia estrutural da tabela `orders.csv`: a coluna `orders.user_id` é 100% nula (todos os 19.785 registros); identificou que a resolução relacional exata se dá via junção 1:1 com `carts.csv` pelo `cart_id`.
  - **Auditoria das 3 Afirmações da Diretoria:**
    1. *Afirmação 1 (CRM: "A comunicação explica o sucesso do Pix"):* Refutada com dados de coorte. Apenas 1,8% dos usuários de Pix clicaram no e-mail de lançamento (39 de 2.140). A conversão de quem não recebeu a campanha (18,13%) foi superior à de quem clicou (15,48%), evidenciando tração puramente orgânica.
    2. *Afirmação 2 (Operador: "O Pix sai a R$ 0,016 por ponto"):* Descoberto erro metodológico no relatório do operador. Em todos os 2.808 pedidos de Pix aprovados a taxa foi estritamente R$ 0,019000/pt. O operador dividiu os Reais aprovados pelos pontos brutos de todos os status (incluindo cancelados e estornados no denominador).
    3. *Afirmação 3 (Diretor: "Breakage está em 40%"):* Identificada confusão conceitual do diretor entre Taxa de Resgate (42,45% no ledger) e Breakage. O Breakage real da base migrada foi de 19,78% (dentro do teto de 20%), e os créditos novos têm validade de 24 meses (breakage atual de 0,0%).
- **O que o candidato conferiu, corrigiu ou rejeitou:**
  - O candidato analisou os resultados estatísticos e os vereditos das 3 afirmações, aprovando a lógica de negócio e determinando o avanço para a modelagem.
- **Arquivos criados ou alterados:** `scripts/profile_data.py`, `scripts/explore_orders.py`.

---

### 2026-10-21T20:05:00-03:00 · Gemini CLI · Gemini 2.5 Pro
- **Pedido:** *"vamos avançar para a estrutura de modelagem e pipeline"* (construção das camadas analíticas e validação automatizada com testes).
- **O que a IA fez ou sugeriu:**
  - Construiu o pipeline completo em Python/DuckDB (`pipeline/build_pipeline.py`) implementando a arquitetura em camadas:
    - *Staging:* Limpeza, tipagem estrita e extração de propriedades JSON de CRM.
    - *Marts:* `dim_users` (visão 360º com coortes e saldo), `fct_order_items` (com custo líquido por ponto e marcação de Pix) e `fct_points_movements`.
    - *Semantic Layer / Agregadas:* `agg_monthly_kpis`, `agg_breakage_analysis`, `agg_operator_audit`, `agg_pix_crm_cohorts`, `agg_category_card_class_monthly`.
  - Exportou as tabelas agregadas em JSON e CSV para `entrega/dashboard/data/` e `agente/data/`, gerando o dicionário semântico `semantic_dictionary.json`.
  - Instalou o `pytest` e implementou a suíte de testes em `tests/test_pipeline.py` (13 testes automatizados).
  - *Diagnóstico e Correção Contábil:* Na primeira execução do teste de resgates, foi detectada uma diferença de 3.141.827 pontos entre o ledger bruto e os itens aprovados. A IA investigou a fundo e comprovou que esses 3.141.827 pontos correspondiam exatamente a pedidos cancelados após o checkout (`ESTORNADO`), os quais, somados a 254.384 pontos de reembolsos parciais em pedidos aprovados, batiam com 100,000% de exatidão na Operação 14 do ledger (`ESTORNO_PEDIDO`: 3.396.211 pontos). O teste foi enriquecido para validar essa reconciliação completa.
- **O que o candidato conferiu, corrigiu ou rejeitou:**
  - O candidato acompanhou a execução da suíte de testes no pytest (13/13 aprovados) e aprovou o grão e a consistência das camadas analíticas.
- **Arquivos criados ou alterados:** `pipeline/build_pipeline.py`, `tests/test_pipeline.py`, `entrega/dashboard/data/` (5 arquivos JSON/CSV), `agente/data/` (5 arquivos JSON/CSV + semantic_dictionary.json).

---

### 2026-10-21T20:20:00-03:00 · Gemini CLI · Gemini 2.5 Pro
- **Pedido:** *"avançar para a construção do Dashboard Estratégico"* (desenvolvimento da interface executiva alinhada às regras do case e ao design system).
- **O que a IA fez ou sugeriu:**
  - Baixou localmente a biblioteca Chart.js (`entrega/dashboard/lib/chart.umd.min.js`) para garantir que o dashboard funcione 100% offline e sem dependências externas.
  - Desenvolveu o gerador `pipeline/generate_dashboard_html.py` e compilou o dashboard executivo `entrega/dashboard/index.html`.
  - Alinhou rigorosamente ao design system **Brain003** (`design-v3.md`: estética dark-first, cores `#1E2BFF`, `#00CFFF`, `#3DFF6E`, `#FF4D6D`, tipografia `Roboto Mono` + `Inter`).
  - Estruturou 5 módulos interativos: Visão Estratégica & Metas, Auditoria das 3 Afirmações, Economia Unitária & Custos, Segmentação por Cartão/Canal e Tabela Auditável de KPIs.
  - Garantia de governança: o dashboard opera exclusivamente sobre dados pré-calculados e agregados, sem trafegar dados linha a linha no build.
- **O que o candidato conferiu, corrigiu ou rejeitou:**
  - O candidato validou a estrutura de métricas, o diagnóstico do efeito diluição em Varejo e solicitou o avanço para a apresentação executiva.
- **Arquivos criados ou alterados:** `entrega/dashboard/lib/chart.umd.min.js`, `pipeline/generate_dashboard_html.py`, `entrega/dashboard/index.html`.

---

### 2026-10-21T20:30:00-03:00 · Gemini CLI · Gemini 2.5 Pro
- **Pedido:** *"avançar para o Deck de Apresentação Executiva"* (construção dos slides para a reunião de diretoria a partir do modelo Brain003).
- **O que a IA fez ou sugeriu:**
  - Copiou os assets oficiais (`img/` e `lib/`) de `apresentacao-modelo/` para `entrega/apresentacao/`.
  - Construiu `entrega/apresentacao/index.html` contendo 14 slides interativos no canvas 1920×1080 com suporte a GSAP/Anime.js, navegação por teclado, modo tela cheia (`F`) e parâmetro `?static`.
  - Estruturou a narrativa executiva: diagnóstico do Pix (+103% de volume), efeito diluição no Varejo (volume estável em ~4M pts/mês vs denominador inflado), auditoria das 3 afirmações com evidências empíricas, unit economics por categoria (Pix custando R$ 0,0190 vs Varejo parceiro a R$ 0,0125) e recomendação de 1 página (reestruturar/coibir o Pix por meio de 4 alavancas quantificadas).
  - Gerou automaticamente a versão em PDF (`entrega/apresentacao/apresentacao_pontua_plus.pdf`) via Microsoft Edge headless para impressão ou leitura executiva.
- **O que o candidato conferiu, corrigiu ou rejeitou:**
  - O candidato validou a qualidade visual dos slides e o embasamento numérico da recomendação estratégica.
- **Arquivos criados ou alterados:** `entrega/apresentacao/index.html`, `entrega/apresentacao/apresentacao_pontua_plus.pdf`, `entrega/apresentacao/img/`, `entrega/apresentacao/lib/`.

---

### 2026-10-21T20:40:00-03:00 · Gemini CLI · Gemini 2.5 Pro
- **Pedido:** *"segue nossa chave de api do gemini [CHAVE_FORNECIDA]"* (integração do modelo de IA para consultas da diretoria e unificação de execução).
- **O que a IA fez ou sugeriu:**
  - Protegeu rigorosamente a chave contra commits em arquivos versionados, mantendo-a lida via variável de ambiente `GEMINI_API_KEY`.
  - Instalou o SDK oficial `google-genai` e desenvolveu `agente/agent.py`.
  - Diagnosticou que a API Gemini v1beta havia descontinuado o alias `gemini-1.5-flash` para a chave fornecida e configurou automaticamente o `gemini-2.5-flash` com fallback resiliente para `google.generativeai`.
  - Implementou o grounding semântico a partir dos dados agregados e configurou guardrails estritos: o agente se recusa formalmente a fornecer estimativas de "lucro líquido em Reais" pela ausência do valor do contrato de repasse do Banco Aurora.
  - Executou a bateria de testes automatizados do agente (`py agente/agent.py --test`), validando respostas exatas e o disparo correto do guardrail de recusa.
  - Criou o servidor unificado `server.py` que sobe o Dashboard, a Apresentação e o endpoint `/api/chat` com um único comando (`py server.py`).
  - Adicionou um widget flutuante de chat com IA diretamente dentro do dashboard web.
  - Documentou a entrega de ponta a ponta no `README.md` e gerou o `requirements.txt`.
- **O que o candidato conferiu, corrigiu ou rejeitou:**
  - O candidato validou o funcionamento do agente com a chave do Gemini e solicitou o enriquecimento minucioso deste `AI_LOG.md` registrando as solicitações e validações de cada etapa.
- **Arquivos criados ou alterados:** `agente/agent.py`, `server.py`, `pipeline/generate_dashboard_html.py`, `entrega/dashboard/index.html`, `requirements.txt`, `README.md`, `.gitignore`, `AI_LOG.md`.
