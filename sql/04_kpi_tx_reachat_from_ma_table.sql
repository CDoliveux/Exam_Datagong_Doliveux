WITH commandes_complete AS ( -- creation de la CTE qui regroupe juste les commandes complete par user
  SELECT
    EXTRACT(YEAR FROM item_created_at) AS year,
    user_id,
    order_id
  FROM `dataset.ma_table`
  WHERE order_status = 'Complete'),

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