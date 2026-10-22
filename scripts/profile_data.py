import duckdb

con = duckdb.connect()

print("--- 1. CARDS ---")
con.sql("""
SELECT 
    COUNT(*) as total_rows,
    COUNT(DISTINCT account_id) as distinct_accounts,
    COUNT(DISTINCT user_id) as distinct_users,
    COUNT(*) FILTER (WHERE is_most_recent = true) as most_recent_true,
    COUNT(*) FILTER (WHERE is_most_recent = false) as most_recent_false,
    MIN(created_at) as min_created,
    MAX(created_at) as max_created
FROM 'dados/cards.csv'
""").show()

con.sql("""
SELECT card_class, card_flag, COUNT(*) as cnt
FROM 'dados/cards.csv'
GROUP BY 1, 2
ORDER BY 1, 2
""").show()

print("--- 2. CARTS & ORDERS ---")
con.sql("""
SELECT 
    COUNT(*) as total_carts,
    COUNT(DISTINCT cart_id) as distinct_carts,
    COUNT(DISTINCT user_id) as distinct_users,
    COUNT(*) FILTER (WHERE user_id IS NULL) as null_users
FROM 'dados/carts.csv'
""").show()

con.sql("""
SELECT channel, COUNT(*) as cnt
FROM 'dados/carts.csv'
GROUP BY 1
""").show()

con.sql("""
SELECT 
    COUNT(*) as total_orders,
    COUNT(DISTINCT order_id) as distinct_orders,
    COUNT(DISTINCT cart_id) as distinct_carts,
    COUNT(DISTINCT user_id) as distinct_users,
    COUNT(*) FILTER (WHERE user_id IS NULL) as null_users,
    status,
    COUNT(*) as cnt,
    MIN(created_at) as min_created,
    MAX(created_at) as max_created
FROM 'dados/orders.csv'
GROUP BY status
""").show()

print("--- 3. ORDER ITEMS & PRODUCT TYPES ---")
con.sql("""
SELECT 
    COUNT(*) as total_items,
    COUNT(DISTINCT order_item_id) as distinct_items,
    COUNT(DISTINCT order_id) as distinct_orders,
    product_type,
    category_macro,
    status,
    COUNT(*) as cnt,
    SUM(paid_points) as sum_paid_points,
    SUM(paid_currency) as sum_paid_currency,
    SUM(product_value) as sum_product_value,
    SUM(refunded_points) as sum_refunded_points
FROM 'dados/order_items.csv'
GROUP BY product_type, category_macro, status
ORDER BY product_type, category_macro, status
""").show(max_rows=50)

print("--- 4. REDEEMED POINTS ---")
con.sql("""
SELECT 
    COUNT(*) as total_rows,
    COUNT(DISTINCT order_item_id) as distinct_items,
    COUNT(DISTINCT account_id) as distinct_accounts,
    movement_type,
    COUNT(*) as cnt,
    SUM(points) as sum_points,
    MIN(points) as min_points,
    MAX(points) as max_points
FROM 'dados/redeemed_points.csv'
GROUP BY movement_type
""").show()

print("--- 5. POINTS LEDGER & OPERATIONS ---")
con.sql("""
SELECT 
    l.operation_code,
    o.operation_name,
    o.direction,
    COUNT(*) as movements,
    COUNT(DISTINCT l.user_id) as distinct_users,
    COUNT(DISTINCT l.account_id) as distinct_accounts,
    SUM(l.points) as sum_points,
    MIN(l.movement_at) as min_date,
    MAX(l.movement_at) as max_date
FROM 'dados/points_ledger.csv' l
LEFT JOIN 'dados/dim_operation.csv' o ON l.operation_code = o.operation_code
GROUP BY 1, 2, 3
ORDER BY 1
""").show()

print("--- 6. CRM EVENTS ---")
con.sql("""
SELECT 
    event_name,
    campaign_type,
    control_group,
    COUNT(*) as cnt,
    COUNT(DISTINCT user_id) as distinct_users,
    MIN(event_ts) as min_ts,
    MAX(event_ts) as max_ts
FROM 'dados/crm_events.csv'
GROUP BY 1, 2, 3
ORDER BY 1, 2, 3
""").show(max_rows=50)
