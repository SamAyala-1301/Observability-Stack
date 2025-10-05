from flask import Flask, jsonify
import time, psycopg2, os
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)   # 🚀 auto /metrics endpoint on port 5000

DB_URL = "postgresql://postgres:postgres@postgres_db:5432/postgres"

@app.route("/health")
def health():
    raise Exception("Simulated error")

@app.route("/transactions")
def transactions():
    start = time.time()
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM transactions;")
        count = cur.fetchone()[0]
        cur.close()
        conn.close()
        latency = time.time() - start
        return jsonify(transaction_count=count, latency=latency)
    except Exception as e:
        return jsonify(error=str(e)), 500
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)