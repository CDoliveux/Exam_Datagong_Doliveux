SELECT
  EXTRACT(YEAR FROM item_created_at) AS year,
  category,
  COUNTIF(item_status IN ('Returned')) AS returned_items,
  COUNTIF(item_status IN ('Returned','Complete')) AS total_items,
  ROUND(COUNTIF(item_status = 'Returned') / NULLIF(COUNTIF(item_status IN ('Returned','Complete')),0) * 100, 2) AS tx_retour_pourcent
  
  FROM  `dataset.ma_table`
   
GROUP BY year, category
ORDER BY  year, category