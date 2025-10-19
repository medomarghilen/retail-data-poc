
  
    

  create  table "demo".analytics_staging."stg_transactions__dbt_tmp"
  
  
    as
  
  (
    

SELECT
    transaction_id AS order_id,
    user_id,
    product_id,
    quantity,
    unit_price,
    total_amount,
    currency,
    status,
    created_at AS order_date
FROM public.transactions
  );
  