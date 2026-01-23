SELECT
  year,
  category,
  AVG(order_total) AS Panier_Moyen
FROM (
  SELECT
    O.order_id,
    EXTRACT(YEAR FROM I.created_at) AS year,
    P.category,
    SUM(I.sale_price) AS order_total
  FROM `bigquery-public-data.thelook_ecommerce.orders` AS O
  LEFT JOIN `bigquery-public-data.thelook_ecommerce.order_items` AS I
    ON O.order_id = I.order_id
  LEFT JOIN `bigquery-public-data.thelook_ecommerce.products` AS P
    ON P.id = I.product_id
  LEFT JOIN `bigquery-public-data.thelook_ecommerce.users` AS U
  ON U.id = O.user_id
  
  WHERE O.status = 'Complete'
  AND U.country = 'France'
  AND P.department = 'Women'
  AND O.status ='Complete'
  AND DATE(I.created_at) BETWEEN '2023-01-01' AND '2024-12-31'
  GROUP BY O.order_id, year, P.category
)
 
GROUP BY year, category
ORDER BY year, category