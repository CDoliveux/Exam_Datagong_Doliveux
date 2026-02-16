SELECT
  EXTRACT(YEAR FROM I.created_at) AS year,
  category,
  COUNTIF(I.status IN ('Returned')) AS returned_items, -- compte toutes les lignes avec statut "Returned"
  COUNTIF(I.status IN ('Returned','Complete')) AS total_items,--compte toutes les lignes avec statut "Returned" + "Complete"
  ROUND(COUNTIF(I.status = 'Returned') / NULLIF(COUNTIF(I.status IN ('Returned','Complete')),0) * 100, 2) AS tx_retour_pourcent
  
  FROM `bigquery-public-data.thelook_ecommerce.orders` AS O --on reprend les mêmes tables / filres que pour ma_table_2 (reconsitution du CSV)
  LEFT JOIN `bigquery-public-data.thelook_ecommerce.order_items` AS I
  ON O.order_id = I.order_id
  LEFT JOIN `bigquery-public-data.thelook_ecommerce.products` AS P
  ON P.id = I.product_id
  LEFT JOIN `bigquery-public-data.thelook_ecommerce.users` AS U
  ON U.id = O.user_id
  WHERE U.country = 'France'
  AND P.department = 'Women'
  AND DATE(I.created_at) BETWEEN '2023-01-01' AND '2024-12-31'
   
GROUP BY year, category
ORDER BY  year, category