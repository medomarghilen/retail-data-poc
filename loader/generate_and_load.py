import os, uuid, random, io, time
from faker import Faker
import psycopg2

# Number of rows to generate
ROWS = int(os.getenv("ROWS", "500000"))
fake = Faker()

def wait_for_postgres(conn_str):
    """Wait until Postgres is ready."""
    for _ in range(30):
        try:
            conn = psycopg2.connect(conn_str)
            conn.close()
            print("✅ Postgres is ready.")
            return
        except Exception:
            print("⏳ Waiting for Postgres...")
            time.sleep(2)
    raise Exception("Postgres not reachable")

def table_has_data(conn_str):
    """Return True if transactions table already has data."""
    conn = psycopg2.connect(conn_str)
    cur = conn.cursor()
    cur.execute("SELECT to_regclass('public.transactions');")
    exists = cur.fetchone()[0] is not None

    if exists:
        cur.execute("SELECT COUNT(*) FROM public.transactions;")
        count = cur.fetchone()[0]
        conn.close()
        if count > 0:
            print(f"⚠️ Table already has {count} rows — skipping generation.")
            return True
    conn.close()
    return False

def generate_rows(n):
    """Generate fake transaction rows."""
    products = [f"p{i}" for i in range(1, 400)]
    for _ in range(n):
        yield f"{uuid.uuid4()},user_{random.randint(1,80000)},{random.choice(products)}," \
              f"{random.randint(1,5)},{random.uniform(5,200):.2f}," \
              f"{random.uniform(5,200)*random.randint(1,5):.2f},USD," \
              f"{random.choice(['completed','refunded','cancelled'])}," \
              f"{fake.date_time_between(start_date='-365d', end_date='now'):%Y-%m-%d %H:%M:%S}\n"

if __name__ == "__main__":
    conn_str = "dbname=%s user=%s password=%s host=%s port=%s" % (
        os.getenv("PGDATABASE"), os.getenv("PGUSER"), os.getenv("PGPASSWORD"),
        os.getenv("PGHOST"), os.getenv("PGPORT", "5432")
    )

    wait_for_postgres(conn_str)

    if table_has_data(conn_str):
        print("✅ Data already exists. Nothing to do.")
        exit(0)

    print("🧠 Generating data in memory...")
    buf = io.StringIO()
    buf.write("transaction_id,user_id,product_id,quantity,unit_price,total_amount,currency,status,created_at\n")
    for line in generate_rows(ROWS):
        buf.write(line)
    buf.seek(0)

    print(f"🚀 Loading {ROWS:,} rows into Postgres...")
    conn = psycopg2.connect(conn_str)
    cur = conn.cursor()
    cur.copy_expert("""
        COPY transactions(transaction_id,user_id,product_id,quantity,unit_price,total_amount,currency,status,created_at)
        FROM STDIN WITH (FORMAT CSV, HEADER TRUE)
    """, buf)
    conn.commit()
    cur.close()
    conn.close()
    print("✅ Load complete ✓")
