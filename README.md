# 🚀 Observability Stack — End-to-End Monitoring & Self-Healing Demo

A complete containerized observability demo showing **how modern production systems monitor, alert, and auto-heal**.  
This stack combines **Flask + PostgreSQL + Prometheus + Grafana + Alertmanager + a Python Alert Bot** — all orchestrated with Docker Compose.

---

## 🌍 Overview

This project simulates a **real-world production environment** with:
- A web API (Flask)
- A database (PostgreSQL)
- A background worker
- Metrics collection (Prometheus)
- System & endpoint exporters
- Visualization (Grafana)
- Alerting (Alertmanager)
- Automated remediation (Python alert bot)

Together they form a **complete observability pipeline**:
> Metrics ➜ Dashboards ➜ Alerts ➜ Auto-actions

---

## 🧩 Why these components?

| Component | Role | Why Chosen |
|------------|------|------------|
| **Docker & Compose** | Orchestrates all containers. | Reproducible, realistic multi-service setup. |
| **Flask (API)** | Serves `/health`, `/transactions`, `/metrics`. | Lightweight, easy to instrument. |
| **PostgreSQL** | Transaction store for API + worker. | Common production DB, demonstrates real load. |
| **Worker (Python)** | Simulates background batch inserts. | Mimics cron / async jobs in production. |
| **Prometheus** | Scrapes & stores metrics. | Industry standard for metrics monitoring. |
| **Node Exporter** | Exposes host CPU/memory metrics. | System-level observability. |
| **Blackbox Exporter** | Probes API endpoints externally. | Simulates uptime checks. |
| **Grafana** | Dashboards & visualization. | Friendly, flexible front-end for metrics. |
| **Alertmanager** | Routes alerts from Prometheus. | Notification management (Slack/email/webhook). |
| **Alert Bot (Python)** | Receives webhooks, performs auto-remediation. | Demonstrates self-healing automation. |

---

## 🧠 Architecture

 ┌─────────────┐
 │ Flask  API  │──┐
 └──────┬──────┘  │ exposes /metrics
        │          │
 ┌──────▼──────┐   │
 │ PostgreSQL  │<──┘  (store transactions)
 └──────┬──────┘
        │
 ┌──────▼──────┐
 │  Worker     │ (batch inserts)
 └──────┬──────┘
        │ metrics
 ┌──────▼─────────────┐
 │    Prometheus      │  ← scrapes exporters
 └──────┬─────────────┘
        │ alerts
 ┌──────▼─────────────┐
 │   Alertmanager     │  → Slack / Alert Bot
 └──────┬─────────────┘
        │
 ┌──────▼──────┐
 │ Alert Bot   │  (restart/scale/log)
 └─────────────┘
        ↓
   Grafana  ←  visualizes everything

   ---

## ⚙️ Folder Structure

Observability-Stack/
├─ api/
│  ├─ app.py
│  ├─ requirements.txt
│  └─ Dockerfile
├─ worker/
│  ├─ worker.py
│  ├─ requirements.txt
│  └─ Dockerfile
├─ alert_bot/
│  ├─ alert_bot.py
│  ├─ requirements.txt
│  └─ Dockerfile
├─ prometheus/
│  ├─ prometheus.yml
│  └─ alert.rules.yml
├─ alertmanager/
│  └─ config.yml
├─ db/
│  └─ init.sql
├─ docker-compose.yml
└─ README.md

---

## 🏃‍♂️ Quick Start

1. **Clone & enter**
   ```bash
   git clone https://github.com/yourname/observability-stack.git
   cd observability-stack
2. **Copy Example env**
   cp .env.example .env

# Fill Slack webhook or email creds (optional)

3. **Run Everything**
    docker compose up -d --build

4. **Check Services**
    Service  -- URL
    Flask API
    http://localhost:8000/health
    Prometheus
    http://localhost:9090
    Grafana
    http://localhost:3000 (admin / admin)
    Alertmanager
    http://localhost:9093

5. **Generating Traffic**
    for i in {1..20}; do curl -s http://localhost:8000/health > /dev/null; sleep 1; done (In your terminal / CLI)

📊 Dashboards & Metrics
	•	API latency (p95) → histogram_quantile(0.95, sum(rate(flask_http_request_duration_seconds_bucket[5m])) by (le))
	•	Error rate → rate(flask_http_request_exceptions_total[5m])
	•	System CPU / Memory → from Node Exporter.
	•	Uptime probe → probe_success from Blackbox Exporter.

⸻

🚨 Alerting Rules
    Alert -- Trigger -- Action

    APIHighLatency -- p95 latency > 200 ms for 1 m -- Slack + Alert Bot
    APIErrorRateHigh -- error rate > 5 % for 5 m -- lack + Alert Bot

🤖 Automation (Alert Bot)

When Alertmanager sends a webhook:
	•	Parses alert labels.
	•	Runs actions:
	•	docker restart flask_api
	•	docker compose up --scale worker=3
	•	Logs the event into incident_log.jsonl.

You can simulate manually:
    curl -XPOST -H "Content-Type: application/json" \
    -d '{"alerts":[{"labels":{"alertname":"APIHighLatency","severity":"critical"}}]}' \
    -- > http://localhost:5001/alert

🔍 Simulating Production
	•	Multiple services: API, DB, worker mimic microservices.
	•	Database I/O: worker generates realistic DB load.
	•	Exporters: monitor system + external health like real production.
	•	Alerting + Auto-Remediation: shows a complete observability → alert → action loop.
	•	Docker Compose network: replicates production service discovery.

⸻

🔐 Best Practices
    Area -- Good Practice
    Secrets -- Never commit .env with real keys.
    Grafana -- Change default admin password.
    Alert Bot -- Don’t mount /var/run/docker.sock in prod.
    Metrics -- Avoid high-cardinality labels.
    Alerts -- Use for: to prevent flapping; group similar alerts.

🧰 Troubleshooting
    Issue -- Likely Cause --Fix
Mount error for prometheus.yml -- Wrong host path / spaces in folder name -- Remove spaces, verify file path.
API down in Prometheus -- Service name mismatch -- Ensure api in docker-compose matches Prometheus target.
Worker fails to connect DB -- DB not yet ready -- Healthcheck + retry loop.
“No alert groups found” -- No active alerts -- Trigger latency/error manually.

🏁 Clean Up
    docker compose down -v
    docker system prune -af --volumes

