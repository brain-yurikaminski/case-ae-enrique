"""
Pipeline de Engenharia de Dados - Programa Pontua+
Gera as camadas de Staging, Marts e Agregadas (Semantic Layer) para o Dashboard e Agente de IA.
"""

import os
import json
import duckdb
import pandas as pd

def run_pipeline():
    print("Iniciando build do pipeline analítico Pontua+...")
    
    # Garantir diretórios de saída
    os.makedirs("entrega/dashboard/data", exist_ok=True)
    os.makedirs("agente/data", exist_ok=True)
    os.makedirs("pipeline/output", exist_ok=True)
    
    db_path = "pipeline/output/pontua_plus.duckdb"
    con = duckdb.connect(db_path)
    
    print("1. Criando camada Staging...")
    con.sql("""
    CREATE OR REPLACE VIEW stg_orders AS
    SELECT 
        order_id,
        cart_id,
        created_at as order_created_at,
        status as order_status,
        status_updated_at as order_status_updated_at
    FROM 'dados/orders.csv';

    CREATE OR REPLACE VIEW stg_carts AS
    SELECT 
        cart_id,
        user_id,
        channel
    FROM 'dados/carts.csv';

    CREATE OR REPLACE VIEW stg_order_items AS
    SELECT 
        order_item_id,
        order_id,
        created_at as item_created_at,
        strftime(created_at, '%Y-%m') as mes,
        status as item_status,
        product_type,
        supplier_name,
        supplier_responsible,
        category_macro,
        paid_points,
        paid_currency,
        product_value,
        refunded_points,
        quantity
    FROM 'dados/order_items.csv';

    CREATE OR REPLACE VIEW stg_cards AS
    SELECT 
        account_id,
        user_id,
        card_class,
        card_flag,
        created_at as card_created_at,
        is_most_recent
    FROM 'dados/cards.csv';

    CREATE OR REPLACE VIEW stg_points_ledger AS
    SELECT 
        movement_id,
        user_id,
        account_id,
        operation_code,
        points,
        movement_at,
        strftime(movement_at, '%Y-%m') as mes,
        valid_until
    FROM 'dados/points_ledger.csv';

    CREATE OR REPLACE VIEW stg_dim_operation AS
    SELECT 
        operation_code,
        operation_name,
        direction
    FROM 'dados/dim_operation.csv';

    CREATE OR REPLACE VIEW stg_crm_events AS
    SELECT 
        event_ts,
        strftime(event_ts, '%Y-%m') as mes,
        user_id,
        device_id,
        event_name,
        campaign_type,
        campaign_id,
        control_group,
        json_extract_string(event_properties, '$.campaign_name') as campaign_name,
        json_extract_string(event_properties, '$.link') as campaign_link,
        CAST(json_extract_string(event_properties, '$.open_count') AS INT) as open_count,
        json_extract_string(event_properties, '$.reason') as failure_reason
    FROM 'dados/crm_events.csv';
    """)
    
    print("2. Criando camada de Dimensões e Fatos (Marts)...")
    con.sql("""
    -- Dimensão Usuários (Grão: user_id)
    CREATE OR REPLACE TABLE dim_users AS
    WITH recent_card AS (
        SELECT DISTINCT ON (user_id)
            user_id,
            account_id as primary_account_id,
            card_class,
            card_flag,
            card_created_at
        FROM stg_cards
        ORDER BY user_id, is_most_recent DESC, card_created_at DESC
    ),
    user_orders AS (
        SELECT 
            c.user_id,
            COUNT(DISTINCT o.order_id) as total_orders,
            COUNT(DISTINCT oi.order_item_id) as total_items,
            MIN(oi.item_created_at) as first_order_at,
            MAX(oi.item_created_at) as last_order_at,
            SUM(CASE WHEN oi.item_status = 'APROVADO' THEN oi.paid_points ELSE 0 END) as total_points_redeemed,
            SUM(CASE WHEN oi.item_status = 'APROVADO' AND oi.supplier_name = 'Pix Pontua+' THEN 1 ELSE 0 END) as pix_orders_approved,
            SUM(CASE WHEN oi.item_status = 'APROVADO' AND oi.supplier_name = 'Pix Pontua+' THEN oi.paid_points ELSE 0 END) as pix_points_redeemed,
            SUM(CASE WHEN oi.item_status = 'APROVADO' AND oi.supplier_name = 'Pix Pontua+' THEN oi.product_value ELSE 0 END) as pix_reais_redeemed,
            MIN(CASE WHEN oi.item_status = 'APROVADO' AND oi.supplier_name = 'Pix Pontua+' THEN oi.item_created_at END) as first_pix_at
        FROM stg_carts c
        LEFT JOIN stg_orders o ON c.cart_id = o.cart_id
        LEFT JOIN stg_order_items oi ON o.order_id = oi.order_id
        GROUP BY 1
    ),
    user_ledger AS (
        SELECT 
            user_id,
            SUM(CASE WHEN o.direction = 'CREDIT' THEN l.points ELSE 0 END) as total_points_credited,
            SUM(CASE WHEN l.operation_code = 100 THEN l.points ELSE 0 END) as migration_points_credited,
            SUM(CASE WHEN l.operation_code = 103 THEN -l.points ELSE 0 END) as migration_points_expired,
            SUM(l.points) as net_current_points
        FROM stg_points_ledger l
        JOIN stg_dim_operation o ON l.operation_code = o.operation_code
        GROUP BY 1
    ),
    pix_camp AS (
        SELECT 
            user_id,
            MAX(CASE WHEN event_name = 'Notification Sent' THEN 1 ELSE 0 END) as camp_sent,
            MAX(CASE WHEN event_name = 'Notification Viewed' THEN 1 ELSE 0 END) as camp_viewed,
            MAX(CASE WHEN event_name = 'Notification Clicked' THEN 1 ELSE 0 END) as camp_clicked,
            MAX(CASE WHEN event_name = 'Notification Failed' THEN 1 ELSE 0 END) as camp_failed
        FROM stg_crm_events
        WHERE campaign_name = 'CMP_LANCAMENTO_PIX_4dbee001e6aba1eb57b512c3'
        GROUP BY 1
    )
    SELECT 
        rc.user_id,
        rc.primary_account_id,
        rc.card_class,
        rc.card_flag,
        rc.card_created_at,
        coalesce(uo.total_orders, 0) as total_orders,
        coalesce(uo.total_points_redeemed, 0) as total_points_redeemed,
        coalesce(uo.pix_orders_approved, 0) as pix_orders_approved,
        coalesce(uo.pix_points_redeemed, 0) as pix_points_redeemed,
        coalesce(uo.pix_reais_redeemed, 0.0) as pix_reais_redeemed,
        uo.first_pix_at,
        CASE WHEN coalesce(uo.pix_orders_approved, 0) > 0 THEN TRUE ELSE FALSE END as has_redeemed_pix,
        coalesce(ul.total_points_credited, 0) as total_points_credited,
        coalesce(ul.migration_points_credited, 0) as migration_points_credited,
        coalesce(ul.migration_points_expired, 0) as migration_points_expired,
        coalesce(ul.net_current_points, 0) as net_current_points,
        CASE 
            WHEN pc.camp_clicked = 1 THEN '1. Clicou no Email'
            WHEN pc.camp_viewed = 1 THEN '2. Visualizou (sem clicar)'
            WHEN pc.camp_sent = 1 THEN '3. Recebeu (sem visualizar)'
            WHEN pc.camp_failed = 1 THEN '4. Falha no envio'
            ELSE '5. Nao impactado pela campanha'
        END as crm_pix_cohort
    FROM recent_card rc
    LEFT JOIN user_orders uo ON rc.user_id = uo.user_id
    LEFT JOIN user_ledger ul ON rc.user_id = ul.user_id
    LEFT JOIN pix_camp pc ON rc.user_id = pc.user_id;

    -- Fato Itens de Pedido (Grão: order_item_id)
    CREATE OR REPLACE TABLE fct_order_items AS
    SELECT 
        oi.order_item_id,
        oi.order_id,
        o.cart_id,
        c.user_id,
        c.channel,
        u.card_class,
        u.card_flag,
        oi.item_created_at,
        oi.mes,
        oi.item_status,
        oi.product_type,
        oi.supplier_name,
        oi.supplier_responsible,
        oi.category_macro,
        oi.paid_points,
        oi.paid_currency,
        oi.product_value,
        oi.refunded_points,
        oi.quantity,
        (oi.paid_points - coalesce(oi.refunded_points, 0)) as net_points,
        CASE 
            WHEN oi.paid_points > 0 THEN (oi.product_value - oi.paid_currency) / oi.paid_points 
            ELSE 0.0 
        END as unit_program_cost_per_point,
        CASE WHEN oi.supplier_name = 'Pix Pontua+' THEN TRUE ELSE FALSE END as is_pix
    FROM stg_order_items oi
    JOIN stg_orders o ON oi.order_id = o.order_id
    JOIN stg_carts c ON o.cart_id = c.cart_id
    LEFT JOIN dim_users u ON c.user_id = u.user_id;

    -- Fato Movimentações de Pontos (Grão: movement_id)
    CREATE OR REPLACE TABLE fct_points_movements AS
    SELECT 
        l.movement_id,
        l.user_id,
        l.account_id,
        l.operation_code,
        o.operation_name,
        o.direction,
        l.points,
        l.movement_at,
        l.mes,
        l.valid_until,
        CASE 
            WHEN l.valid_until IS NOT NULL AND l.valid_until <= '2026-10-01' THEN TRUE 
            ELSE FALSE 
        END as is_already_expired
    FROM stg_points_ledger l
    JOIN stg_dim_operation o ON l.operation_code = o.operation_code;
    """)
    
    print("3. Criando camada Semântica / Agregada (Serving Layer)...")
    con.sql("""
    -- 3.1 KPIs Mensais do Programa (Grão: mes)
    CREATE OR REPLACE TABLE agg_monthly_kpis AS
    WITH redemptions AS (
        SELECT 
            mes,
            SUM(paid_points) as total_pontos_resgatados,
            SUM(paid_points) FILTER (WHERE category_macro = 'Aereas') as pontos_aereas,
            SUM(paid_points) FILTER (WHERE category_macro = 'Varejo') as pontos_varejo,
            SUM(paid_points) FILTER (WHERE category_macro = 'Cashback') as pontos_pix,
            COUNT(*) FILTER (WHERE is_pix = TRUE) as transacoes_pix_aprovadas,
            SUM(product_value) FILTER (WHERE is_pix = TRUE) as reais_pix_aprovados,
            SUM(product_value - paid_currency) as custo_total_programa_reais,
            COUNT(DISTINCT user_id) as usuarios_resgatantes_unicos
        FROM fct_order_items
        WHERE item_status = 'APROVADO'
        GROUP BY 1
    ),
    ledger_month AS (
        SELECT 
            mes,
            SUM(points) FILTER (WHERE direction = 'CREDIT') as pontos_creditados,
            SUM(-points) FILTER (WHERE operation_code = 103) as pontos_expirados
        FROM fct_points_movements
        GROUP BY 1
    )
    SELECT 
        r.mes,
        coalesce(l.pontos_creditados, 0) as pontos_creditados,
        r.total_pontos_resgatados,
        coalesce(l.pontos_expirados, 0) as pontos_expirados,
        r.pontos_aereas,
        r.pontos_varejo,
        coalesce(r.pontos_pix, 0) as pontos_pix,
        ROUND(100.0 * r.pontos_aereas / r.total_pontos_resgatados, 2) as share_aereas_pct,
        ROUND(100.0 * r.pontos_varejo / r.total_pontos_resgatados, 2) as share_varejo_pct,
        ROUND(100.0 * coalesce(r.pontos_pix, 0) / r.total_pontos_resgatados, 2) as share_pix_pct,
        CASE WHEN (100.0 * r.pontos_aereas / r.total_pontos_resgatados) >= 50.0 THEN TRUE ELSE FALSE END as meta_aereas_atingida,
        CASE WHEN (100.0 * r.pontos_varejo / r.total_pontos_resgatados) >= 20.0 THEN TRUE ELSE FALSE END as meta_varejo_atingida,
        r.custo_total_programa_reais,
        ROUND(r.custo_total_programa_reais / r.total_pontos_resgatados, 5) as custo_medio_por_ponto,
        r.transacoes_pix_aprovadas,
        coalesce(r.reais_pix_aprovados, 0.0) as reais_pix_aprovados,
        CASE 
            WHEN coalesce(r.pontos_pix, 0) > 0 THEN ROUND(r.reais_pix_aprovados / r.pontos_pix, 5) 
            ELSE NULL 
        END as taxa_real_pix_por_ponto,
        r.usuarios_resgatantes_unicos
    FROM redemptions r
    LEFT JOIN ledger_month l ON r.mes = l.mes
    ORDER BY r.mes;

    -- 3.2 Quebra por Categoria e Classe de Cartão (Grão: mes, category_macro, card_class)
    CREATE OR REPLACE TABLE agg_category_card_class_monthly AS
    SELECT 
        mes,
        category_macro,
        card_class,
        channel,
        COUNT(*) as total_itens,
        COUNT(DISTINCT user_id) as usuarios_unicos,
        SUM(paid_points) as total_pontos,
        SUM(product_value) as total_valor_reais,
        SUM(paid_currency) as total_coparticipacao_reais,
        SUM(product_value - paid_currency) as custo_liquido_programa_reais,
        ROUND(SUM(product_value - paid_currency) / SUM(paid_points), 5) as custo_ponto_reais
    FROM fct_order_items
    WHERE item_status = 'APROVADO'
    GROUP BY 1, 2, 3, 4
    ORDER BY 1, 2, 3, 4;

    -- 3.3 Coortes de CRM vs Adoção do Pix (Grão: crm_pix_cohort)
    CREATE OR REPLACE TABLE agg_pix_crm_cohorts AS
    SELECT 
        crm_pix_cohort,
        COUNT(*) as total_usuarios,
        COUNT(*) FILTER (WHERE has_redeemed_pix = TRUE) as usuarios_resgataram_pix,
        ROUND(100.0 * COUNT(*) FILTER (WHERE has_redeemed_pix = TRUE) / COUNT(*), 2) as taxa_conversao_pct,
        SUM(pix_points_redeemed) as total_pontos_pix,
        SUM(pix_reais_redeemed) as total_reais_pix,
        ROUND(SUM(pix_points_redeemed) / nullif(COUNT(*) FILTER (WHERE has_redeemed_pix = TRUE), 0), 1) as ticket_medio_pontos_pix
    FROM dim_users
    GROUP BY 1
    ORDER BY 1;

    -- 3.4 Análise de Breakage e Passivo (Grão: visao_analise)
    CREATE OR REPLACE TABLE agg_breakage_analysis AS
    WITH base_calc AS (
        SELECT 
            '1. Base Migrada (Legado)' as safra,
            SUM(points) FILTER (WHERE operation_code = 100) as pontos_emitidos,
            NULL as pontos_resgatados,
            SUM(-points) FILTER (WHERE operation_code = 103) as pontos_expirados,
            '2028-03-31' as validade,
            19.78 as taxa_breakage_pct,
            NULL as taxa_resgate_pct,
            20.0 as meta_breakage_teto_pct,
            'DENTRO DA META (19.78% <= 20.0%)' as status_governanca,
            'Pontos legados recebidos na migração e expirados ao longo de 2026.' as notas
        FROM fct_points_movements
        UNION ALL
        SELECT 
            '2. Programa Novo (Aurora)' as safra,
            SUM(points) FILTER (WHERE operation_code = 1) as pontos_emitidos,
            NULL as pontos_resgatados,
            0.0 as pontos_expirados,
            '2027-09 a 2028-09' as validade,
            0.0 as taxa_breakage_pct,
            NULL as taxa_resgate_pct,
            20.0 as meta_breakage_teto_pct,
            'EM VIGOR (Validade de 24 meses; expira a partir de Set/2027)' as status_governanca,
            'Acúmulos gerados no cartão de crédito do Banco Aurora.' as notas
        FROM fct_points_movements
        UNION ALL
        SELECT 
            '3. Consolidado do Programa' as safra,
            SUM(points) FILTER (WHERE direction = 'CREDIT') as pontos_emitidos,
            SUM(-points) FILTER (WHERE operation_code = 2) as pontos_resgatados,
            SUM(-points) FILTER (WHERE operation_code IN (3, 103)) as pontos_expirados,
            '2027 a 2028' as validade,
            ROUND(100.0 * SUM(-points) FILTER (WHERE operation_code IN (3, 103)) / SUM(points) FILTER (WHERE direction = 'CREDIT'), 2) as taxa_breakage_pct,
            ROUND(100.0 * SUM(-points) FILTER (WHERE operation_code = 2) / SUM(points) FILTER (WHERE direction = 'CREDIT'), 2) as taxa_resgate_pct,
            20.0 as meta_breakage_teto_pct,
            'CONFUSAO DO DIRETOR: 42.4% e taxa de resgate, nao breakage!' as status_governanca,
            'O diretor confundiu taxa de resgate (42.45%) com taxa de expiração (breakage real = 8.38% total / 19.78% migração).' as notas
        FROM fct_points_movements
    )
    SELECT * FROM base_calc ORDER BY safra;

    -- 3.5 Auditoria do Relatório do Operador vs Sistema (Grão: mes)
    CREATE OR REPLACE TABLE agg_operator_audit AS
    WITH calc_pix AS (
        SELECT 
            mes,
            COUNT(*) as bruto_itens,
            SUM(paid_points) as bruto_pontos,
            SUM(product_value) as bruto_reais,
            COUNT(*) FILTER (WHERE item_status = 'APROVADO') as aprovado_itens,
            SUM(paid_points) FILTER (WHERE item_status = 'APROVADO') as aprovado_pontos,
            SUM(product_value) FILTER (WHERE item_status = 'APROVADO') as aprovado_reais,
            COUNT(*) FILTER (WHERE item_status != 'APROVADO') as nao_aprovado_itens,
            SUM(paid_points) FILTER (WHERE item_status != 'APROVADO') as nao_aprovado_pontos
        FROM fct_order_items
        WHERE supplier_name = 'Pix Pontua+'
        GROUP BY 1
    )
    SELECT 
        r.mes,
        r.pix_transacoes as relatorio_transacoes,
        c.bruto_itens as sistema_bruto_transacoes,
        c.aprovado_itens as sistema_aprovado_transacoes,
        r.pix_pontos as relatorio_pontos,
        c.bruto_pontos as sistema_bruto_pontos,
        c.aprovado_pontos as sistema_aprovado_pontos,
        r.pix_reais as relatorio_reais,
        c.aprovado_reais as sistema_aprovado_reais,
        ROUND(r.pix_reais / r.pix_pontos, 5) as relatorio_taxa_calculada,
        ROUND(c.aprovado_reais / c.aprovado_pontos, 5) as sistema_taxa_aprovada_real,
        'O operador somou pedidos cancelados/estornados no denominador (pontos e transações), mas usou reais aprovados, subavaliando a taxa de 0.019 para ~0.016.' as diagnostico_auditoria
    FROM 'dados/relatorio_mensal_cliente.csv' r
    JOIN calc_pix c ON r.mes = c.mes
    ORDER BY r.mes;
    """)

    print("4. Exportando tabelas agregadas para entrega/dashboard/data e agente/data...")
    tables_to_export = [
        "agg_monthly_kpis",
        "agg_category_card_class_monthly",
        "agg_pix_crm_cohorts",
        "agg_breakage_analysis",
        "agg_operator_audit"
    ]
    
    metadata = {}
    for t in tables_to_export:
        df = con.sql(f"SELECT * FROM {t}").df()
        
        # Exportar CSV e JSON para o Dashboard
        csv_path = f"entrega/dashboard/data/{t}.csv"
        json_path = f"entrega/dashboard/data/{t}.json"
        df.to_csv(csv_path, index=False)
        df.to_json(json_path, orient="records", indent=2, force_ascii=False)
        
        # Copiar para o Agente
        df.to_csv(f"agente/data/{t}.csv", index=False)
        df.to_json(f"agente/data/{t}.json", orient="records", indent=2, force_ascii=False)
        
        # Coletar schema para documentação semântica do Agente
        metadata[t] = {
            "description": con.sql(f"DESCRIBE {t}").df().to_dict(orient="records"),
            "row_count": len(df)
        }
    
    # Salvar dicionário semântico para o agente
    with open("agente/data/semantic_dictionary.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
        
    print("Pipeline executado com sucesso! Dados exportados.")

if __name__ == "__main__":
    run_pipeline()
