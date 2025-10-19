import os, uuid, random, datetime, io, sys, time
from faker import Faker
import psycopg2

ROWS = int(os.getenv("ROWS", "500000"))
fake = Faker()

def gen_rows(n):
    products = [f"p{i}" for i in range(1, 400)]  # 399 products
    for _ in range(n):
        tid = str(uuid.uuid4())
        uid = f"user_{random.randint(1,80000)}"
        pid = random.choice(products)
        qty = random.randint(1,5)
        unit = round(random.uniform(5, 200), 2)
        total = round(qty * unit, 2)
        status = random.choices(["completed","refunded","cancelled"], [0.95,0.03,0.02])[0]
        created = fake.date_time_between(start_date='-365d', end_date='now')
        yield f"{tid},{uid},{pid},{qty},{unit},{total},USD,{status},{created:%Y-%m-%d %H:%M:%S}\n"

def wait_pg(conn_str, retries=60):
    for i in range(retries):
        try:
            conn = psycopg2.connect(conn_str)
            conn.close()
            return
        except Exception as e:
            time.sleep(2)
    raise RuntimeError("Postgres not reachable")

if __name__ == "__main__":
    conn_str = "dbname=%s user=%s password=%s host=%s port=%s" % (
        os.getenv("PGDATABASE"), os.getenv("PGUSER"), os.getenv("PGPASSWORD"),
        os.getenv("PGHOST"), os.getenv("PGPORT", "5432")
    )
    print("Waiting for Postgres...")
    wait_pg(conn_str)
    print("Generating CSV in-memory…", flush=True) 
    buf = io.StringIO()
    buf.write("transaction_id,user_id,product_id,quantity,unit_price,total_amount,currency,status,created_at\n")
    for line in gen_rows(ROWS):
        buf.write(line)
    buf.seek(0)

    print(f"Loading {ROWS:,} rows with COPY…", flush=True)
    conn = psycopg2.connect(conn_str)
    cur = conn.cursor()
    cur.copy_expert("""
        COPY transactions(transaction_id,user_id,product_id,quantity,unit_price,total_amount,currency,status,created_at)
        FROM STDIN WITH (FORMAT CSV, HEADER TRUE)
    """, buf)
    conn.commit()
    cur.close(); conn.close()
    print("Load complete ✓", flush=True)
