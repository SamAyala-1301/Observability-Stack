# worker.py - original
import time
import random
import psycopg2
import os

DB_URL = os.environ.get("DATABASE_URL", "postgresql://admin:admin@postgres_db:5432/transactions")

def wait_for_db():
    for i in range(10):
        try:
            conn = psycopg2.connect(DB_URL)
            conn.close()
            return
        except psycopg2.OperationalError:
            time.sleep(3)
    raise Exception("Database not ready")

def insert_txn():
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id SERIAL PRIMARY KEY,
            amount DECIMAL(10,2),
            status VARCHAR(20),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    amount = round(random.uniform(10, 500), 2)
    status = random.choice(["success", "failed"])
    cur.execute("INSERT INTO transactions (amount, status) VALUES (%s, %s);", (amount, status))
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    wait_for_db()
    while True:
        insert_txn()
        time.sleep(random.randint(3, 7))