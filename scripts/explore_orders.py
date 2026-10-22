import duckdb

con = duckdb.connect()

print("--- DISTINCT PRODUCT TYPES & CATEGORY MACRO ---")
con.sql("""
SELECT 
    product_type,
    category_macro,
    status,
    COUNT(*) as items_cnt,
    SUM(paid_points) as sum_paid_points,
    SUM(paid_currency) as sum_paid_currency,
    SUM(product_value) as sum_product_value,
    SUM(refunded_points) as sum_refunded_points
FROM 'dados/order_items.csv'
GROUP BY 1, 2, 3
ORDER BY 1, 2, 3
""").show(max_rows=100)

print("--- ORDERS STATUSES ---")
con.sql("""
SELECT status, COUNT(*) 
FROM 'dados/orders.csv' 
GROUP BY 1
""").show()

print("--- ORDERS vs ORDER_ITEMS STATUS MATCH ---")
con.sql("""
SELECT 
    o.status as order_status,
    i.status as item_status,
    COUNT(*) as cnt
FROM 'dados/orders.csv' o
JOIN 'dados/order_items.csv' i ON o.order_id = i.order_id
GROUP BY 1, 2
ORDER BY 1, 2
""").show()
