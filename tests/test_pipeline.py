"""
Testes Automatizados de Validação e Reconciliação dos Modelos de Dados (Pontua+)
Garante integridade referencial, unicidade de grão, reconciliação contábil e auditoria das 3 afirmações.
"""

import duckdb
import pytest

DB_PATH = "pipeline/output/pontua_plus.duckdb"

@pytest.fixture(scope="module")
def con():
    conn = duckdb.connect(DB_PATH, read_only=True)
    yield conn
    conn.close()

# ---------------------------------------------------------
# 1. TESTES DE UNICIDADE DE GRÃO E CHAVES PRIMÁRIAS (PK)
# ---------------------------------------------------------

def test_dim_users_pk_uniqueness(con):
    res = con.sql("""
    SELECT 
        COUNT(*) as total_rows,
        COUNT(DISTINCT user_id) as distinct_keys,
        COUNT(*) FILTER (WHERE user_id IS NULL) as null_keys
    FROM dim_users
    """).fetchone()
    total, distinct, nulls = res
    assert nulls == 0, "dim_users possui chaves nulas"
    assert total == distinct, f"dim_users violou a unicidade da PK (total={total}, distinct={distinct})"

def test_fct_order_items_pk_uniqueness(con):
    res = con.sql("""
    SELECT 
        COUNT(*) as total_rows,
        COUNT(DISTINCT order_item_id) as distinct_keys,
        COUNT(*) FILTER (WHERE order_item_id IS NULL) as null_keys
    FROM fct_order_items
    """).fetchone()
    total, distinct, nulls = res
    assert nulls == 0, "fct_order_items possui chaves nulas"
    assert total == distinct, f"fct_order_items violou a unicidade da PK (total={total}, distinct={distinct})"

def test_fct_points_movements_pk_uniqueness(con):
    res = con.sql("""
    SELECT 
        COUNT(*) as total_rows,
        COUNT(DISTINCT movement_id) as distinct_keys,
        COUNT(*) FILTER (WHERE movement_id IS NULL) as null_keys
    FROM fct_points_movements
    """).fetchone()
    total, distinct, nulls = res
    assert nulls == 0, "fct_points_movements possui chaves nulas"
    assert total == distinct, f"fct_points_movements violou a unicidade da PK"

def test_agg_monthly_kpis_grain_uniqueness(con):
    res = con.sql("""
    SELECT COUNT(*), COUNT(DISTINCT mes) FROM agg_monthly_kpis
    """).fetchone()
    assert res[0] == res[1], "agg_monthly_kpis possui duplicidade no grão 'mes'"

def test_agg_breakage_grain_uniqueness(con):
    res = con.sql("""
    SELECT COUNT(*), COUNT(DISTINCT safra) FROM agg_breakage_analysis
    """).fetchone()
    assert res[0] == res[1], "agg_breakage_analysis possui duplicidade no grão 'safra'"

# ---------------------------------------------------------
# 2. TESTES DE INTEGRIDADE REFERENCIAL E QUALIDADE
# ---------------------------------------------------------

def test_order_items_user_id_resolution(con):
    """Garante que a junção com carts resolveu o problema do orders.user_id nulo."""
    res = con.sql("""
    SELECT 
        COUNT(*) as total,
        COUNT(*) FILTER (WHERE user_id IS NULL) as null_users
    FROM fct_order_items
    """).fetchone()
    assert res[1] == 0, "fct_order_items possui user_id nulo após resolução via carts"

def test_order_items_foreign_key_to_users(con):
    res = con.sql("""
    SELECT COUNT(*) 
    FROM fct_order_items oi
    LEFT JOIN dim_users u ON oi.user_id = u.user_id
    WHERE u.user_id IS NULL
    """).fetchone()
    assert res[0] == 0, "fct_order_items contém user_id órfão sem correspondência em dim_users"

# ---------------------------------------------------------
# 3. TESTES DE RECONCILIAÇÃO CONTÁBIL E REGRAS DE NEGÓCIO
# ---------------------------------------------------------

def test_points_redemption_reconciliation(con):
    """Valida a reconciliação contábil exata entre fct_order_items, redeemed_points e points_ledger."""
    # 1. Total bruto de resgates iniciados (Aprovados + Estornados)
    rp_resgate_bruto = con.sql("""
    SELECT SUM(-points) 
    FROM 'dados/redeemed_points.csv' 
    WHERE movement_type = 'RESGATE'
    """).fetchone()[0]
    
    ledger_resgate_bruto = con.sql("""
    SELECT SUM(-points) 
    FROM fct_points_movements 
    WHERE operation_code = 2
    """).fetchone()[0]
    
    assert rp_resgate_bruto == 323423650, f"Total bruto divergente em redeemed_points: {rp_resgate_bruto}"
    assert ledger_resgate_bruto == 323423650, f"Total bruto divergente no ledger: {ledger_resgate_bruto}"
    assert rp_resgate_bruto == ledger_resgate_bruto, "Descasamento contábil no resgate bruto"

    # 2. Reconciliação dos Estornos (Operação 14: ESTORNO_PEDIDO)
    ledger_estornos = con.sql("""
    SELECT SUM(points) 
    FROM fct_points_movements 
    WHERE operation_code = 14
    """).fetchone()[0]
    
    itens_estornados_pts = con.sql("""
    SELECT SUM(-rp.points)
    FROM 'dados/redeemed_points.csv' rp
    JOIN fct_order_items oi ON rp.order_item_id = oi.order_item_id
    WHERE rp.movement_type = 'RESGATE' AND oi.item_status = 'ESTORNADO'
    """).fetchone()[0]
    
    itens_aprovados_reembolsos = con.sql("""
    SELECT SUM(refunded_points)
    FROM fct_order_items
    WHERE item_status = 'APROVADO'
    """).fetchone()[0]
    
    total_reembolsado_sistema = itens_estornados_pts + itens_aprovados_reembolsos
    assert ledger_estornos == 3396211, f"Estorno no ledger divergente: {ledger_estornos}"
    assert total_reembolsado_sistema == 3396211, f"Soma de estornos e reembolsos diverge: {total_reembolsado_sistema}"
    assert ledger_estornos == total_reembolsado_sistema, "Descasamento contábil no estorno de pedidos"

def test_pix_unit_rate_is_strictly_0019(con):
    """Valida se todo resgate de Pix aprovado foi cobrado rigorosamente a R$ 0,019 por ponto."""
    res = con.sql("""
    SELECT 
        COUNT(*) as total_approved_pix,
        MIN(product_value / paid_points) as min_rate,
        MAX(product_value / paid_points) as max_rate
    FROM fct_order_items
    WHERE is_pix = TRUE AND item_status = 'APROVADO'
    """).fetchone()
    cnt, min_r, max_r = res
    assert cnt == 2808, f"Contagem de itens Pix aprovados inesperada: {cnt}"
    assert round(min_r, 4) == 0.0190, f"Taxa mínima do Pix diferente de 0.019: {min_r}"
    assert round(max_r, 4) == 0.0190, f"Taxa máxima do Pix diferente de 0.019: {max_r}"

def test_operator_report_discrepancy_explanation(con):
    """Valida matematicamente que o relatório do operador somou pedidos cancelados e estornados no denominador."""
    diff = con.sql("""
    SELECT COUNT(*) 
    FROM agg_operator_audit
    WHERE relatorio_transacoes != sistema_bruto_transacoes
       OR relatorio_pontos != sistema_bruto_pontos
    """).fetchone()[0]
    assert diff == 0, "O relatório do operador não corresponde aos valores brutos (todos os status) do sistema"

def test_breakage_statement_audit(con):
    """Valida os números que refutam a afirmação do diretor sobre o breakage."""
    migrated_breakage = con.sql("""
    SELECT taxa_breakage_pct 
    FROM agg_breakage_analysis 
    WHERE safra LIKE '%Base Migrada%'
    """).fetchone()[0]
    
    total_redemption_rate = con.sql("""
    SELECT 
        ROUND(100.0 * SUM(-points) FILTER (WHERE operation_code = 2) / 
                      SUM(points) FILTER (WHERE operation_code IN (1, 100)), 2)
    FROM fct_points_movements
    """).fetchone()[0]
    
    # Breakage real da base migrada é 19.78% (abaixo do teto de 20%)
    assert migrated_breakage == 19.78, f"Breakage da migração divergiu: {migrated_breakage}"
    # Taxa de resgate total é ~42.45% (o número que o diretor confundiu com breakage)
    assert total_redemption_rate == 42.45, f"Taxa de resgate total divergiu: {total_redemption_rate}"

def test_crm_pix_attribution_refutation(con):
    """Valida que a taxa de conversão para Pix é praticamente igual entre quem clicou no e-mail e quem não foi impactado."""
    cohorts = con.sql("""
    SELECT crm_pix_cohort, taxa_conversao_pct 
    FROM agg_pix_crm_cohorts
    """).df().set_index('crm_pix_cohort')['taxa_conversao_pct'].to_dict()
    
    clicked_rate = cohorts['1. Clicou no Email']
    untargeted_rate = cohorts['5. Nao impactado pela campanha']
    
    # Clicou: ~15.5%; Não impactado: ~18.1% (ambos entre 15% e 19%, sem correlação causal positiva do CRM)
    assert 14.0 <= clicked_rate <= 17.0, f"Taxa de quem clicou fora do esperado: {clicked_rate}"
    assert 17.0 <= untargeted_rate <= 19.5, f"Taxa de não impactados fora do esperado: {untargeted_rate}"

def test_retail_contract_breach_post_pix(con):
    """Valida que o share de Varejo violou a meta contratual de 20% a partir de junho de 2026."""
    res = con.sql("""
    SELECT mes, share_varejo_pct, meta_varejo_atingida
    FROM agg_monthly_kpis
    WHERE mes >= '2026-06'
    """).df()
    
    for _, row in res.iterrows():
        assert row['share_varejo_pct'] < 20.0, f"Mês {row['mes']} não violou a meta de 20% de varejo: {row['share_varejo_pct']}"
        assert row['meta_varejo_atingida'] == False, f"Flag meta_varejo_atingida deveria ser False em {row['mes']}"

if __name__ == "__main__":
    pytest.main(["-v", "tests/test_pipeline.py"])
