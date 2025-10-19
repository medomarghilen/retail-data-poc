

SELECT
    user_id,
    status,
    COUNT(order_id) AS total_orders,
    SUM(total_amount) AS total_spent,
    MIN(order_date) AS first_order_date,
    MAX(order_date) AS last_order_date
FROM "demo".analytics_staging."stg_transactions"
WHERE status = 'completed'
GROUP BY user_id, status