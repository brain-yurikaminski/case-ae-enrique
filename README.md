# Case Analytics Engineer · Brain003   
  
Exercício 1. Programa Pontua+

> Todos os dados, nomes e números deste case são fictícios e foram gerados para o processo seletivo.
> Versão dos dados: **v1**. O arquivo `MANIFESTO_v1.csv` lista os 9 CSVs com contagens de linhas e impressão digital (SHA-256).

## O contexto

O **Pontua+** é o programa de pontos dos cartões de crédito do Banco Aurora. Quem usa o cartão acumula pontos e troca por passagens aéreas, produtos de varejo ou transferências para programas parceiros. O programa é operado por uma empresa do grupo, que presta contas ao banco todo mês com um relatório (`relatorio_mensal_cliente.csv`).

Em **27/05/2026** o programa lançou o **Pontos no Pix**: o cliente troca pontos por dinheiro na conta, a R$ 0,019 por ponto. Cada 53 pontos equivael a aproximadamente R$1. O resgate nessa modalidade disparou.

O contrato com o banco tem duas metas sobre o total de pontos resgatados: trocas por passagens **aéreas devem ser pelo menos 50%** do volume de pontos trocados e **varejo pelo menos 20%**.   
  
Passagens aéreas custam mais caro ao programa do que o banco paga por ponto, sendo assim, mais desvantajoso para o programa (como empresa) e o varejo é onde o grupo tem parceiros próprios, (sendo mais vantajoso)

A diretoria vai decidir na semana que vem qual ação tomar para estimular ou coibir o resgate via Pix.  
  
Antes, quer entender o que aconteceu. E também se vale a pena estimular ou coibir o resgate tendo em vista as metas de aéreas e varejo e a própria saúde financeira do programa.  
Ela também ouviu duas afirmações e quer saber se são verdade:

- do time de CRM: "a comunicação de lançamento explica o sucesso do Pix";
- do relatório do operador: "Na verdade o Pix sai a cerca de R$ 0,016 por ponto, abaixo dos R$ 0,019 anunciados".
- De um diretor: “nosso breakage está em 40%! Nossa meta é não passar de 20%!"

## A descoberta faz parte do exercício

Não fornecemos um dicionário de dados. Explore os arquivos para identificar tipos, campos vazios, grãos, chaves, relacionamentos e regras relevantes para a análise. Documente esse entendimento no `README`, incluindo as evidências que sustentam suas escolhas.

Registre as hipóteses utilizadas e as perguntas que faria aos responsáveis pelos sistemas ou pelo negócio. Diferencie o que foi confirmado nos dados do que depende de validação adicional. Quando uma informação não puder ser estabelecida com os arquivos disponíveis, explique a limitação e o que precisaria para avançar. Hipóteses alternativas fundamentadas serão consideradas na avaliação.

## O que pedimos

Tempo de trabalho: **4 horas**. 

**O que pedimos**

1. O que aconteceu com os resgates depois do Pix e o que isso significa para as metas e para o programa.
2. Avalie as três afirmações.
3. Uma recomendação de uma página para a diretoria.
4. **Dashboard estratégico.** A diretoria vai acompanhar as principais métricas do programa por um dashboard. Monte o dashboard e a estrutura de dados por trás dele para responder às principais perguntas de negócio da diretoria. Os mesmos dados também serão consumidos por um agente de IA: desenhe uma estrutura que atenda aos dois (dashboard e agente) e justifique suas escolhas (camadas, grão, métricas, nomes, documentação, como o agente descobre o que cada campo significa).
5. **Opcional, se sobrar tempo:** desenvolva o agente que responde perguntas da diretoria sobre esses dados. Veja *Chave de LLM para o agente* abaixo.

**Regras da entrega**

- Os dados não vêm com dicionário. Entender os arquivos faz parte do exercício.
- Todos os números precisam sair de código executável (SQL e/ou Python, dbt opcional), com o grão de cada modelo declarado e **testes que garantam que os números estão certos.**
- No README, **separe o que foi confirmado nos dados do que é hipótese e liste o que você perguntaria ao negócio ou aos donos dos sistemas.**
- Tempo sugerido: 4 horas. Informe quanto tempo levou. Se não terminar, entregue o que rodou e diga como seguiria.
- Pode (DEVE) usar IA. Queremos ver como você usa e o que você confere.

## O que entregar

Quatro peças em formato zip ou em um git (cinco, se fizer o agente).

1. **Apresentação para a diretoria.** Mostra o que aconteceu, avalia as três afirmações e termina com a sua recomendação. Cada ponto da recomendação precisa trazer o número que o sustenta e dizer o que ainda falta saber. A apresentação será usada na devolutiva. Em HTML, partindo do modelo em `apresentacao-modelo/` (veja *Contrato de entrega*).
2. **Código e testes.** Todos os números da apresentação saem daqui, com SQL e/ou Python (dbt é opcional).
3. **README.** Precisa permitir que um avaliador reconstrua tudo a partir dos CSVs, sem editar nada à mão. Nele também ficam o que você entendeu dos dados, como modelou, as hipóteses que assumiu, o que perguntaria ao negócio ou aos donos dos sistemas e um registro breve do uso de IA (o que você pediu e o que conferiu ou corrigiu, subagentes e/ou skills que utilizou).
4. **Dashboard e estrutura de dados.** O dashboard (link acessível aos avaliadores, arquivo ou instruções para subir localmente), os modelos que o alimentam e a justificativa da estrutura para dashboard e agente. Ferramenta livre.
5. **Agente (opcional).** Código, instruções para rodar e exemplos de perguntas e respostas, incluindo pelo menos uma pergunta que ele deveria se recusar a responder ou responder com ressalva.

## Contrato de entrega (estrutura obrigatória)

Vamos abrir todas as entregas da mesma forma. Organize o repositório assim:

```
entrega/
  apresentacao/index.html   # deck HTML, autocontido (img/ e lib/ ao lado)
  dashboard/                # dashboard: build estático, arquivo ou app que sobe com o comando do README
agente/                     # opcional; um único ponto de entrada documentado no README
README.md
AI_LOG.md
```

- **Apresentação.** Copie `apresentacao-modelo/` para `entrega/apresentacao/` e edite os slides. O guia visual da Brain está em `apresentacao-modelo/design-v3.md` (cores, tipografia, componentes) e `apresentacao-modelo/SLIDES.md` (componentes e templates de slide). O modelo traz exemplos ilustrativos: substitua todo o conteúdo pelo do case. Abra direto no navegador; `?static` na URL desliga a animação e serve para exportar PDF. Se preferir outra ferramenta, entregue também um PDF em `entrega/apresentacao/`.
- **Dashboard.** Só dados agregados. Nada de dados linha a linha no build publicado.
- **Agente.** Lê `GEMINI_API_KEY` (e opcionalmente `GEMINI_MODEL`) de variável de ambiente. A chave nunca vai para o navegador.

## Chave de LLM para o agente

Você não precisa gastar dinheiro com o agente.

- Durante o desenvolvimento, use a chave e o provedor que preferir. Sugestão: a camada gratuita da API do Gemini, com chave criada em https://aistudio.google.com/apikey usando qualquer conta Google. Ela basta para o volume deste case. Outros provedores com cota gratuita ou um modelo local (Ollama ou similar) também servem.
- **Na avaliação, vamos publicar o seu projeto em produção (por exemplo, no Vercel) e rodar o agente com a nossa chave do Gemini.** Por isso:
  - o agente precisa funcionar com o Gemini, mesmo que você tenha desenvolvido com outro provedor;
  - a chave deve ser lida de variável de ambiente, e o nome dela deve estar documentado no README;
  - o README deve trazer um único comando ou passo a passo curto para subir o dashboard e o agente.
- Guarde a chave em `.env` (já está no `.gitignore`). **Nunca faça commit de chave.**

## Como enviar

Envie um arquivo `.zip` com a solução ou um link para um repositório acessível aos avaliadores (@brain-yurikaminski, @brain-leonardo-andrade)pelo mesmo canal em que recebeu o case. O prazo de entrega é o alinhado entre vc e o recrutador. Inclua as respostas, o código, os testes e o `README`. Se a execução depender dos CSVs fornecidos, documente onde colocá-los.

Registre as dúvidas e eventuais esclarecimentos recebidos no `README`.

## Como vamos avaliar

Vamos avaliar análise e engenharia com o mesmo peso. Importa a qualidade do raciocínio, das evidências e do julgamento, não a quantidade de coisas entregues. Escolhas diferentes de ferramenta, arquitetura ou interpretação são bem-vindas quando fundamentadas. Na devolutiva, você vai defender suas escolhas, inclusive as que fez com ajuda de IA.

## Os dados (`dados/`)

Nove arquivos CSV separados por vírgula, com cabeçalho e codificação UTF-8. Os valores monetários estão em reais (R$). Datas e horas mantêm os formatos dos sistemas de origem; identifique e documente como você as interpreta nas análises.


| Arquivo                        | Finalidade geral                                          | Colunas                                                                                                                                                                              |
| ------------------------------ | --------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `orders.csv`                   | Registros do sistema de pedidos                           | order_id, cart_id, user_id, created_at, status, status_updated_at                                                                                                                    |
| `order_items.csv`              | Produtos e valores associados aos pedidos                 | order_item_id, order_id, created_at, status, product_type, supplier_name, supplier_responsible, category_macro, paid_points, paid_currency, product_value, refunded_points, quantity |
| `carts.csv`                    | Carrinhos e canais de compra                              | cart_id, user_id, channel                                                                                                                                                            |
| `points_ledger.csv`            | Movimentações do saldo de pontos                          | movement_id, user_id, account_id, operation_code, points, movement_at, valid_until                                                                                                   |
| `dim_operation.csv`            | Cadastro de tipos de movimentação                         | operation_code, operation_name, direction                                                                                                                                            |
| `cards.csv`                    | Cadastros relacionados aos cartões                        | account_id, user_id, card_class, card_flag, created_at, is_most_recent                                                                                                               |
| `redeemed_points.csv`          | Registros de movimentação de pontos associados às compras | order_item_id, account_id, movement_type, points                                                                                                                                     |
| `crm_events.csv`               | Exportação da ferramenta de engajamento                   | event_ts, user_id, device_id, event_name, campaign_type, campaign_id, control_group, event_properties (JSON)                                                                         |
| `relatorio_mensal_cliente.csv` | Relatório do operador ao banco                            | mes, aereas_pct, varejo_pct, pix_pct, pix_reais, pix_pontos, pix_transacoes, emails_enviados, push_enviados                                                                          |


O que o time de dados sabe e te conta:

- O Pontua+ substituiu um programa anterior; os saldos antigos foram migrados para o sistema novo.
- Os níveis de cartão, do mais simples ao mais alto: Essencial, Gold, Platinum, Platinum Elo, Infinite, Black.
- A ferramenta de CRM e o sistema de pedidos são sistemas diferentes e não compartilham configuração.
- Os dados foram extraídos em 01/10/2026.


## Registro do processo (obrigatório)

**Commits e pushes.** Trabalhe na branch `entrega` e faça push ao fim de cada sessão de trabalho. O GitHub registra a hora de cada push no servidor. Ao terminar, abra um Pull Request de `entrega` para `main`: a abertura do PR marca a entrega.

**Uso de IA em `AI_LOG.md`.**
- Se usar um agente que lê `AGENTS.md` ou `CLAUDE.md` (Claude Code, Cursor, Codex, Copilot e similares), ele registra cada sessão automaticamente. Confira o que foi escrito.
- Se usar IA em chat (ChatGPT, Claude.ai, Gemini etc.), ao fim de cada conversa cole o prompt abaixo e acrescente a resposta ao final de `AI_LOG.md`:

```
Resuma esta conversa para um registro de uso de IA, em português, neste formato:
### <data e hora> · <ferramenta e modelo>
- **Pedido:** o que eu pedi, em 1 a 3 linhas.
- **O que a IA fez ou sugeriu:** resumo factual.
- **O que eu conferi, corrigi ou rejeitei:** inclusive erros seus que eu apontei.
- **Arquivos criados ou alterados:** caminhos, se houver.
Seja factual. Não invente nada que não esteja na conversa.
```

Links de compartilhamento ou exportações das conversas (por exemplo, `/export` no Claude Code) são bem-vindos em `ai-log/`.

---

# Documentação da Solução · Case Analytics Engineer

Este documento detalha a solução completa de engenharia de dados, modelagem dimensional, testes automatizados, dashboard executivo e agente de IA desenvolvidos para responder às perguntas estratégicas da diretoria sobre o Programa Pontua+.

---

## 1. Guia Rápido de Execução (Single-Command Setup)

### Pré-requisitos
- Python 3.10+ instalado (`py` ou `python`).
- Variável de ambiente `GEMINI_API_KEY` configurada com sua chave da Google Gemini API (para o agente).

```bash
# Configuração da chave de API no terminal:
# No Windows PowerShell:
$env:GEMINI_API_KEY="sua-chave-aqui"

# No Linux / macOS:
export GEMINI_API_KEY="sua-chave-aqui"
```

### Passo a Passo de Ponta a Ponta

1. **Instalar Dependências:**
   ```bash
   py -m pip install -r requirements.txt
   ```
   *(Dependências utilizadas: `duckdb`, `pytest`, `pandas`, `google-genai`)*

2. **Reconstruir Pipeline e Camadas Analíticas a partir dos CSVs brutos (`dados/`):**
   ```bash
   py pipeline/build_pipeline.py
   ```
   *Lê os 9 arquivos CSV em `dados/`, processa as camadas Staging, Marts e Agregadas, e exporta os datasets prontos em `entrega/dashboard/data/` e `agente/data/`.*

3. **Executar a Suíte de Testes Automatizados:**
   ```bash
   py -m pytest -v tests/test_pipeline.py
   ```
   *Executa os 13 testes de integridade referencial, unicidade de grão, reconciliação contábil do ledger e auditoria das 3 afirmações.*

4. **Subir Dashboard e Agente com um Único Comando:**
   ```bash
   py server.py
   ```
   *Inicia o servidor unificado em `http://localhost:8000`:*
   - **Dashboard Estratégico Interativo:** `http://localhost:8000` (com widget flutuante de chat com IA integrado!)
   - **Apresentação Executiva (Deck HTML):** `http://localhost:8000/apresentacao`
   - **Endpoint da API do Agente:** `POST http://localhost:8000/api/chat`

5. **Executar o Agente de IA via Terminal (CLI):**
   ```bash
   # Modo interativo (chat no terminal):
   py agente/agent.py

   # Pergunta direta via linha de comando:
   py agente/agent.py "Qual foi o share de varejo em agosto de 2026?"

   # Executar a bateria de perguntas de teste exigidas no case:
   py agente/agent.py --test
   ```

---

## 2. Justificativa da Estrutura de Dados (Dashboard e Agente)

Para atender simultaneamente ao **Dashboard Executivo** (que exige performance instantânea e cumpre a restrição de **apenas dados agregados**) e ao **Agente de IA** (que exige consistência semântica e imunidade a alucinações), adotamos uma arquitetura em camadas estruturada em DuckDB:

```
[dados/*.csv] (Camada Bruta / Raw)
      │
      ▼
[Staging Views] (Tipagem estrita, limpeza, extração de JSON do CRM)
      │
      ▼
[Marts Dimensionais] (dim_users, fct_order_items, fct_points_movements)
      │
      ▼
[Semantic / Serving Layer] (Tabelas Agregadas e Métricas de Negócio)
      ├──> entrega/dashboard/data/*.json & *.csv (Alimenta Dashboard SPA)
      └──> agente/data/*.json + semantic_dictionary.json (Alimenta Agente Gemini)
```

### Por que esta estrutura atende aos dois objetivos?
1. **Para o Dashboard:**
   - **Privacidade e Governança:** O build estático publicado do dashboard consome exclusivamente arquivos JSON/CSV pré-agregados, garantindo que nenhum dado nominal ou transacional de clientes trafegue na visualização.
   - **Performance Instantânea:** Todos os cálculos complexos de shares contratuais, custos ponderados e agregações temporais são resolvidos em tempo de build, eliminando gargalos de processamento no navegador.
2. **Para o Agente de IA (Gemini):**
   - **Context Grounding Preciso:** Em vez de expor 146 mil linhas cruas do ledger (que estourariam o contexto ou gerariam alucinações de soma), o agente recebe tabelas de grão consolidado (`agg_monthly_kpis`, `agg_breakage_analysis`, `agg_operator_audit`, `agg_pix_crm_cohorts`).
   - **Dicionário Semântico (`semantic_dictionary.json`):** Cada coluna tem seu tipo, grão e definição de negócio declarados, permitindo que a LLM compreenda exatamente o significado de conceitos como "taxa de resgate", "breakage" e "efeito diluição".
   - **Resolução de Anomalia de Dados na Engenharia:** A tabela `orders.csv` possui a coluna `user_id` 100% nula. O pipeline resolveu essa anomalia via junção relacional 1:1 com `carts.csv`, garantindo que o agente e o dashboard tenham dados de clientes íntegros sem intervenção manual.

---

## 3. Fatos Confirmados nos Dados

Todos os números abaixo foram calculados e validados por código executável e testados na suíte `tests/test_pipeline.py`:

1. **Explosão no Volume de Resgates pós-Pix:**
   - No pré-Pix (fev a abr/2026), a média de resgates era de **15,5M a 19M de pontos/mês**.
   - Com o lançamento em 27/05/2026, o volume saltou para **30,4M em junho (+103%)** e atingiu **33,5M em setembro/2026**.
   - O Pix se estabilizou em cerca de **9,4M de pontos/mês** (~28% a 30% do total resgatado no programa).

2. **Violação da Meta Contratual de Varejo ($\ge 20\%$):**
   - O share de Varejo despencou de **20,3% (maio/2026)** para **13,3% (junho)**, **12,8% (julho)**, **12,1% (agosto)** e **13,0% (setembro)**.
   - **Diagnóstico Técnico (Efeito Diluição):** O volume absoluto em Varejo permaneceu praticamente estável (2,88M em jan; 3,63M em abr; 4,37M em mai; 4,04M em jun; 4,34M em set). A quebra da meta decorre exclusivamente da expansão de +55% no denominador causada pela entrada do Pix.

3. **Pressão na Meta Contratual de Aéreas ($\ge 50\%$):**
   - O share de passagens aéreas caiu de **80,7% (abril)** para **56,3% (junho)** e fechou setembro em **59,0%**, reduzindo perigosamente a margem de segurança contratual para menos de 10 p.p.

4. **Auditoria da Afirmação 1 (CRM: *"A comunicação de lançamento explica o sucesso do Pix"*): FALSA**
   - O Pix foi lançado em **27/05/2026**. O e-mail de lançamento só foi enviado em **28/05 às 13:00**. Clientes já resgatavam Pix antes do disparo.
   - Dos 2.140 clientes únicos que fizeram Pix aprovado, **apenas 39 clientes (1,8%)** clicaram no e-mail de lançamento.
   - **435 clientes (20,3%)** que resgataram Pix sequer foram cadastrados ou impactados pela campanha.
   - **Taxa de conversão:** Clicou no e-mail (**15,48%**) vs Não impactado pela campanha (**18,13%**). O sucesso foi tração 100% orgânica decorrente da atratividade do dinheiro em conta.

5. **Auditoria da Afirmação 2 (Operador: *"O Pix sai a cerca de R$ 0,016 por ponto"*): FALSA (Erro de Cálculo)**
   - Em todas as 2.808 transações de Pix aprovadas em `order_items.csv`, a taxa cobrada foi rigorosamente de **R$ 0,019000 por ponto** (R$ 721.610,73 desembolsados para 37.979.434 pontos).
   - **Origem do erro do operador:** No `relatorio_mensal_cliente.csv`, o operador incluiu pedidos cancelados, estornados e inválidos no total de pontos (denominador de 10,7M), mas dividiu apenas pelos Reais aprovados (R$ 174.261), derrubando a razão matemática artificialmente para R$ 0,01627.

6. **Auditoria da Afirmação 3 (Diretor: *"Nosso breakage está em 40%! Meta: até 20%"*): FALSA (Confusão Conceitual)**
   - O diretor confundiu **Taxa de Resgate (Redemption Rate)** com **Breakage**.
   - No ledger, o total de pontos resgatados sobre o total de créditos emitidos ($323,4\text{M} \div 761,8\text{M}$) é exatamente **42,45%**.
   - O **Breakage real** da base migrada (pontos expirados na op 103 sobre o total migrado na op 100) é de **19,78%** ($64.090.805 \div 324.024.198$), rigorosamente dentro da meta de até 20%.
   - Os pontos emitidos no programa novo (op 1) têm validade de 24 meses (`valid_until` entre set/2027 e set/2028), tendo breakage atual de **0,0%**.

7. **Estrutura de Custos Unitários Líquidos:**
   - **Varejo Transferências (Nuvem, Pontos Max):** R$ 0,01250 por ponto.
   - **Varejo Produtos (Casa&Cia, Tech10, Mega):** R$ 0,01390 por ponto (parceiros próprios do grupo).
   - **Passagens Aéreas:** R$ 0,01500 por ponto (custo líquido após coparticipação em dinheiro do cliente).
   - **Pix Pontua+:** R$ 0,01900 por ponto.
   - *Conclusão Financeira:* O Pix é **26,7% mais caro** que Aéreas e **52,0% mais caro** que Varejo parceiro. Como passagens aéreas já custam mais caro do que o banco repassa por ponto, o Pix opera em severo prejuízo operacional (drenou R$ 721.610 em caixa em 4 meses).

---

## 4. Hipóteses Adotadas

1. **Precedência de Cartão do Usuário:** Para usuários que possuem múltiplos cartões em `cards.csv`, assumiu-se como classificação primária do cliente o cartão com `is_most_recent = TRUE` e data de criação mais recente.
2. **Reconciliação FIFO de Saldo:** Como os saldos de pontos são fungíveis na carteira do cliente, assumiu-se que os resgates consom prioritariamente os pontos mais antigos (da migração), o que é compatível com a expiração observada na base legada.
3. **Custo do Repasse do Banco Aurora:** Como o contrato de repasse por ponto acumulado no cartão não foi fornecido na base, assumiu-se a premissa de negócio descrita no briefing de que *passagens aéreas (R$ 0,0150/pt) custam mais caro do que o banco repassa*, implicando que o repasse do banco é inferior a R$ 0,0150 por ponto.

---

## 5. Perguntas para as Áreas de Negócio e Sistemas

### Para o Banco Aurora & Área Comercial:
1. **Fórmula de Repasse Comercial:** Qual é o valor exato em Reais repassado pelo Banco Aurora à operadora por ponto emitido no cartão de crédito?
2. **Penalidades Contratuais:** O não cumprimento da meta de 20% em Varejo sujeita a operadora a multas contratuais, renegociação compulsória de margem ou perda de exclusividade?
3. **Impacto no Negócio Bancário:** O Pix gerou aumento no volume de compras (spend) ou reduziu o cancelamento (churn) de cartões de alta renda do Banco Aurora?

### Para os Donos dos Sistemas & Engenharia:
1. **Anomalia na Tabela de Pedidos:** Por que o campo `orders.user_id` está 100% nulo em produção, obrigando a resolução via `carts`? Existe plano de correção ou migração de schema?
2. **Rotina de Fechamento do Operador:** Como o script que gera o `relatorio_mensal_cliente.csv` é executado? Por que ele não filtra pedidos cancelados/estornados antes de agregar os pontos?
3. **Regra de Expiração da Safra Nova:** Qual será a política de comunicação e tolerância para os pontos do programa novo quando começarem a vencer em setembro de 2027?

---

## 6. Documentação do Agente de IA (`agente/`)

O agente de IA está localizado em `agente/agent.py` e se conecta à API oficial do Google Gemini utilizando a chave configurada na variável `GEMINI_API_KEY`.

### Perguntas que o Agente Responde com Precisão:
1. *"Qual foi o comportamento do share de Varejo após o lançamento do Pix?"* -> Apresenta a queda de 20% para 13% e explica detalhadamente o efeito diluição em relação ao volume absoluto estável.
2. *"A campanha de e-mail do time de CRM foi a responsável pela adesão do Pix?"* -> Refuta a tese com a conversão de 15,48% em quem clicou vs 18,13% em não impactados.
3. *"Qual é o custo unitário por ponto de cada modalidade de resgate e qual dá mais prejuízo?"* -> Apresenta a tabela comparativa (R$ 0,0125 a R$ 0,0190) e aponta o Pix como maior drenador de margem.
4. *"O que explica o valor de R$ 0,016 reportado pelo operador?"* -> Explica a falha contábil de incluir cancelados no denominador.

### Pergunta com Recusa / Ressalva Obrigatória:
- **Pergunta:** *"Qual foi o lucro líquido em Reais da operadora no último mês?"*
- **Comportamento do Agente:** O agente **se recusa a fornecer um número fechado de lucro líquido** e emite uma ressalva formal:
  > *"Não é possível calcular o Lucro Líquido da operadora com os dados disponíveis. Os dados cobrem detalhadamente os custos de resgate e valores desembolsados, mas não trazem o contrato comercial da taxa de repasse por ponto emitido paga pelo Banco Aurora (a receita do programa). Qualquer estimativa sem esse dado seria alucinação."*

