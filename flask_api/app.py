import os
from flask import Flask, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://demo:demo@postgres:5432/demo")

# --- Helper function for queries ---
def q(sql, params=None):
    print(f"[DEBUG] Executing SQL:\n{sql}\nWith params: {params}")
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute(sql, params or ())
        rows = cur.fetchall() if cur.description else []
        conn.commit()
        print(f"[DEBUG] Query returned {len(rows)} rows")
        return rows
    except Exception as e:
        print(f"[ERROR] Database error: {e}")
        raise
    finally:
        cur.close()
        conn.close()

# --- Flask app setup ---
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Flask API for Retail POC is running."

@app.get("/health")
def health():
    try:
        q("SELECT 1;")
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}, 500


# 🔹 Get total completed orders for a user
@app.get("/api/users/<user_id>/orders_count")
def orders_count(user_id):
    try:
        rows = q("""
            SELECT total_orders AS orders_count
            FROM analytics_analytics.fact_orders
            WHERE user_id = %s AND status = 'completed';
        """, (user_id,))
        print(f"[DEBUG] Orders count result: {rows}")
        return rows[0] if rows else {"orders_count": 0}
    except Exception as e:
        print(f"[ERROR] orders_count failed: {e}")
        return {"error": str(e)}, 500


# 🔹 Summary of total_spent + first/last order
@app.get("/api/users/<user_id>/summary")
def user_summary(user_id):
    try:
        rows = q("""
            SELECT
                total_orders,
                total_spent,
                first_order_date,
                last_order_date
            FROM analytics_analytics.fact_orders
            WHERE user_id = %s AND status = 'completed';
        """, (user_id,))
        print(f"[DEBUG] User summary result: {rows}")
        return rows[0] if rows else {}
    except Exception as e:
        print(f"[ERROR] user_summary failed: {e}")
        return {"error": str(e)}, 500


# 🔹 Revenue by month (based on first_order_date)
@app.get("/api/sales/by_month")
def sales_by_month():
    try:
        rows = q("""
            SELECT
                DATE_TRUNC('month', first_order_date)::date AS month,
                SUM(total_spent) AS revenue
            FROM analytics_analytics.fact_orders
            WHERE status = 'completed'
            GROUP BY 1
            ORDER BY 1;
        """)
        print(f"[DEBUG] Sales by month result: {rows[:3]} ...")
        return rows
    except Exception as e:
        print(f"[ERROR] sales_by_month failed: {e}")
        return {"error": str(e)}, 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
