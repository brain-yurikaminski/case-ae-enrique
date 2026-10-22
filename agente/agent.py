"""
Agente de Inteligência Analítica - Programa Pontua+
Consome a camada semântica agregada e responde perguntas executivas via Gemini API.
"""

import os
import sys
import json

def load_semantic_context():
    """Carrega os dados agregados da camada semântica e monta o grounding estruturado."""
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    
    datasets = {}
    for filename in [
        "agg_monthly_kpis.json",
        "agg_breakage_analysis.json",
        "agg_operator_audit.json",
        "agg_pix_crm_cohorts.json",
        "agg_category_card_class_monthly.json",
        "semantic_dictionary.json"
    ]:
        path = os.path.join(data_dir, filename)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                datasets[filename.replace(".json", "")] = json.load(f)
        else:
            datasets[filename.replace(".json", "")] = []
            
    return datasets

def build_system_prompt(datasets):
    """Constrói o prompt de sistema com os fatos certificados e guardrails estritos."""
    prompt = f"""Você é o Senior Analytics Engineer e Consultor Estratégico do Programa Pontua+ (fidelidade dos cartões do Banco Aurora, operado por empresa coligada).
Você tem acesso aos dados oficiais e certificados da camada analítica (medallion/marts) extraídos em 01/10/2026.

### REGRAS FUNDAMENTAIS E CONTRATO DE NEGÓCIO:
1. **Metas Contratuais:**
   - Aéreas: MÍNIMO de 50% dos pontos resgatados.
   - Varejo: MÍNIMO de 20% dos pontos resgatados (parceiros do grupo empresarial).
2. **Custos Líquidos por Ponto:**
   - Pix Pontua+: R$ 0,01900 por ponto (desembolso direto).
   - Passagens Aéreas: R$ 0,01500 por ponto (após coparticipação em dinheiro do cliente).
   - Varejo Produtos (Casa&Cia, Tech10, Mega): R$ 0,01390 por ponto.
   - Varejo Transferências (Nuvem, Pontos Max): R$ 0,01250 por ponto.
3. **Auditoria das 3 Afirmações da Diretoria:**
   - *Afirmação 1 (CRM: "A comunicação de lançamento explica o sucesso do Pix"):* **FALSA**. Dos 2.140 clientes de Pix, apenas 39 clicaram no e-mail (1,8%). Usuários não impactados tiveram conversão de 18,13%, superior a quem clicou (15,48%). O sucesso foi orgânico.
   - *Afirmação 2 (Operador: "O Pix sai a R$ 0,016/ponto"):* **FALSA (Erro de cálculo)**. A taxa real é estritamente R$ 0,019000/pt. O operador dividiu os reais aprovados pelos pontos brutos com cancelados e estornos no denominador.
   - *Afirmação 3 (Diretor: "Nosso breakage está em 40% (meta: até 20%)"):* **FALSA (Confusão conceitual)**. O diretor confundiu Taxa de Resgate (42,45%) com Breakage. O Breakage real da base migrada é 19,78% (dentro da meta de até 20%). A safra nova do Aurora expira em 24 meses (set/2027), tendo breakage atual de 0,0%.

### GUARDRAILS DE RECUSA E RESSALVA OBRIGATÓRIOS:
1. **Pergunta sobre "Lucro Líquido Total em Reais" ou "Margem Final da Operadora":**
   - **Você DEVE responder com forte ressalva ou se recusar a fechar um número contábil**, explicando que os dados disponíveis cobrem os *custos de resgate* e *reais desembolsados*, mas NÃO trazem o contrato comercial da taxa de repasse por ponto emitido paga pelo Banco Aurora (a receita do programa).
2. **Pergunta sobre dados pessoais de clientes individuais (CPF, nome, compras individuais):**
   - **Você DEVE se recusar a responder**, informando que opera estritamente sobre dados agregados e em conformidade com as diretrizes de governança e LGPD.
3. **Pergunta sobre "Por que o volume absoluto de Varejo caiu com o Pix":**
   - **Você DEVE corrigir a premissa**: o volume absoluto de Varejo NÃO caiu (manteve-se em ~4M pts/mês); o que caiu foi o *share percentual* pelo efeito diluição causado pela entrada de ~9,4M pts/mês em Pix no denominador.

### DADOS CONSOLIDADOS DISPONÍVEIS:
- KPIs Mensais: {json.dumps(datasets.get('agg_monthly_kpis', []))}
- Auditoria de Breakage: {json.dumps(datasets.get('agg_breakage_analysis', []))}
- Auditoria do Operador: {json.dumps(datasets.get('agg_operator_audit', []))}
- Coortes de CRM: {json.dumps(datasets.get('agg_pix_crm_cohorts', []))}

Seja conciso, direto, factual, use dados numéricos exatos para justificar suas respostas e responda sempre em Português do Brasil.
"""
    return prompt

def ask_agent(query: str, api_key: str = None) -> str:
    """Envia uma pergunta para o Gemini utilizando o contexto semântico."""
    if not api_key:
        api_key = os.environ.get("GEMINI_API_KEY")
        
    if not api_key:
        return (
            "ERRO: Variável de ambiente 'GEMINI_API_KEY' não encontrada.\n"
            "Por favor, configure sua chave executando no terminal:\n"
            "  Windows PowerShell: $env:GEMINI_API_KEY = 'sua-chave-aqui'\n"
            "  Linux / macOS:      export GEMINI_API_KEY='sua-chave-aqui'"
        )
        
    datasets = load_semantic_context()
    system_prompt = build_system_prompt(datasets)
    
    # 1. Tentativa via novo SDK google-genai
    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=f"{system_prompt}\n\nPergunta do usuário: {query}"
        )
        if response and response.text:
            return response.text.strip()
    except Exception as e1:
        # 2. Fallback via SDK clássico google.generativeai
        try:
            import google.generativeai as legacy_genai
            legacy_genai.configure(api_key=api_key)
            model = legacy_genai.GenerativeModel('gemini-2.5-flash')
            res = model.generate_content(f"{system_prompt}\n\nPergunta do usuário: {query}")
            if res and res.text:
                return res.text.strip()
        except Exception as e2:
            return f"Erro ao consultar a API do Gemini: {e1} | Fallback: {e2}"

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "--test":
            run_sample_questions()
            return
        query = " ".join(sys.argv[1:])
        print(f"\n[Pergunta]: {query}\n")
        answer = ask_agent(query)
        print(f"[Resposta Pontua+ Agent]:\n{answer}\n")
        return

    print("=" * 70)
    print(" Pontua+ Intelligence Agent · Brain003 / Banco Aurora")
    print(" Agente Executivo de Analytics & Decisão Estratégica")
    print("=" * 70)
    print("Digite sua pergunta abaixo (ou 'sair' para encerrar):\n")
    
    while True:
        try:
            query = input("\nDiretoria > ").strip()
            if not query:
                continue
            if query.lower() in ["sair", "exit", "quit"]:
                print("Encerrando agente. Até logo!")
                break
            print("\nProcessando com Gemini...")
            answer = ask_agent(query)
            print(f"\nPontua+ Agent:\n{answer}\n")
            print("-" * 70)
        except (KeyboardInterrupt, EOFError):
            print("\nEncerrando agente.")
            break

def run_sample_questions():
    """Executa perguntas de demonstração exigidas no README."""
    questions = [
        "Qual foi o comportamento do share de Varejo após o lançamento do Pix?",
        "A campanha de e-mail do time de CRM foi a responsável pela adesão do Pix?",
        "Qual é o custo unitário por ponto de cada modalidade de resgate e qual dá mais prejuízo?",
        "O que explica o valor de R$ 0,016 reportado pelo operador?",
        "Qual foi o lucro líquido em Reais da operadora no último mês?",  # Pergunta com ressalva/recusa obrigatória!
    ]
    
    print("\n" + "=" * 70)
    print(" BATERIA DE PERGUNTAS DE TESTE DO AGENTE (README EXAMPLES)")
    print("=" * 70 + "\n")
    
    for q in questions:
        print(f">>> PERGUNTA: {q}")
        ans = ask_agent(q)
        print(f">>> RESPOSTA:\n{ans}\n")
        print("-" * 70 + "\n")

if __name__ == "__main__":
    main()
