
SELECT
  EXTRACT(YEAR FROM item_created_at) AS year,
  category,
  brand,
  state,
  SUM(sale_price) AS CA,
  SUM(sale_price - cost) AS Margin
FROM `dataset.ma_table`


WHERE order_status = 'Complete'
GROUP BY year, category, brand, state
ORDER BY year, category, brand, state