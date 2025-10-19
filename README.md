# Retail Data POC (Postgres + dbt + Flask)

## What it does
- Generates **500k** fake e-commerce transactions
- Loads into **Postgres**
- Transforms with **dbt** (`staging` → `analytics_analytics.fact_orders`)
- Exposes KPIs via **Flask API**

## Run
```bash
docker-compose up --build
