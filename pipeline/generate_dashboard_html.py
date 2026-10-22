"""
Gerador do Dashboard Estratégico Pontua+ (HTML5 SPA)
Incorpora dados agregados, Chart.js local e design system Brain003 (dark-first, elétrico, executivo).
"""

import json
import os

def build_dashboard():
    print("Compilando dashboard executivo...")
    
    with open("entrega/dashboard/data/agg_monthly_kpis.json", encoding="utf-8") as f:
        monthly_kpis = json.load(f)
        
    with open("entrega/dashboard/data/agg_breakage_analysis.json", encoding="utf-8") as f:
        breakage_data = json.load(f)
        
    with open("entrega/dashboard/data/agg_operator_audit.json", encoding="utf-8") as f:
        operator_audit = json.load(f)
        
    with open("entrega/dashboard/data/agg_pix_crm_cohorts.json", encoding="utf-8") as f:
        crm_cohorts = json.load(f)
        
    with open("entrega/dashboard/data/agg_category_card_class_monthly.json", encoding="utf-8") as f:
        category_card_data = json.load(f)

    html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Pontua+ | Dashboard Estratégico da Diretoria</title>
  <script src="lib/chart.umd.min.js"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Roboto+Mono:wght@400;500;700&display=swap" rel="stylesheet">
  <style>
    :root {{
      --primary: #1E2BFF;
      --primary-light: #4D5AFF;
      --accent-data: #00CFFF;
      --accent-synapse: #3DFF6E;
      --warning: #FFB300;
      --error: #FF4D6D;
      --bg-deep: #060A1C;
      --bg-surface: #0E142F;
      --bg-card: #141C3E;
      --bg-hover: #1C2754;
      --border-color: #212C5B;
      --text-hi: #EAF0FF;
      --text-mid: #A9B4D0;
      --text-low: #6B7699;
      --font-mono: 'Roboto Mono', monospace;
      --font-body: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    body {{
      background-color: var(--bg-deep);
      color: var(--text-hi);
      font-family: var(--font-body);
      font-size: 14px;
      line-height: 1.5;
      padding-bottom: 60px;
      overflow-x: hidden;
    }}

    /* HEADER */
    header {{
      background: rgba(14, 20, 47, 0.85);
      backdrop-filter: blur(12px);
      border-bottom: 1px solid var(--border-color);
      padding: 16px 32px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      position: sticky;
      top: 0;
      z-index: 100;
    }}

    .brand {{
      display: flex;
      align-items: center;
      gap: 16px;
    }}

    .brand-badge {{
      background: var(--primary);
      color: #fff;
      font-family: var(--font-mono);
      font-weight: 700;
      font-size: 12px;
      letter-spacing: 0.1em;
      padding: 4px 8px;
    }}

    .brand-title {{
      font-family: var(--font-mono);
      font-weight: 700;
      font-size: 18px;
      letter-spacing: -0.02em;
      color: var(--text-hi);
    }}

    .brand-subtitle {{
      font-size: 12px;
      color: var(--text-mid);
    }}

    .header-actions {{
      display: flex;
      align-items: center;
      gap: 16px;
    }}

    .status-pill {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 6px 12px;
      font-family: var(--font-mono);
      font-size: 12px;
      background: rgba(255, 77, 109, 0.12);
      border: 1px solid var(--error);
      color: var(--error);
    }}

    .status-dot {{
      width: 8px;
      height: 8px;
      background: var(--error);
      border-radius: 50%;
      animation: pulse 2s infinite;
    }}

    @keyframes pulse {{
      0% {{ opacity: 1; transform: scale(1); }}
      50% {{ opacity: 0.4; transform: scale(0.85); }}
      100% {{ opacity: 1; transform: scale(1); }}
    }}

    /* CONTAINER */
    .container {{
      max-width: 1440px;
      margin: 0 auto;
      padding: 24px 32px;
    }}

    /* NAV TABS */
    .nav-tabs {{
      display: flex;
      gap: 8px;
      border-bottom: 1px solid var(--border-color);
      margin-bottom: 24px;
      padding-bottom: 8px;
      overflow-x: auto;
    }}

    .tab-btn {{
      background: transparent;
      border: 1px solid transparent;
      color: var(--text-mid);
      font-family: var(--font-mono);
      font-size: 13px;
      font-weight: 500;
      padding: 8px 16px;
      cursor: pointer;
      transition: all 0.2s;
    }}

    .tab-btn:hover {{
      color: var(--text-hi);
      background: var(--bg-surface);
    }}

    .tab-btn.active {{
      background: var(--bg-card);
      border: 1px solid var(--accent-data);
      color: var(--accent-data);
    }}

    /* SCORECARDS */
    .kpi-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 16px;
      margin-bottom: 24px;
    }}

    .kpi-card {{
      background: var(--bg-surface);
      border: 1px solid var(--border-color);
      padding: 20px;
      position: relative;
      transition: border-color 0.2s, transform 0.2s;
    }}

    .kpi-card:hover {{
      border-color: var(--primary-light);
      transform: translateY(-2px);
    }}

    .kpi-overline {{
      font-family: var(--font-mono);
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.12em;
      color: var(--text-low);
      margin-bottom: 6px;
    }}

    .kpi-value {{
      font-family: var(--font-mono);
      font-size: 28px;
      font-weight: 700;
      color: var(--text-hi);
      margin-bottom: 4px;
    }}

    .kpi-subtext {{
      font-size: 12px;
      color: var(--text-mid);
      display: flex;
      align-items: center;
      gap: 6px;
    }}

    .badge-ok {{
      color: var(--accent-synapse);
      font-family: var(--font-mono);
      font-weight: 600;
    }}

    .badge-bad {{
      color: var(--error);
      font-family: var(--font-mono);
      font-weight: 600;
    }}

    .badge-warn {{
      color: var(--warning);
      font-family: var(--font-mono);
      font-weight: 600;
    }}

    /* GRID LAYOUTS */
    .dashboard-grid {{
      display: grid;
      grid-template-columns: 2fr 1fr;
      gap: 20px;
      margin-bottom: 24px;
    }}

    .grid-2col {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 20px;
      margin-bottom: 24px;
    }}

    .grid-3col {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
      gap: 20px;
      margin-bottom: 24px;
    }}

    /* CARDS */
    .card {{
      background: var(--bg-surface);
      border: 1px solid var(--border-color);
      padding: 24px;
      position: relative;
    }}

    .card-header {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 20px;
      border-bottom: 1px solid var(--border-color);
      padding-bottom: 12px;
    }}

    .card-title {{
      font-family: var(--font-mono);
      font-size: 16px;
      font-weight: 700;
      color: var(--text-hi);
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .card-desc {{
      font-size: 13px;
      color: var(--text-mid);
      margin-top: 4px;
    }}

    .chart-container {{
      position: relative;
      height: 320px;
      width: 100%;
    }}

    /* TABLES */
    .table-container {{
      overflow-x: auto;
      max-height: 480px;
      border: 1px solid var(--border-color);
    }}

    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 13px;
      text-align: left;
    }}

    th {{
      background: var(--bg-card);
      color: var(--text-hi);
      font-family: var(--font-mono);
      font-size: 11px;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      padding: 12px 16px;
      position: sticky;
      top: 0;
      border-bottom: 1px solid var(--border-color);
      white-space: nowrap;
    }}

    td {{
      padding: 12px 16px;
      border-bottom: 1px solid rgba(33, 44, 91, 0.4);
      color: var(--text-mid);
      white-space: nowrap;
    }}

    tr:hover td {{
      background: rgba(30, 43, 255, 0.05);
      color: var(--text-hi);
    }}

    .mono {{
      font-family: var(--font-mono);
    }}

    /* AUDIT CALLOUT BOXES */
    .audit-box {{
      padding: 18px;
      border-left: 4px solid var(--primary);
      background: var(--bg-card);
      margin-bottom: 16px;
    }}

    .audit-box.danger {{
      border-left-color: var(--error);
      background: rgba(255, 77, 109, 0.06);
    }}

    .audit-box.success {{
      border-left-color: var(--accent-synapse);
      background: rgba(61, 255, 110, 0.06);
    }}

    .audit-box.warning {{
      border-left-color: var(--warning);
      background: rgba(255, 179, 0, 0.06);
    }}

    .audit-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 8px;
    }}

    .audit-title {{
      font-family: var(--font-mono);
      font-weight: 700;
      font-size: 14px;
      color: var(--text-hi);
    }}

    .audit-verdict {{
      font-family: var(--font-mono);
      font-size: 11px;
      padding: 2px 8px;
      font-weight: 700;
    }}

    .audit-verdict.false {{
      background: var(--error);
      color: #fff;
    }}

    .audit-body {{
      font-size: 13px;
      color: var(--text-mid);
      line-height: 1.6;
    }}

    /* UNIT ECONOMICS BOX */
    .unit-economics-list {{
      display: flex;
      flex-direction: column;
      gap: 12px;
      margin-top: 12px;
    }}

    .unit-item {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 12px;
      background: var(--bg-card);
      border: 1px solid var(--border-color);
    }}

    .unit-meta {{
      display: flex;
      flex-direction: column;
    }}

    .unit-name {{
      font-family: var(--font-mono);
      font-weight: 600;
      color: var(--text-hi);
    }}

    .unit-sub {{
      font-size: 11px;
      color: var(--text-low);
    }}

    .unit-cost {{
      font-family: var(--font-mono);
      font-size: 16px;
      font-weight: 700;
      text-align: right;
    }}

    /* TAB CONTENT TOGGLE */
    .tab-content {{
      display: none;
    }}

    .tab-content.active {{
      display: block;
    }}

    /* FOOTER */
    footer {{
      margin-top: 40px;
      border-top: 1px solid var(--border-color);
      padding: 24px 32px;
      text-align: center;
      font-family: var(--font-mono);
      font-size: 12px;
      color: var(--text-low);
    }}

    @media (max-width: 1024px) {{
      .dashboard-grid, .grid-2col {{
        grid-template-columns: 1fr;
      }}
    }}
  </style>
</head>
<body>

  <!-- HEADER -->
  <header>
    <div class="brand">
      <div class="brand-badge">BRAIN003</div>
      <div>
        <div class="brand-title">PONTUA+ // DASHBOARD ESTRATÉGICO</div>
        <div class="brand-subtitle">Banco Aurora · Análise Executiva de Desempenho & Auditoria do Pix</div>
      </div>
    </div>
    <div class="header-actions">
      <div class="status-pill">
        <div class="status-dot"></div>
        <span>ALERTA CONTRATUAL: VAREJO &lt; 20%</span>
      </div>
    </div>
  </header>

  <div class="container">
    
    <!-- NAVIGATION TABS -->
    <div class="nav-tabs">
      <button class="tab-btn active" onclick="switchTab('tab-visao-geral')">01 // VISÃO ESTRATÉGICA & METAS</button>
      <button class="tab-btn" onclick="switchTab('tab-auditoria')">02 // AUDITORIA DAS 3 AFIRMAÇÕES</button>
      <button class="tab-btn" onclick="switchTab('tab-economics')">03 // ECONOMIA UNITÁRIA & CUSTOS</button>
      <button class="tab-btn" onclick="switchTab('tab-segmentacao')">04 // SEGMENTAÇÃO DE CLIENTES</button>
      <button class="tab-btn" onclick="switchTab('tab-dados')">05 // TABELA DE DADOS & KPIS</button>
    </div>

    <!-- SCORECARDS (SEMPRE VISÍVEIS) -->
    <div class="kpi-grid">
      <div class="kpi-card">
        <div class="kpi-overline">Volume Resgatado (Ano)</div>
        <div class="kpi-value" id="kpi-vol-total">320,3 M</div>
        <div class="kpi-subtext">Pós-Pix: +103% no volume mensal</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-overline">Share Varejo Atual (Set/26)</div>
        <div class="kpi-value badge-bad" id="kpi-share-varejo">13,0%</div>
        <div class="kpi-subtext">Meta: &ge; 20,0% <span class="badge-bad">(-7,0 p.p. Inadimplente)</span></div>
      </div>
      <div class="kpi-card">
        <div class="kpi-overline">Share Aéreas Atual (Set/26)</div>
        <div class="kpi-value badge-warn" id="kpi-share-aereas">59,0%</div>
        <div class="kpi-subtext">Meta: &ge; 50,0% <span class="badge-ok">(Margem de +9,0 p.p.)</span></div>
      </div>
      <div class="kpi-card">
        <div class="kpi-overline">Impacto Pix (Acumulado)</div>
        <div class="kpi-value badge-bad" id="kpi-pix-val">R$ 721,6 mil</div>
        <div class="kpi-subtext">37,98 M pontos a R$ 0,0190/pt</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-overline">Breakage Real (Migração)</div>
        <div class="kpi-value badge-ok" id="kpi-breakage">19,78%</div>
        <div class="kpi-subtext">Teto: &le; 20,0% <span class="badge-ok">(Conforme)</span></div>
      </div>
    </div>

    <!-- TAB 1: VISÃO GERAL & METAS -->
    <div id="tab-visao-geral" class="tab-content active">
      <div class="dashboard-grid">
        <div class="card">
          <div class="card-header">
            <div>
              <div class="card-title">EVOLUÇÃO DOS SHARES DE RESGATE VS METAS CONTRATUAIS (%)</div>
              <div class="card-desc">Acompanhamento mensal da composição de resgate e violação do contrato de Varejo</div>
            </div>
          </div>
          <div class="chart-container">
            <canvas id="chartShares"></canvas>
          </div>
        </div>

        <div class="card">
          <div class="card-header">
            <div>
              <div class="card-title">VOLUME ABSOLUTO DE PONTOS (M)</div>
              <div class="card-desc">Efeito de diluição do denominador causado pelo Pix</div>
            </div>
          </div>
          <div class="chart-container">
            <canvas id="chartVolume"></canvas>
          </div>
        </div>
      </div>

      <div class="grid-2col">
        <div class="audit-box danger">
          <div class="audit-header">
            <span class="audit-title">DIAGNÓSTICO DA QUEBRA DA META DE VAREJO</span>
            <span class="audit-verdict false">CRÍTICO</span>
          </div>
          <div class="audit-body">
            O Varejo caiu de <strong>20,3% (mai/26)</strong> para <strong>13,0% (set/26)</strong>. No entanto, o volume absoluto em Varejo permaneceu estável em <strong>~4,0 a 4,3 milhões de pontos/mês</strong>. 
            O descumprimento contratual é fruto exclusivo do <strong>efeito diluição</strong>: a injeção repentina de 9,4 milhões de pontos mensais em Pix expandiu o denominador em +55%, derrubando o percentual de Varejo.
          </div>
        </div>

        <div class="audit-box warning">
          <div class="audit-header">
            <span class="audit-title">PRESSÃO NA META DE PASSAGENS AÉREAS</span>
            <span class="audit-verdict false">ATENÇÃO</span>
          </div>
          <div class="audit-body">
            O share de passagens aéreas caiu de <strong>80,7%</strong> para <strong>56,3% em junho</strong> e está atualmente em <strong>59,0%</strong>. 
            Embora ainda cumpra o piso contratual de 50%, a margem de segurança foi severamente reduzida para apenas 9 pontos percentuais.
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 2: AUDITORIA DAS 3 AFIRMAÇÕES -->
    <div id="tab-auditoria" class="tab-content">
      <div class="grid-3col">
        
        <!-- AFIRMAÇÃO 1: CRM -->
        <div class="card">
          <div class="audit-header">
            <span class="card-title">01 // CRM MARKETING</span>
            <span class="audit-verdict false">FALSA</span>
          </div>
          <p style="font-size: 13px; font-style: italic; color: var(--text-hi); margin-bottom: 12px;">
            "A comunicação de lançamento explica o sucesso do Pix."
          </p>
          <div class="chart-container" style="height: 220px;">
            <canvas id="chartCrm"></canvas>
          </div>
          <div class="audit-body" style="margin-top: 16px;">
            • Apenas <strong>39 dos 2.140 clientes Pix</strong> (1,8%) clicaram no e-mail de lançamento.<br>
            • Usuários <strong>não impactados</strong> tiveram conversão de <strong>18,13%</strong>, superior a quem clicou (<strong>15,48%</strong>).<br>
            • Adoção foi 100% orgânica pela atratividade do produto.
          </div>
        </div>

        <!-- AFIRMAÇÃO 2: OPERADOR -->
        <div class="card">
          <div class="audit-header">
            <span class="card-title">02 // TAXA DO OPERADOR</span>
            <span class="audit-verdict false">ERRO DE CÁLCULO</span>
          </div>
          <p style="font-size: 13px; font-style: italic; color: var(--text-hi); margin-bottom: 12px;">
            "Na verdade o Pix sai a cerca de R$ 0,016 por ponto."
          </p>
          <div class="chart-container" style="height: 220px;">
            <canvas id="chartTaxaPix"></canvas>
          </div>
          <div class="audit-body" style="margin-top: 16px;">
            • O programa pagou rigorosamente <strong>R$ 0,019000 por ponto</strong> em todos os 2.808 pedidos aprovados.<br>
            • <strong>Origem do erro:</strong> O operador somou pedidos cancelados e estornados no denominador (pontos brutos), mas dividiu apenas pelos reais aprovados.<br>
            • Discrepância auditada e reconciliada em 100%.
          </div>
        </div>

        <!-- AFIRMAÇÃO 3: DIRETOR / BREAKAGE -->
        <div class="card">
          <div class="audit-header">
            <span class="card-title">03 // BREAKAGE</span>
            <span class="audit-verdict false">CONFUSÃO CONCEITUAL</span>
          </div>
          <p style="font-size: 13px; font-style: italic; color: var(--text-hi); margin-bottom: 12px;">
            "Nosso breakage está em 40%! Nossa meta é não passar de 20%!"
          </p>
          <div class="chart-container" style="height: 220px;">
            <canvas id="chartBreakage"></canvas>
          </div>
          <div class="audit-body" style="margin-top: 16px;">
            • O diretor confundiu <strong>Taxa de Resgate (42,45%)</strong> com <strong>Breakage</strong>.<br>
            • O Breakage real da base migrada é <strong>19,78%</strong>, dentro da meta de &le; 20%.<br>
            • Os créditos novos expiram em 24 meses (apenas a partir de Set/2027), tendo breakage atual de <strong>0,0%</strong>.
          </div>
        </div>

      </div>
    </div>

    <!-- TAB 3: ECONOMIA UNITÁRIA & CUSTOS -->
    <div id="tab-economics" class="tab-content">
      <div class="dashboard-grid">
        <div class="card">
          <div class="card-header">
            <div>
              <div class="card-title">COMPARATIVO DE CUSTO LÍQUIDO POR PONTO RESGATADO (R$)</div>
              <div class="card-desc">Custo efetivo desembolsado pelo programa por categoria de produto</div>
            </div>
          </div>
          <div class="chart-container">
            <canvas id="chartUnitCosts"></canvas>
          </div>
        </div>

        <div class="card">
          <div class="card-header">
            <div>
              <div class="card-title">ESTRUTURA DE CUSTOS UNITÁRIOS</div>
              <div class="card-desc">Diferencial de margem por parceiro</div>
            </div>
          </div>
          <div class="unit-economics-list">
            <div class="unit-item">
              <div class="unit-meta">
                <span class="unit-name">Pix Pontua+ (Cashback)</span>
                <span class="unit-sub">Dinheiro na conta (Mais oneroso ao programa)</span>
              </div>
              <div class="unit-cost badge-bad">R$ 0,01900</div>
            </div>
            <div class="unit-item">
              <div class="unit-meta">
                <span class="unit-name">Passagens Aéreas (Líquido)</span>
                <span class="unit-sub">Após coparticipação em dinheiro do cliente</span>
              </div>
              <div class="unit-cost badge-warn">R$ 0,01500</div>
            </div>
            <div class="unit-item">
              <div class="unit-meta">
                <span class="unit-name">Varejo: Produtos (Casa&Cia, Tech10, Mega)</span>
                <span class="unit-sub">Parceiros próprios do grupo empresarial</span>
              </div>
              <div class="unit-cost badge-ok">R$ 0,01390</div>
            </div>
            <div class="unit-item">
              <div class="unit-meta">
                <span class="unit-name">Varejo: Transferências (Nuvem, Pontos Max)</span>
                <span class="unit-sub">Parceiros de fidelidade integrados</span>
              </div>
              <div class="unit-cost badge-ok">R$ 0,01250</div>
            </div>
          </div>
          <div class="audit-box danger" style="margin-top: 16px;">
            <div class="audit-body">
              <strong>Impacto Financeiro Negativo:</strong> O Pix custa <strong>26,7% mais caro</strong> por ponto do que Aéreas e <strong>52,0% mais caro</strong> do que Varejo Parceiros. Cada resgate via Pix destrói rentabilidade e afasta o programa das metas contratuais.
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 4: SEGMENTAÇÃO DE CLIENTES -->
    <div id="tab-segmentacao" class="tab-content">
      <div class="grid-2col">
        <div class="card">
          <div class="card-header">
            <div>
              <div class="card-title">PENETRAÇÃO DO PIX POR CLASSE DE CARTÃO (PÓS-PIX)</div>
              <div class="card-desc">% do volume de resgate em Pix por classe de cartão (Jun a Set/26)</div>
            </div>
          </div>
          <div class="chart-container">
            <canvas id="chartCardShare"></canvas>
          </div>
        </div>

        <div class="card">
          <div class="card-header">
            <div>
              <div class="card-title">DISTRIBUIÇÃO DE CANAIS (APP VS WEB)</div>
              <div class="card-desc">Volume de pontos transacionados por ponto de contato</div>
            </div>
          </div>
          <div class="chart-container">
            <canvas id="chartChannels"></canvas>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 5: TABELA DE DADOS & KPIS -->
    <div id="tab-dados" class="tab-content">
      <div class="card">
        <div class="card-header">
          <div>
            <div class="card-title">SÉRIE HISTÓRICA MENSAL DO PROGRAMA (OUT/2025 A SET/2026)</div>
            <div class="card-desc">Dados agregados certificados pelo pipeline analítico</div>
          </div>
        </div>
        <div class="table-container">
          <table id="tableMonthly">
            <thead>
              <tr>
                <th>Mês</th>
                <th>Créditos (M)</th>
                <th>Resgates (M)</th>
                <th>Aéreas (M)</th>
                <th>Varejo (M)</th>
                <th>Pix (M)</th>
                <th>Share Aéreas</th>
                <th>Share Varejo</th>
                <th>Share Pix</th>
                <th>Custo Total (R$)</th>
                <th>Custo Médio/Pt</th>
                <th>Status Metas</th>
              </tr>
            </thead>
            <tbody>
              <!-- Renderizado via JS -->
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- CHAT FLUTUANTE DO AGENTE IA -->
    <div id="aiChatDrawer" style="position:fixed; bottom:24px; right:24px; z-index:999; display:flex; flex-direction:column; align-items:flex-end;">
      <!-- JANELA DE CONVERSA -->
      <div id="aiChatWindow" style="display:none; width:400px; height:520px; background:var(--bg-card); border:1px solid var(--accent-data); box-shadow:0 12px 36px rgba(0,0,0,0.6); display:flex; flex-direction:column; margin-bottom:12px; overflow:hidden;">
        <div style="background:var(--bg-surface); padding:12px 16px; border-bottom:1px solid var(--border-color); display:flex; justify-content:space-between; align-items:center;">
          <div style="display:flex; align-items:center; gap:8px;">
            <div style="width:8px; height:8px; background:var(--accent-synapse); border-radius:50%;"></div>
            <strong style="font-family:var(--font-mono); font-size:13px; color:var(--text-hi);">PONTUA+ AI AGENT (GEMINI)</strong>
          </div>
          <button onclick="toggleChat()" style="background:none; border:none; color:var(--text-mid); font-size:18px; cursor:pointer;">&times;</button>
        </div>
        <div id="aiChatMessages" style="flex:1; padding:16px; overflow-y:auto; display:flex; flex-direction:column; gap:12px; font-size:13px; font-family:var(--font-body); line-height:1.5;">
          <div style="background:var(--bg-surface); padding:10px 14px; border-left:3px solid var(--accent-data); color:var(--text-hi);">
            Olá! Sou o <strong>Agente Analítico do Pontua+</strong>. Posso responder dúvidas sobre o impacto do Pix, metas contratuais, custos por modalidade ou auditoria das afirmações da diretoria.
          </div>
        </div>
        <div style="padding:12px; background:var(--bg-surface); border-top:1px solid var(--border-color); display:flex; gap:8px;">
          <input type="text" id="aiChatInput" placeholder="Faça uma pergunta executiva..." onkeypress="if(event.key==='Enter') sendChatMessage()" style="flex:1; background:var(--bg-deep); border:1px solid var(--border-color); color:#fff; padding:8px 12px; font-family:var(--font-mono); font-size:12px; outline:none;">
          <button onclick="sendChatMessage()" style="background:var(--primary); color:#fff; border:none; padding:8px 14px; font-family:var(--font-mono); font-size:12px; font-weight:700; cursor:pointer;">ENVIAR</button>
        </div>
      </div>

      <!-- BOTÃO FLUTUANTE -->
      <button onclick="toggleChat()" style="background:var(--primary); color:#fff; border:1px solid var(--accent-data); padding:12px 20px; font-family:var(--font-mono); font-size:13px; font-weight:700; cursor:pointer; display:flex; align-items:center; gap:10px; box-shadow:0 4px 16px rgba(30,43,255,0.4);">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>
        <span>CONSULTAR AGENTE IA</span>
      </button>
    </div>

  </div>

  <footer>
    PONTUA+ INTELLIGENCE LAB · DESENVOLVIDO PARA AVALIAÇÃO ANALYTICS ENGINEER · BANCO AURORA / BRAIN003
  </footer>

  <!-- SCRIPT COM DADOS EMBUTIDOS E RENDERIZAÇÃO DOS GRÁFICOS -->
  <script>
    // DADOS EMBUTIDOS GERADOS PELO PIPELINE
    const monthlyKpis = {json.dumps(monthly_kpis)};
    const crmCohorts = {json.dumps(crm_cohorts)};
    const operatorAudit = {json.dumps(operator_audit)};
    const breakageData = {json.dumps(breakage_data)};
    const categoryCardData = {json.dumps(category_card_data)};

    // FUNÇÃO DO CHAT FLUTUANTE
    let chatOpen = false;
    function toggleChat() {{
      const win = document.getElementById('aiChatWindow');
      chatOpen = !chatOpen;
      win.style.display = chatOpen ? 'flex' : 'none';
      if (chatOpen) document.getElementById('aiChatInput').focus();
    }}

    async function sendChatMessage() {{
      const input = document.getElementById('aiChatInput');
      const query = input.value.trim();
      if (!query) return;

      const msgs = document.getElementById('aiChatMessages');
      
      // User msg
      const userDiv = document.createElement('div');
      userDiv.style.alignSelf = 'flex-end';
      userDiv.style.background = 'var(--primary)';
      userDiv.style.color = '#fff';
      userDiv.style.padding = '8px 12px';
      userDiv.style.maxWidth = '85%';
      userDiv.textContent = query;
      msgs.appendChild(userDiv);
      input.value = '';
      msgs.scrollTop = msgs.scrollHeight;

      // Loading indicator
      const loadDiv = document.createElement('div');
      loadDiv.style.alignSelf = 'flex-start';
      loadDiv.style.color = 'var(--text-mid)';
      loadDiv.style.fontStyle = 'italic';
      loadDiv.textContent = 'Processando com Gemini...';
      msgs.appendChild(loadDiv);
      msgs.scrollTop = msgs.scrollHeight;

      try {{
        const resp = await fetch('/api/chat', {{
          method: 'POST',
          headers: {{ 'Content-Type': 'application/json' }},
          body: JSON.stringify({{ query: query }})
        }});
        const data = await resp.json();
        loadDiv.remove();

        const agentDiv = document.createElement('div');
        agentDiv.style.alignSelf = 'flex-start';
        agentDiv.style.background = 'var(--bg-surface)';
        agentDiv.style.borderLeft = '3px solid var(--accent-synapse)';
        agentDiv.style.color = 'var(--text-hi)';
        agentDiv.style.padding = '10px 14px';
        agentDiv.style.maxWidth = '90%';
        agentDiv.textContent = data.answer || data.error;
        msgs.appendChild(agentDiv);
      }} catch (err) {{
        loadDiv.remove();
        const errDiv = document.createElement('div');
        errDiv.style.alignSelf = 'flex-start';
        errDiv.style.background = 'rgba(255,77,109,0.15)';
        errDiv.style.borderLeft = '3px solid var(--error)';
        errDiv.style.color = 'var(--text-hi)';
        errDiv.style.padding = '10px 14px';
        errDiv.innerHTML = 'Para conversar com o agente ao vivo, execute no terminal:<br><code>py server.py</code> e acesse via <code>http://localhost:8000</code>.<br><br>Ou execute diretamente via CLI: <code>py agente/agent.py "' + query + '"</code>';
        msgs.appendChild(errDiv);
      }}
      msgs.scrollTop = msgs.scrollHeight;
    }}

    // CHART CONFIG DEFAULTS (DARK BRAIN003 THEME)
    Chart.defaults.color = '#A9B4D0';
    Chart.defaults.font.family = "'Roboto Mono', monospace";
    Chart.defaults.plugins.tooltip.backgroundColor = '#141C3E';
    Chart.defaults.plugins.tooltip.titleColor = '#EAF0FF';
    Chart.defaults.plugins.tooltip.borderColor = '#212C5B';
    Chart.defaults.plugins.tooltip.borderWidth = 1;
    Chart.defaults.plugins.tooltip.padding = 10;

    // TAB SWITCHER
    function switchTab(tabId) {{
      document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
      document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
      
      event.target.classList.add('active');
      document.getElementById(tabId).classList.add('active');
    }}

    // POPULAR TABELA DE DADOS
    const tbody = document.querySelector('#tableMonthly tbody');
    monthlyKpis.forEach(row => {{
      const tr = document.createElement('tr');
      const metaStatus = (row.meta_aereas_atingida && row.meta_varejo_atingida)
        ? '<span class="badge-ok">CONFORME</span>'
        : (row.meta_aereas_atingida && !row.meta_varejo_atingida)
        ? '<span class="badge-bad">VAREJO VIOLADO</span>'
        : '<span class="badge-bad">AMBAS VIOLADAS</span>';

      tr.innerHTML = `
        <td class="mono"><strong>${{row.mes}}</strong></td>
        <td class="mono">${{(row.pontos_creditados / 1e6).toFixed(2)}}</td>
        <td class="mono">${{(row.total_pontos_resgatados / 1e6).toFixed(2)}}</td>
        <td class="mono">${{(row.pontos_aereas / 1e6).toFixed(2)}}</td>
        <td class="mono">${{(row.pontos_varejo / 1e6).toFixed(2)}}</td>
        <td class="mono">${{row.pontos_pix ? (row.pontos_pix / 1e6).toFixed(2) : '0.00'}}</td>
        <td class="mono">${{row.share_aereas_pct}}%</td>
        <td class="mono ${{row.share_varejo_pct < 20 ? 'badge-bad' : ''}}">${{row.share_varejo_pct}}%</td>
        <td class="mono">${{row.share_pix_pct}}%</td>
        <td class="mono">R$ ${{row.custo_total_programa_reais.toLocaleString('pt-BR', {{minimumFractionDigits: 2}})}}</td>
        <td class="mono">R$ ${{row.custo_medio_por_ponto.toFixed(5)}}</td>
        <td>${{metaStatus}}</td>
      `;
      tbody.appendChild(tr);
    }});

    // INICIALIZAR GRÁFICOS
    window.addEventListener('DOMContentLoaded', () => {{
      const labels = monthlyKpis.map(r => r.mes);

      // 1. CHART SHARES
      new Chart(document.getElementById('chartShares'), {{
        type: 'line',
        data: {{
          labels: labels,
          datasets: [
            {{
              label: 'Share Aéreas (%)',
              data: monthlyKpis.map(r => r.share_aereas_pct),
              borderColor: '#1E2BFF',
              backgroundColor: 'rgba(30, 43, 255, 0.1)',
              tension: 0.3,
              fill: false,
              borderWidth: 2.5
            }},
            {{
              label: 'Share Varejo (%)',
              data: monthlyKpis.map(r => r.share_varejo_pct),
              borderColor: '#3DFF6E',
              backgroundColor: 'rgba(61, 255, 110, 0.1)',
              tension: 0.3,
              fill: false,
              borderWidth: 2.5
            }},
            {{
              label: 'Share Pix (%)',
              data: monthlyKpis.map(r => r.share_pix_pct),
              borderColor: '#FF4D6D',
              backgroundColor: 'rgba(255, 77, 109, 0.15)',
              tension: 0.3,
              fill: true,
              borderWidth: 2.5
            }},
            {{
              label: 'Meta Mínima Varejo (20%)',
              data: labels.map(() => 20),
              borderColor: '#FFB300',
              borderDash: [5, 5],
              borderWidth: 2,
              pointRadius: 0,
              fill: false
            }},
            {{
              label: 'Meta Mínima Aéreas (50%)',
              data: labels.map(() => 50),
              borderColor: '#00CFFF',
              borderDash: [5, 5],
              borderWidth: 2,
              pointRadius: 0,
              fill: false
            }}
          ]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          scales: {{
            y: {{
              min: 0,
              max: 100,
              grid: {{ color: 'rgba(33, 44, 91, 0.4)' }},
              ticks: {{ callback: v => v + '%' }}
            }},
            x: {{ grid: {{ color: 'rgba(33, 44, 91, 0.4)' }} }}
          }}
        }}
      }});

      // 2. CHART VOLUME EMPILHADO
      new Chart(document.getElementById('chartVolume'), {{
        type: 'bar',
        data: {{
          labels: labels,
          datasets: [
            {{
              label: 'Aéreas (M pts)',
              data: monthlyKpis.map(r => (r.pontos_aereas / 1e6).toFixed(2)),
              backgroundColor: '#1E2BFF'
            }},
            {{
              label: 'Varejo (M pts)',
              data: monthlyKpis.map(r => (r.pontos_varejo / 1e6).toFixed(2)),
              backgroundColor: '#3DFF6E'
            }},
            {{
              label: 'Pix (M pts)',
              data: monthlyKpis.map(r => ((r.pontos_pix || 0) / 1e6).toFixed(2)),
              backgroundColor: '#FF4D6D'
            }}
          ]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          scales: {{
            x: {{ stacked: true, grid: {{ display: false }} }},
            y: {{ stacked: true, grid: {{ color: 'rgba(33, 44, 91, 0.4)' }} }}
          }}
        }}
      }});

      // 3. CHART CRM CONVERSION
      new Chart(document.getElementById('chartCrm'), {{
        type: 'bar',
        data: {{
          labels: crmCohorts.map(c => c.crm_pix_cohort.replace(/^[0-9]\.\s*/, '')),
          datasets: [{{
            label: 'Taxa de Conversão para Pix (%)',
            data: crmCohorts.map(c => c.taxa_conversao_pct),
            backgroundColor: ['#1E2BFF', '#2438E6', '#00CFFF', '#6B7699', '#3DFF6E']
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{ legend: {{ display: false }} }},
          scales: {{
            y: {{ min: 0, max: 25, ticks: {{ callback: v => v + '%' }} }}
          }}
        }}
      }});

      // 4. CHART TAXA PIX AUDIT
      new Chart(document.getElementById('chartTaxaPix'), {{
        type: 'bar',
        data: {{
          labels: operatorAudit.map(r => r.mes),
          datasets: [
            {{
              label: 'Taxa do Relatório (~R$ 0,016)',
              data: operatorAudit.map(r => r.relatorio_taxa_calculada),
              backgroundColor: 'rgba(255, 77, 109, 0.6)'
            }},
            {{
              label: 'Taxa Real Efetiva (R$ 0,0190)',
              data: operatorAudit.map(r => r.sistema_taxa_aprovada_real),
              backgroundColor: '#3DFF6E'
            }}
          ]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          scales: {{
            y: {{ min: 0.012, max: 0.021, ticks: {{ callback: v => 'R$ ' + v.toFixed(3) }} }}
          }}
        }}
      }});

      // 5. CHART BREAKAGE AUDIT
      new Chart(document.getElementById('chartBreakage'), {{
        type: 'bar',
        data: {{
          labels: ['Confusão Diretor (Resgate)', 'Breakage Migrado (Real)', 'Teto Meta Breakage', 'Breakage Safra Nova'],
          datasets: [{{
            data: [42.45, 19.78, 20.0, 0.0],
            backgroundColor: ['#FF4D6D', '#3DFF6E', '#FFB300', '#00CFFF']
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{ legend: {{ display: false }} }},
          scales: {{
            y: {{ min: 0, max: 50, ticks: {{ callback: v => v + '%' }} }}
          }}
        }}
      }});

      // 6. CHART UNIT COSTS
      new Chart(document.getElementById('chartUnitCosts'), {{
        type: 'bar',
        data: {{
          labels: ['Pix Pontua+', 'Aéreas (Líquido)', 'Varejo (Produtos)', 'Varejo (Parceiros)'],
          datasets: [{{
            data: [0.0190, 0.0150, 0.0139, 0.0125],
            backgroundColor: ['#FF4D6D', '#FFB300', '#3DFF6E', '#00CFFF']
          }}]
        }},
        options: {{
          indexAxis: 'y',
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{ legend: {{ display: false }} }},
          scales: {{
            x: {{ min: 0, max: 0.022, ticks: {{ callback: v => 'R$ ' + v.toFixed(4) }} }}
          }}
        }}
      }});

      // 7. CHART CARD CLASS SHARE
      const cardClasses = ['Essencial', 'Gold', 'Platinum', 'Platinum Elo', 'Infinite', 'Black'];
      const cardPixShares = [34.7, 36.6, 34.2, 29.0, 20.7, 18.4];
      new Chart(document.getElementById('chartCardShare'), {{
        type: 'bar',
        data: {{
          labels: cardClasses,
          datasets: [{{
            label: 'Share de Pix Pós-Lançamento (%)',
            data: cardPixShares,
            backgroundColor: '#00CFFF'
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          scales: {{
            y: {{ min: 0, max: 45, ticks: {{ callback: v => v + '%' }} }}
          }}
        }}
      }});

      // 8. CHART CHANNELS
      new Chart(document.getElementById('chartChannels'), {{
        type: 'doughnut',
        data: {{
          labels: ['APP Mobile (63,9%)', 'Portal WEB (36,1%)'],
          datasets: [{{
            data: [208.14, 112.13],
            backgroundColor: ['#1E2BFF', '#00CFFF'],
            borderColor: '#0E142F',
            borderWidth: 2
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false
        }}
      }});

    }});
  </script>
</body>
</html>
"""
    
    with open("entrega/dashboard/index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
        
    print("Dashboard gerado com sucesso em entrega/dashboard/index.html!")

if __name__ == "__main__":
    build_dashboard()
