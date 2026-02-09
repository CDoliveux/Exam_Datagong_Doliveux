SELECT 
    O.order_id,
    I.id AS order_item_id,
    I.product_id,
    I.created_at AS item_created_at,
    I.status AS item_status,
    I.sale_price,
    P.cost,
    P.category,
    P.department,
    P.brand,
    P.name AS product_name,
    O.status AS order_status,
    O.created_at AS order_created_at,
    O.shipped_at,
    O.delivered_at,
    O.user_id,
    U.gender,
    U.country,
    U.state,
    U.city
FROM 'bigquery-public-data.thelook_ecommerce.orders' AS O
LEFT JOIN 'bigquery-public-data.thelook_ecommerce.order_items' AS I
    ON O.order_id = I.order_id
LEFT JOIN 'bigquery-public-data.thelook_ecommerce.products' AS P
    ON P.id = I.product_id
LEFT JOIN 'bigquery-public-data.thelook_ecommerce.users' AS U
    ON U.id = O.user_id
WHERE U.country = 'France'
    AND P.department = 'Women'
    AND DATE(I.created_at) BETWEEN '2023-01-01' AND '2024-12-31'

ORDER BY
    I.created_at,
    O.order_id,
    I.id;