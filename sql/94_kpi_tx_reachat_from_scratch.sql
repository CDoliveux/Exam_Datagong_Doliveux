WITH commandes_complete AS ( -- creation de la CTE qui regroupe juste les commandes complete par user
  SELECT
    EXTRACT(YEAR FROM I.created_at) AS year,
    O.user_id,
    O.order_id
  FROM `bigquery-public-data.thelook_ecommerce.orders` AS O
  LEFT JOIN `bigquery-public-data.thelook_ecommerce.order_items` AS I
  ON O.order_id = I.order_id
  LEFT JOIN `bigquery-public-data.thelook_ecommerce.products` AS P
  ON P.id = I.product_id
  LEFT JOIN `bigquery-public-data.thelook_ecommerce.users` AS U
  ON U.id = O.user_id
  WHERE U.country = 'France'
  AND P.department = 'Women'
  AND O.status ='Complete'
  AND DATE(I.created_at) BETWEEN '2023-01-01' AND '2024-12-31'
  AND O.status = 'Complete'),

commandes_par_client AS ( -- creation de la CTE qui compte le nombre de commandes par user_id (donc pasr client)
  SELECT
    year,
    user_id,
    COUNT(DISTINCT order_id) AS nb_commandes
  FROM commandes_complete
  GROUP BY year, user_id
)

SELECT
  year,
  SAFE_DIVIDE(
    COUNTIF(nb_commandes >= 2),   -- Clients ré-acheteurs
    COUNT(*)                      -- Total clients
  ) AS tx_reachat
FROM commandes_par_client
GROUP BY year