SELECT
  year,
  category,
  AVG(order_total) AS Panier_Moyen
  
  FROM (
    SELECT
      EXTRACT(YEAR FROM item_created_at) AS year,
      category,
      order_id,
     SUM(sale_price) AS order_total
    FROM `dataset.ma_table_2`
    WHERE order_status = 'Complete' 
    GROUP BY year, category, order_id
    ) AS subquery

WHERE order_total > 0 
GROUP BY year, category
ORDER BY year, category