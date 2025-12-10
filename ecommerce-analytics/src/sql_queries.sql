-- Vendas mensais
SELECT strftime('%Y-%m', order_date) AS ym, SUM(revenue) AS monthly_revenue
FROM orders
GROUP BY ym
ORDER BY ym;

-- Top 10 produtos por receita
SELECT product_id, product_name, SUM(revenue) AS total_revenue
FROM orders
GROUP BY product_id, product_name
ORDER BY total_revenue DESC
LIMIT 10;

-- Cohort simplificado: usuários com primeiro pedido e retenção 30 dias
WITH first_order AS (
  SELECT user_id, MIN(date(order_date)) AS cohort_date
  FROM orders
  GROUP BY user_id
)
SELECT f.cohort_date, COUNT(DISTINCT o.user_id) AS retained_30d
FROM first_order f
JOIN orders o ON o.user_id = f.user_id
WHERE date(o.order_date) BETWEEN date(f.cohort_date) AND date(f.cohort_date, '+30 days')
GROUP BY f.cohort_date
ORDER BY f.cohort_date;
