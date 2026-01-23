SELECT   
  EXTRACT(YEAR FROM I.created_at) AS year,
  P.category,
  P.brand,
  U.state,
  SUM(I.sale_price) AS CA,
  SUM(I.sale_price - P.cost) AS Margin

 FROM 'bigquery-public-data.thelook_ecommerce.orders' AS O
  LEFT JOIN 'bigquery-public-data.thelook_ecommerce.order_items' AS I
  ON O.order_id = I.order_id
  LEFT JOIN 'bigquery-public-data.thelook_ecommerce.products' AS P
  ON P.id = I.product_id
  LEFT JOIN 'bigquery-public-data.thelook_ecommerce.users' AS U
  ON U.id = O.user_id

  WHERE U.country = 'France'
  AND P.department = 'Women'
  AND O.status ='Complete'
  AND DATE(I.created_at) BETWEEN '2023-01-01' AND '2024-12-31'

  GROUP BY year, P.category, P.brand,U.state
  ORDER BY year, P.category, P.brand,U.state

  