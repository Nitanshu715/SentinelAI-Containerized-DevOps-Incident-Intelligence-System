<div align="center">

```
███████╗███████╗███╗   ██╗████████╗██╗███╗   ██╗███████╗██╗      █████╗ ██╗
██╔════╝██╔════╝████╗  ██║╚══██╔══╝██║████╗  ██║██╔════╝██║     ██╔══██╗██║
███████╗█████╗  ██╔██╗ ██║   ██║   ██║██╔██╗ ██║█████╗  ██║     ███████║██║
╚════██║██╔══╝  ██║╚██╗██║   ██║   ██║██║╚██╗██║██╔══╝  ██║     ██╔══██║██║
███████║███████╗██║ ╚████║   ██║   ██║██║ ╚████║███████╗███████╗██║  ██║██║
╚══════╝╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝╚═╝  ╚═╝╚═╝
```

### **Autonomous DevOps Incident Intelligence & Telemetry Anomaly Detection Platform**

[![Docker](https://img.shields.io/badge/Docker-24.0+-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Docker Compose](https://img.shields.io/badge/Docker_Compose-v2-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docs.docker.com/compose/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.135.1-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-1.8.0-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-3.4-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

<br/>

[Explore Architecture](#-system-architecture) •
[Interactive Dashboard](#-modern-web-ui-dashboard) •
[AI Anomaly Engine](#-ai-anomaly-detection-engine) •
[Docker Implementation](#-container-infrastructure--docker-compose) •
[Macvlan & Ipvlan](#-networking--macvlan--ipvlan-deep-dive) •
[Quickstart](#-quickstart-guide) •
[Free Cloud Deployment](#-100-free-cloud-deployment)

</div>

---

## 🌟 Executive Overview

**SentinelAI** is an enterprise-grade, containerized DevOps telemetry and incident intelligence platform. In modern distributed cloud infrastructures, SRE and DevOps engineering teams are inundated with thousands of raw alerts, service degradations, and transient connection timeouts. Identifying which outages represent true statistical anomalies vs. routine background noise is critical to reducing **Mean Time to Detection (MTTD)** and **Mean Time to Resolution (MTTR)**.

SentinelAI provides:
1. **High-Throughput Incident Ingestion**: Parameterized ACID write path into PostgreSQL 15.
2. **Unsupervised ML Anomaly Detection**: Isolation Forest model trained on downtime distributions to isolate severe outage anomalies without needing labeled training data.
3. **Cyberpunk DevOps Observability Dashboard**: High-contrast, dark glassmorphic web UI with real-time multi-chart telemetry, service reliability scorecards, and chaos simulation.
4. **Production Container Orchestration**: Multi-stage Docker packaging, non-root execution, named volume durability, healthcheck-driven readiness probes, and advanced Macvlan/Ipvlan LAN routing specifications.

---

## 🖥️ Modern Web UI Dashboard

SentinelAI comes equipped with a real-time single-page observability dashboard built with **Tailwind CSS**, **Lucide Icons**, and **Chart.js**:

```
┌────────────────────────────────────────────────────────────────────────────────┐
│  [🛡️ SentinelAI] Enterprise v2.4   [Simulate Outage] [Seed Telemetry] [Log Inc] │
├────────────────────────────────────────────────────────────────────────────────┤
│  [backend: Online]  [sentinel-db: Active]  [ML Engine: Ready]  [Volume: Durable]│
├────────────────────────────────────────────────────────────────────────────────┤
│  [Total Events]  [MTTR/Avg]  [AI Outliers]  [Critical]  [Global SLA]  [Regions]│
├──────────────────────────────────────────────────────┬─────────────────────────┤
│  📈 Downtime Timeline & Anomaly Boundary            │ 🍩 Severity Breakdown   │
│     (Interactive Bar & Spline Curve Switcher)        │ 🧠 AI Diagnostics Card  │
├──────────────────────────────────────────────────────┼─────────────────────────┤
│  🛡️ Microservice Reliability Scorecard (SLA Gauge)   │ 🗺️ Regional Heatmap     │
│     (Uptime % per service: payment, auth, billing)   │    (Cloud Outage Zones) │
├──────────────────────────────────────────────────────┴─────────────────────────┤
│  📊 Live Telemetry Ledger (Search, Multi-Filter, Anomaly Badges, Export to CSV)│
└────────────────────────────────────────────────────────────────────────────────┘
```

### Dashboard Capabilities
* **Dynamic Visualization Suite**: Main downtime timeline with glowing red anomaly markers, severity doughnut distribution, and cloud zone bar charts.
* **Microservice Health Scorecard**: Auto-calculates uptime reliability percentages ($70\% - 100\%$) for every microservice.
* **Chaos / Outage Injector**: Injects random high-severity outage spikes to watch the unsupervised ML engine detect and tag anomalies in real time.
* **Telemetry Ledger & CSV Export**: Searchable incident table with 1-click export for incident postmortems.

---

## 🏛️ System Architecture

```mermaid
flowchart TD
    subgraph Clients["Ingestion & Observability Clients"]
        Browser["🌐 Web Browser / Modern Dashboard"]
        Swagger["📖 OpenAPI / Swagger Docs (/docs)"]
        Webhook["⚡ CI/CD & Monitoring Webhooks"]
    end

    subgraph DockerHost["Docker Container Stack (sentinel-net)"]
        subgraph Backend["sentinel-backend (FastAPI + Uvicorn)"]
            Router["API Router: /incidents, /health, /seed"]
            MLEngine["🧠 Isolation Forest Engine (scikit-learn)"]
            StaticUI["🎨 Dashboard Static Engine (/static)"]
            DBPool["🗄️ SQLAlchemy 2.0 Pool (psycopg2)"]
        end

        subgraph Database["sentinel-db (PostgreSQL 15)"]
            InitHook["/docker-entrypoint-initdb.d/init.sql"]
            PostgresCore["PostgreSQL Server (:5432)"]
        end
    end

    subgraph Storage["Persistent Host Storage"]
        NamedVolume[("💾 Docker Named Volume: postgres_data<br/>/var/lib/postgresql/data")]
    end

    Browser -->|HTTP :8000| Router
    Swagger -->|HTTP :8000| Router
    Webhook -->|POST /incidents| Router
    Router --> StaticUI
    Router --> MLEngine
    Router --> DBPool
    DBPool -->|TCP :5432| PostgresCore
    InitHook -.->|Initial Schema Boot| PostgresCore
    PostgresCore -->|ACID Persistence| NamedVolume
```

---

## 🔬 AI Anomaly Detection Engine

### Algorithm: Isolation Forest
SentinelAI utilizes **Isolation Forest**, an unsupervised tree ensemble algorithm built on the premise that **anomalous observations are few and structurally distinct**, making them easier to isolate than nominal data points.

```
       [Root Dataset: All Downtimes]
              /             \
       [Downtime <= 12]    [Downtime > 12] ─── (Isolated in 1 Split! -> ANOMALY 🚨)
          /        \
    [Downtime<=6] [Downtime>6]
       /    \       /     \
     ...   ...    ...    ...  ─── (Requires many recursive splits -> NOMINAL ✓)
```

### Mathematical Formulation
1. An ensemble of $t$ randomized Isolation Trees (iTrees) is constructed.
2. Given a feature instance $x$ (downtime duration) and subsample size $n$, the path length $h(x)$ is the number of edges $x$ traverses from the root node to a terminating leaf node.
3. The average path length $E(h(x))$ across the ensemble is normalized against the average path length of an unsuccessful search in a Binary Search Tree:
   $$c(n) = 2 \ln(n - 1) + 0.5772156649 \text{ (Euler-Mascheroni Constant)} - \frac{2(n - 1)}{n}$$
4. The composite anomaly score $s(x, n)$ is defined as:
   $$s(x, n) = 2^{-\frac{E(h(x))}{c(n)}}$$
   * If $s \to 1.0$: Short path length $\rightarrow$ **High confidence anomaly**.
   * If $s < 0.5$: Long path length $\rightarrow$ **Nominal baseline event**.

### Backend Implementation (`backend/app.py`)
```python
@app.get("/ai/risk-analysis")
def risk_analysis():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT downtime_minutes FROM incidents"))
        values = [r[0] for r in result]

    if len(values) < 5:
        return {"message": "not enough incidents"}

    # contamination=0.20 defines the top 20% statistical outlier threshold
    model = IsolationForest(contamination=0.2, random_state=42)
    model.fit([[v] for v in values])

    preds = model.predict([[v] for v in values])
    anomalies = [values[i] for i, p in enumerate(preds) if p == -1]

    return {"anomalous_downtime": anomalies}
```

---

## 📦 Container Infrastructure & Docker Compose

SentinelAI is orchestrated through Docker Compose into two decoupled, containerized services:

| Metric / Property | `sentinel-backend` | `sentinel-db` |
| :--- | :--- | :--- |
| **Base Image** | `python:3.11-slim` | `postgres:15` |
| **Container User** | `appuser` (Non-Root / Least Privilege) | `postgres` |
| **Internal Port** | `8000` | `5432` |
| **Host Port Mapping** | `8000:8000` | Isolated (Internal Network Only) |
| **Data Persistence** | Stateless | Managed Named Volume (`postgres_data`) |
| **Health Probe** | `GET /health` (HTTP 200) | `pg_isready -U postgres` |

### `docker-compose.yml`
```yaml
services:
  db:
    build: ./database
    container_name: sentinel-db
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
      POSTGRES_DB: sentinel
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - sentinel-net
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  backend:
    build: ./backend
    container_name: sentinel-backend
    environment:
      DATABASE_URL: postgresql://postgres:password@db:5432/sentinel
    ports:
      - "8000:8000"
    depends_on:
      db:
        condition: service_healthy
    networks:
      - sentinel-net
    restart: unless-stopped

volumes:
  postgres_data:

networks:
  sentinel-net:
    driver: bridge
```

---

## 🌐 Networking — Macvlan & Ipvlan Deep Dive

Standard Docker bridge networking places containers behind Network Address Translation (NAT), isolating them from direct physical local area network (LAN) communication. SentinelAI supports advanced layer 2 container network architectures:

```
                      Physical Network Router (192.168.1.1)
                                      │
               ┌──────────────────────┴──────────────────────┐
               │                                             │
      Host NIC (eth0)                               Physical LAN Devices
               │
    ┌──────────┴──────────┐
    │  Macvlan / Ipvlan   │
    ├─────────────────────┤
    │ sentinel-backend    │ ─── IP: 192.168.1.50 (Direct LAN Addressable)
    │ sentinel-db         │ ─── IP: 192.168.1.51 (Direct LAN Addressable)
    └─────────────────────┘
```

### Network Architecture Comparison

| Feature | Docker Bridge | Macvlan | Ipvlan L2 |
| :--- | :--- | :--- | :--- |
| **Addressing** | Virtual Subnet (172.x.x.x) | Real Physical LAN Subnet | Real Physical LAN Subnet |
| **MAC Address** | Generated Virtual MAC | Unique Hardware MAC per container | Shared Host Physical MAC |
| **Routing Overhead** | NAT Port Mapping Required | Zero NAT / Direct L2 Routing | Zero NAT / Direct L2 Routing |
| **Host Communication**| Accessible via `localhost:PORT` | Requires Host Macvlan Subinterface | Natively Supported by Kernel |
| **Hardware Requirement**| Cross-Platform | Direct Linux Physical NIC (`eth0`) | Direct Linux Physical NIC (`eth0`) |

### Production Macvlan Setup (Linux)
```bash
# 1. Create external Macvlan network bound to host physical interface (eth0)
docker network create \
  --driver macvlan \
  --subnet=192.168.1.0/24 \
  --gateway=192.168.1.1 \
  --opt parent=eth0 \
  sentinel-macvlan

# 2. Host Isolation Workaround (Allows host to communicate with containers)
ip link add macvlan-host link eth0 type macvlan mode bridge
ip addr add 192.168.1.99/32 dev macvlan-host
ip link set macvlan-host up
ip route add 192.168.1.0/24 dev macvlan-host
```

---

## 📚 REST API Reference

The interactive Swagger UI is live at `http://localhost:8000/docs`.

### 1. `GET /`
Returns the modern single-page DevOps intelligence dashboard.

### 2. `GET /health`
Liveness probe utilized by container orchestrators.
```json
{ "status": "running" }
```

### 3. `POST /incidents`
Records infrastructure incident telemetry into PostgreSQL. Supports both JSON body and URL query parameters.
```json
// POST /incidents
{
  "service_name": "payment-gateway",
  "severity": "critical",
  "downtime_minutes": 65,
  "region": "ap-south-1"
}
```
**Response (200 OK):**
```json
{ "message": "incident stored" }
```

### 4. `GET /incidents`
Retrieves all recorded telemetry sorted chronologically.
```json
[
  {
    "id": 1,
    "service_name": "auth-service",
    "severity": "low",
    "downtime_minutes": 4,
    "region": "us-east-1",
    "created_at": "2026-08-30T03:50:00"
  },
  {
    "id": 2,
    "service_name": "payment-gateway",
    "severity": "critical",
    "downtime_minutes": 65,
    "region": "ap-south-1",
    "created_at": "2026-08-30T03:51:00"
  }
]
```

### 5. `GET /ai/risk-analysis`
Executes Isolation Forest anomaly scoring across all stored downtime durations.
```json
{
  "anomalous_downtime": [65]
}
```

### 6. `POST /seed`
Instantly populates realistic multi-service demo telemetry.

---

## 🚀 Quickstart Guide

### Prerequisites
* [Docker Desktop 24+](https://www.docker.com/products/docker-desktop)
* [Git](https://git-scm.com/)

```bash
# 1. Clone the repository
git clone https://github.com/Nitanshu715/SentinelAI-Containerized-DevOps-Incident-Intelligence-System.git
cd SentinelAI-Containerized-DevOps-Incident-Intelligence-System

# 2. Build and launch the container stack
docker compose up -d --build

# 3. Access the endpoints
# Dashboard UI: http://localhost:8000
# OpenAPI Docs: http://localhost:8000/docs
# Health Probe: http://localhost:8000/health
```

---

## ☁️ 100% Free Cloud Deployment

You can deploy SentinelAI publicly to the internet with zero hosting costs using **Neon.tech** and **Vercel** / **Render**:

```mermaid
flowchart LR
    A["1. Create Free PostgreSQL<br/>(Neon.tech)"] --> B["2. Deploy App<br/>(Vercel or Render)"]
    B --> C["3. Add DATABASE_URL<br/>Environment Variable"]
    C --> D["4. Live Global URL &<br/>Dashboard Online!"]
```

### Step 1: Provision Free Serverless PostgreSQL
1. Sign up for free at [Neon.tech](https://neon.tech) (No credit card required).
2. Create a project named `sentinel-db` and copy your **Postgres Connection URI** (`postgresql://user:pass@ep-xyz.aws.neon.tech/neondb?sslmode=require`).

### Step 2: Deploy to Vercel
1. Fork or push this repository to your GitHub account.
2. Log into [Vercel.com](https://vercel.com) and click **"Add New Project"**.
3. Select your repository.
4. Add the Environment Variable:
   * **Key**: `DATABASE_URL`
   * **Value**: *(Your Neon.tech connection string)*
5. Click **Deploy**. Vercel will build and assign you an SSL-secured live domain (`https://your-project.vercel.app`)!

---

## 📂 Project Structure

```
sentinel-ai/
├── backend/
│   ├── app.py              # FastAPI server, SQLAlchemy pooling, Isolation Forest
│   ├── requirements.txt    # Pinned Python dependencies
│   ├── Dockerfile          # Multi-stage container build with non-root appuser
│   └── static/
│       └── index.html      # Modern Cyber/DevOps Glassmorphism Dashboard UI
├── database/
│   ├── Dockerfile          # Custom PostgreSQL 15 container wrapper
│   └── init.sql            # Idempotent table schema initialization
├── docker-compose.yml       # Stack orchestration, volumes, networks, healthchecks
├── vercel.json             # Vercel serverless Python deployment configuration
├── render.yaml             # Render Blueprint 1-click cloud deployment config
├── .dockerignore           # Excludes build context overhead (venv, caches)
├── .gitignore              # Git ignore configuration
├── LICENSE                 # MIT Open Source License
└── README.md               # Project documentation
```

---

## 📜 License
This project is open-source and licensed under the terms of the [MIT License](LICENSE).

<div align="center">
<b>SentinelAI &bull; Built with ❤️ for DevOps & SRE Teams</b>
</div>
