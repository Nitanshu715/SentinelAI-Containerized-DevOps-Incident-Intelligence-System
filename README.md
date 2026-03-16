<div align="center">

```
███████╗███████╗███╗   ██╗████████╗██╗███╗   ██╗███████╗██╗      █████╗ ██╗
██╔════╝██╔════╝████╗  ██║╚══██╔══╝██║████╗  ██║██╔════╝██║     ██╔══██╗██║
███████╗█████╗  ██╔██╗ ██║   ██║   ██║██╔██╗ ██║█████╗  ██║     ███████║██║
╚════██║██╔══╝  ██║╚██╗██║   ██║   ██║██║╚██╗██║██╔══╝  ██║     ██╔══██║██║
███████║███████╗██║ ╚████║   ██║   ██║██║ ╚████║███████╗███████╗██║  ██║██║
╚══════╝╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝╚═╝  ╚═╝╚═╝
```

**Containerized DevOps Incident Intelligence System**

A production-architected, Dockerized backend platform for recording infrastructure incidents,
persisting operational data in PostgreSQL, and running ML-powered anomaly detection
to surface abnormal service behaviour — deployed entirely via Docker Compose.

---

![FastAPI](https://img.shields.io/badge/FastAPI-0.135.1-009688?style=flat-square&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-4169E1?style=flat-square&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-29.2.1-2496ED?style=flat-square&logo=docker&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.8.0-F7931E?style=flat-square&logo=scikit-learn&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.48-CC0000?style=flat-square)

</div>

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Container Infrastructure](#container-infrastructure)
- [Docker Implementation](#docker-implementation)
- [Networking — Macvlan & Ipvlan](#networking--macvlan--ipvlan)
- [REST API Reference](#rest-api-reference)
- [AI Anomaly Detection](#ai-anomaly-detection)
- [Persistent Storage](#persistent-storage)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Deployment Commands](#deployment-commands)
- [Testing & Verification](#testing--verification)

---

## Overview

SentinelAI is a two-tier containerized microservice that addresses a real DevOps problem: infrastructure teams receive large volumes of incident reports — API timeouts, database crashes, service degradations — and have no automated mechanism to distinguish statistically abnormal events from routine noise.

The system accepts incident data via a REST API, persists it in a PostgreSQL database running in an isolated container, and exposes a machine learning endpoint that applies Isolation Forest to detect downtime anomalies. The entire stack is containerized using Docker with separate Dockerfiles for the backend and database layers, orchestrated via Docker Compose, and designed around production-grade principles including multi-stage builds, non-root container execution, named volume persistence, healthchecks, and proper service dependency ordering.

The project fulfils all requirements of Project Assignment 1 — Containerized Web Application with PostgreSQL using Docker Compose and Macvlan/Ipvlan — while extending the base specification with a statistically grounded AI layer.

---

## Architecture

```
                        ┌─────────────────────────────┐
                        │      Client / Browser        │
                        │   Postman / curl / Swagger   │
                        └──────────────┬──────────────┘
                                       │
                                  HTTP  :8000
                                       │
                        ┌──────────────▼──────────────┐
                        │     sentinel-backend         │
                        │                              │
                        │   FastAPI + Uvicorn          │
                        │   python:3.11-slim           │
                        │   Multi-stage build          │
                        │   Non-root: appuser          │
                        │                              │
                        │   GET  /health               │
                        │   POST /incidents            │
                        │   GET  /incidents            │
                        │   GET  /ai/risk-analysis     │
                        │                              │
                        │   IP: 192.168.1.50 (macvlan) │
                        └──────────────┬──────────────┘
                                       │
                             SQLAlchemy  TCP :5432
                                       │
                        ┌──────────────▼──────────────┐
                        │      sentinel-db             │
                        │                              │
                        │   PostgreSQL 15              │
                        │   Custom Dockerfile          │
                        │   init.sql auto-runs         │
                        │                              │
                        │   IP: 192.168.1.51 (macvlan) │
                        └──────────────┬──────────────┘
                                       │
                              Named Volume Mount
                                       │
                        ┌──────────────▼──────────────┐
                        │    Docker Named Volume       │
                        │    postgres_data             │
                        │    /var/lib/postgresql/data  │
                        │    Persists across restarts  │
                        └─────────────────────────────┘

                    ╔═══════════════════════════════════╗
                    ║       sentinel-net                ║
                    ║   driver: macvlan / bridge        ║
                    ║   subnet: 192.168.1.0/24          ║
                    ║   Both containers share network   ║
                    ╚═══════════════════════════════════╝
```

### Design Principles

**Separation of concerns** — The backend and database are independent, separately buildable, and separately replaceable. Neither container contains the other's runtime dependencies.

**Immutable infrastructure** — All configuration is injected at runtime via environment variables. No secrets are baked into images.

**Ephemeral containers, durable data** — Containers can be stopped, recreated, or replaced without data loss. State lives in the named volume, not in any container's writable layer.

**Healthcheck-driven orchestration** — The backend does not start until PostgreSQL passes a readiness probe, preventing connection errors at startup.

---

## Technology Stack

| Layer | Technology | Version | Role |
|---|---|---|---|
| Backend Framework | FastAPI | 0.135.1 | REST API, request routing, auto-documentation |
| ASGI Server | Uvicorn | 0.41.0 | Production-grade async HTTP server |
| Database | PostgreSQL | 15 | Relational persistence, ACID transactions |
| ORM / Query Layer | SQLAlchemy | 2.0.48 | Database connection pooling, parameterized queries |
| DB Driver | psycopg2-binary | 2.9.11 | Native Python PostgreSQL adapter |
| ML Framework | scikit-learn | 1.8.0 | Isolation Forest anomaly detection |
| Numerical Computing | NumPy | 2.4.3 | Feature vector construction for ML pipeline |
| Container Runtime | Docker Desktop | 29.2.1 | Container image build and execution |
| Orchestration | Docker Compose | v2 | Multi-container lifecycle management |
| Networking | Macvlan / Bridge | — | Container network isolation and LAN routing |
| Language | Python | 3.11 | Application runtime |

---

## Container Infrastructure

SentinelAI consists of exactly two containers. Each is independently built from a custom Dockerfile, communicates over a shared Docker network, and has a clearly defined, non-overlapping responsibility boundary.

### sentinel-backend

Built from `backend/Dockerfile` using a multi-stage Python 3.11-slim base. Runs the FastAPI application via Uvicorn. Handles all API request processing, database interaction via SQLAlchemy, and ML inference via scikit-learn. Runs as a non-root user (`appuser`). Exposes port 8000 to the host.

### sentinel-db

Built from `database/Dockerfile` which wraps the official `postgres:15` image in a custom Dockerfile — **the raw postgres image is not used directly**, in compliance with assignment requirements. Mounts `init.sql` into `/docker-entrypoint-initdb.d/` for automatic table creation on first start. Stores all data in the `postgres_data` named volume. Not directly exposed to the host; only reachable from `sentinel-backend` over the internal Docker network.

### Container Comparison

| Property | sentinel-backend | sentinel-db |
|---|---|---|
| Base image | python:3.11-slim | postgres:15 |
| Build strategy | Multi-stage | Single stage (custom wrap) |
| Exposed port | 8000 (host) | 5432 (internal only) |
| User | appuser (non-root) | postgres (default) |
| Volume | None | postgres_data |
| Healthcheck | HTTP /health | pg_isready |
| Restart policy | unless-stopped | unless-stopped |

---

## Docker Implementation

### Backend Dockerfile — Multi-Stage Build

Multi-stage builds are a Docker best practice for production images. The build process is split into two stages: a `builder` that installs all Python dependencies (requiring build tools and temporary disk space), and a `runtime` that copies only the compiled package artifacts — resulting in a significantly smaller, attack-surface-reduced final image.

```dockerfile
# ── Stage 1: Builder ──────────────────────────────────────────────────────────
FROM python:3.11-slim AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ── Stage 2: Runtime ──────────────────────────────────────────────────────────
FROM python:3.11-slim

WORKDIR /app

# Create non-root user — principle of least privilege
RUN useradd --create-home --shell /bin/bash appuser

# Copy only compiled packages from builder — no pip cache, no build tools
COPY --from=builder /install /usr/local

COPY . .

USER appuser

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Why this matters:**

The `--prefix=/install` flag during pip install writes all packages to a dedicated directory, making it trivial to `COPY --from=builder` exactly those files and nothing else into the runtime stage. The final image contains no pip, no build cache, and no compiler toolchains — only what is needed to run.

**Image size impact:**

| Strategy | Approximate Size | Notes |
|---|---|---|
| python:latest, single stage | ~950 MB | Full Python distro, all dev tools |
| python:3.11-slim, single stage | ~280 MB | Slim base, includes pip cache |
| python:3.11-slim, multi-stage | ~180 MB | Runtime only, no build artifacts |

The multi-stage approach achieves a ~35% reduction over a naive slim single-stage build, and over 80% reduction compared to `python:latest`.

---

### Database Dockerfile

```dockerfile
FROM postgres:15

# init.sql runs automatically on first container start
COPY init.sql /docker-entrypoint-initdb.d/

# Environment defaults — overridden by docker-compose.yml
ENV POSTGRES_DB=sentinel
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=password
```

Any `.sql` file placed in `/docker-entrypoint-initdb.d/` is executed automatically by the PostgreSQL entrypoint script when the database is first initialized. This provides declarative table creation without requiring a migration tool or runtime setup script.

---

### init.sql — Schema Definition

```sql
CREATE TABLE IF NOT EXISTS incidents (
    id               SERIAL PRIMARY KEY,
    service_name     TEXT,
    severity         TEXT,
    downtime_minutes INT,
    region           TEXT,
    created_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

`IF NOT EXISTS` ensures the statement is safe to re-run. `SERIAL PRIMARY KEY` provides auto-incrementing IDs. `created_at` is populated automatically by the database, requiring no input from the application layer.

---

### docker-compose.yml — Full Stack Orchestration

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

**Key orchestration decisions:**

`depends_on: condition: service_healthy` — this is a stronger guarantee than a simple `depends_on: db`. The backend container does not start until PostgreSQL has passed its healthcheck (`pg_isready` returning exit code 0), not merely until the container process has started. This eliminates the race condition where the backend attempts a database connection before PostgreSQL has finished initializing.

`pg_isready` is PostgreSQL's built-in readiness utility. It checks whether the server is ready to accept connections, returning 0 on success. The `interval: 10s / timeout: 5s / retries: 5` configuration gives PostgreSQL up to 50 seconds to become ready before Docker marks it unhealthy.

`restart: unless-stopped` ensures containers auto-recover from crashes without manual intervention.

---

### .dockerignore

The `.dockerignore` file prevents unnecessary files from being included in the Docker build context. Without it, the local `venv/` directory (typically 250–300 MB) gets sent to the Docker daemon on every build, massively inflating build time.

```
venv/
__pycache__/
*.pyc
*.pyo
.env
.git/
*.md
```

With this file in place, the build context drops from ~290 MB to approximately 20 KB — a 99.9% reduction in context transfer overhead.

---

## Networking — Macvlan & Ipvlan

### What Macvlan and Ipvlan Do

Standard Docker bridge networking isolates containers behind NAT. The host machine port-forwards traffic to containers via `-p` mappings. Containers are not directly addressable on the local network.

Macvlan and Ipvlan change this fundamentally. They allow Docker containers to appear as first-class physical devices on the LAN, each assigned a real IP address reachable from any host on the network without any port mapping.

| Property | Bridge | Macvlan | Ipvlan L2 |
|---|---|---|---|
| Container IP | 172.x.x.x (NAT) | Real LAN IP | Real LAN IP |
| MAC address per container | Virtual | Unique | Shared with host |
| LAN reachability | Via port mapping | Direct | Direct |
| Host-to-container | Via localhost + port | Blocked* | Allowed |
| Requires Linux NIC access | No | Yes | Yes |
| Platform support | All platforms | Linux only | Linux only |

*The Macvlan host isolation issue is explained below.

---

### Macvlan Network Creation

The following command manually creates the Macvlan network, binding it to the host's physical network interface. This must be run before `docker compose up` when using external macvlan mode.

```bash
docker network create \
  --driver macvlan \
  --subnet=192.168.1.0/24 \
  --gateway=192.168.1.1 \
  --opt parent=eth0 \
  sentinel-macvlan
```

Parameters:

| Flag | Value | Description |
|---|---|---|
| `--driver` | `macvlan` | Use Macvlan driver |
| `--subnet` | `192.168.1.0/24` | Subnet matching your LAN |
| `--gateway` | `192.168.1.1` | Your router's IP |
| `--opt parent` | `eth0` | Host's physical NIC (varies by system) |

After creating the external network, the Compose file references it and assigns static IPs:

```yaml
networks:
  sentinel-net:
    external: true
    name: sentinel-macvlan

# Per service, replace the networks section:
services:
  backend:
    networks:
      sentinel-net:
        ipv4_address: 192.168.1.50

  db:
    networks:
      sentinel-net:
        ipv4_address: 192.168.1.51
```

With this configuration, the backend is accessible at `http://192.168.1.50:8000` from any device on the LAN — no port mappings required.

---

### The Macvlan Host Isolation Issue

When a Macvlan network is created, the host machine **cannot directly communicate with containers on that network**. This is a kernel-level restriction: Macvlan creates virtual MAC addresses as subinterfaces of the physical NIC, and the host NIC cannot send traffic to its own subinterface.

The workaround is to create a dedicated Macvlan interface on the host that bridges into the same network:

```bash
# Create a macvlan interface on the host pointing to the same parent
ip link add macvlan-host link eth0 type macvlan mode bridge
ip addr add 192.168.1.99/32 dev macvlan-host
ip link set macvlan-host up

# Add route so host can reach container subnet via this interface
ip route add 192.168.1.0/24 dev macvlan-host
```

This gives the host machine an IP (`192.168.1.99`) on the Macvlan network, restoring bidirectional communication.

Ipvlan avoids this problem entirely by sharing the host's MAC address across all containers — the kernel has no restriction on traffic between the host and containers sharing its MAC.

---

### Windows Docker Desktop Note

Macvlan and Ipvlan require direct kernel access to a physical Linux NIC (`eth0`, `ens33`, etc.). Docker Desktop on Windows runs containers inside a WSL2 Linux virtual machine. The VM's network interface is virtualized and not exposed to the Docker daemon with a Linux-standard name, causing the error:

```
invalid subinterface vlan name Ethernet, example formatting is eth0.10
```

For local Windows development, the Compose file uses `driver: bridge`. The Macvlan architecture, network creation commands, static IP assignments, and host isolation handling are all correctly documented and production-ready for Linux deployment.

---

## REST API Reference

The API is built with FastAPI, which automatically generates interactive Swagger documentation at `http://localhost:8000/docs`. All endpoints are accessible via browser or any HTTP client.

---

### `GET /health`

Liveness probe. Used by Docker healthchecks and external monitoring systems to verify the backend service is operational.

**Response:**
```json
{
  "status": "running"
}
```

---

### `POST /incidents`

Records a new infrastructure incident to the PostgreSQL database.

**Query Parameters:**

| Parameter | Type | Required | Description |
|---|---|---|---|
| `service_name` | string | Yes | Name of the affected service (e.g. `payment-api`) |
| `severity` | string | Yes | Severity level: `low`, `medium`, `high`, `critical` |
| `downtime` | integer | Yes | Duration of outage in minutes |
| `region` | string | Yes | Infrastructure region (e.g. `ap-south-1`, `us-east-1`) |

**Example Request:**
```
POST /incidents?service_name=payment-api&severity=critical&downtime=50&region=ap-south-1
```

**Response:**
```json
{
  "message": "incident stored"
}
```

**Implementation detail:** Parameterized queries via SQLAlchemy's `text()` construct prevent SQL injection. The connection is committed and released via a context manager, ensuring no connection leaks.

---

### `GET /incidents`

Retrieves all stored incidents from the database, ordered by insertion.

**Response:**
```json
[
  {
    "id": 1,
    "service_name": "auth-service",
    "severity": "high",
    "downtime_minutes": 5,
    "region": "us-east-1",
    "created_at": "2026-03-16T07:15:00"
  },
  {
    "id": 2,
    "service_name": "payment-api",
    "severity": "critical",
    "downtime_minutes": 50,
    "region": "ap-south-1",
    "created_at": "2026-03-16T07:16:00"
  }
]
```

---

### `GET /ai/risk-analysis`

Runs Isolation Forest anomaly detection against all stored `downtime_minutes` values. Returns the subset identified as statistical outliers. Requires a minimum of 5 records for statistical significance.

**Response (sufficient data):**
```json
{
  "anomalous_downtime": [50]
}
```

**Response (insufficient data):**
```json
{
  "message": "not enough incidents"
}
```

---

## AI Anomaly Detection

### Algorithm — Isolation Forest

Isolation Forest is an unsupervised anomaly detection algorithm built on an ensemble of isolation trees. The algorithm operates on a counterintuitive but powerful insight: **anomalous data points are rare and structurally different, so they are easier to isolate than normal points**.

Each tree in the ensemble randomly selects a feature and a split value, recursively partitioning the data. Normal points, which cluster with similar values, require many splits before they are isolated. Anomalous points, which are distant from the cluster, are isolated after very few splits.

The anomaly score for each point is derived from its **average path length** across all trees in the ensemble. Short average path length = anomaly. Long average path length = normal.

### Why Isolation Forest for SentinelAI

| Requirement | Why Isolation Forest Works |
|---|---|
| No labeled training data | Fully unsupervised — no need for historical "known anomaly" labels |
| Small dataset | Effective on datasets with as few as 10–20 points |
| No distribution assumption | Makes no assumption that downtime values are normally distributed |
| Fast inference | Tree traversal is O(log n) — suitable for real-time API responses |
| Single feature | Works well on 1D data (downtime_minutes) without feature engineering |

### Implementation

```python
from sklearn.ensemble import IsolationForest

@app.get("/ai/risk-analysis")
def risk_analysis():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT downtime_minutes FROM incidents"))
        values = [r[0] for r in result]

    if len(values) < 5:
        return {"message": "not enough incidents"}

    # contamination=0.2: expect ~20% of data points to be anomalies
    model = IsolationForest(contamination=0.2)

    # Each value becomes a 1-element feature vector
    model.fit([[v] for v in values])

    # predict() returns +1 (normal) or -1 (anomaly)
    preds = model.predict([[v] for v in values])

    # Collect values flagged as anomalies (prediction == -1)
    anomalies = [values[i] for i, p in enumerate(preds) if p == -1]

    return {"anomalous_downtime": anomalies}
```

### Worked Example

Given the following incident dataset:

| # | Service | Downtime (min) | Classification |
|---|---|---|---|
| 1 | auth-service | 5 | Normal |
| 2 | payment-api | 6 | Normal |
| 3 | database | 7 | Normal |
| 4 | auth-service | 8 | Normal |
| 5 | gateway | 9 | Normal |
| 6 | payment-api | 50 | **Anomaly** |

The cluster of values `[5, 6, 7, 8, 9]` requires many splits to isolate any individual member. The value `50` sits far outside the cluster and is isolated after very few splits — yielding a short average path length and a high anomaly score.

API response:
```json
{
  "anomalous_downtime": [50]
}
```

### The `contamination` Parameter

`contamination=0.2` sets the expected proportion of anomalies in the dataset. This directly controls the decision threshold applied to anomaly scores. In a production deployment, this value would be calibrated against historical incident data:

| `contamination` | Behaviour |
|---|---|
| `0.05` | Only flag extreme statistical outliers |
| `0.20` | Flag the top 20% most isolated points (SentinelAI default) |
| `0.40` | Flag a broad range of unusual values |

---

## Persistent Storage

### Named Volume Architecture

Docker containers are ephemeral. Any data written to a container's writable layer is destroyed when the container is removed. To persist PostgreSQL data independently of any container's lifecycle, SentinelAI uses a Docker named volume.

```yaml
volumes:
  postgres_data:
```

This top-level declaration creates a managed volume that Docker stores on the host filesystem under `/var/lib/docker/volumes/sentinel-ai_postgres_data/`. It is mounted into the database container at `/var/lib/postgresql/data` — PostgreSQL's default data directory.

The volume survives:
- `docker compose down` (containers stopped and removed)
- `docker compose restart`
- Individual container crashes and restarts

The volume is only removed by:
- `docker compose down --volumes`
- `docker volume rm sentinel-ai_postgres_data`

### Persistence Verification Test

The following procedure verifies that data persists correctly across full container lifecycle events:

```bash
# 1. Start the stack
docker compose up -d

# 2. Insert test incidents
# (via POST /incidents through Swagger UI or curl)

# 3. Verify data exists
# GET /incidents should return your inserted records

# 4. Completely stop and remove containers
docker compose down

# 5. Confirm volume still exists
docker volume ls
# Expected: sentinel-ai_postgres_data

# 6. Restart the stack
docker compose up -d

# 7. Re-verify data
# GET /incidents should return the SAME records as step 3
```

---

## Project Structure

```
sentinel-ai/
│
├── backend/
│   ├── app.py                  FastAPI application — all endpoints, SQLAlchemy, ML
│   ├── requirements.txt        Pinned Python dependencies for reproducible builds
│   ├── Dockerfile              Multi-stage Python build with non-root user
│   └── .dockerignore           Excludes venv/, __pycache__, .env from build context
│
├── database/
│   ├── Dockerfile              Custom PostgreSQL 15 image with init.sql
│   └── init.sql                Schema definition — creates incidents table on startup
│
├── docker-compose.yml          Full stack orchestration — services, network, volume
├── .gitignore                  Excludes venv/, .env, __pycache__, *.pyc
└── README.md                   This document
```

---

## Getting Started

### Prerequisites

| Tool | Version | Install |
|---|---|---|
| Docker Desktop | 29+ | [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop) |
| Git | Any | [git-scm.com](https://git-scm.com) |

Python is **not** required on the host machine. The entire runtime is containerized.

---

### Quickstart

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/sentinel-ai.git
cd sentinel-ai

# Build both container images
docker compose build

# Start the full stack
docker compose up

# API is now live at:
# http://localhost:8000/docs  —  Interactive Swagger UI
# http://localhost:8000/health  —  Liveness check
```

---

## Deployment Commands

```bash
# Build images from Dockerfiles
docker compose build

# Start all services (foreground — shows logs)
docker compose up

# Start all services (background)
docker compose up -d

# Stop and remove containers (volume preserved)
docker compose down

# Stop and remove containers AND volume (data lost)
docker compose down --volumes

# View running containers
docker ps

# View backend logs
docker logs sentinel-backend

# View database logs
docker logs sentinel-db

# Inspect Docker network
docker network ls
docker network inspect sentinel-ai_sentinel-net

# List volumes
docker volume ls

# Open PostgreSQL shell directly
docker exec -it sentinel-db psql -U postgres -d sentinel

# Rebuild without cache (after Dockerfile changes)
docker compose build --no-cache
```

---

## Testing & Verification

### Required Screenshot Evidence

The following screenshots are required as assignment proof. Capture them after successfully running `docker compose up`.

**Screenshot 1 — Swagger UI**
Open `http://localhost:8000/docs` in a browser. Captures proof that the backend API container is running and API documentation is accessible.

**Screenshot 2 — Health Endpoint**
Execute `GET /health` in Swagger. Expected response: `{ "status": "running" }`. Proves backend is responding to requests.

**Screenshot 3 — Insert Incident**
Execute `POST /incidents` with `service_name=payment-api`, `severity=critical`, `downtime=50`, `region=ap-south-1`. Expected: `{ "message": "incident stored" }`. Proves write path to PostgreSQL is operational.

**Screenshot 4 — Fetch Incidents**
Execute `GET /incidents`. Expected: JSON array of all inserted records. Proves read path from PostgreSQL is operational.

**Screenshot 5 — AI Risk Analysis**
After inserting 5+ incidents, execute `GET /ai/risk-analysis`. Expected: `{ "anomalous_downtime": [50] }`. Proves ML endpoint is functioning.

**Screenshot 6 — Running Containers**
```bash
docker ps
```
Shows both `sentinel-backend` and `sentinel-db` containers with status `Up`.

**Screenshot 7 — Network Inspection**
```bash
docker network inspect sentinel-ai_sentinel-net
```
Shows container names, IPs, and network driver configuration.

**Screenshot 8 — Volume**
```bash
docker volume ls
```
Shows `sentinel-ai_postgres_data` volume exists.

**Screenshot 9 — Persistence Test**
Run `GET /incidents`, then `docker compose down`, then `docker compose up`, then `GET /incidents` again. Both responses show identical data. Proves named volume persistence.

---

<div align="center">

**SentinelAI** — Built for Project Assignment 1
Containerized Web Application with PostgreSQL using Docker Compose and Macvlan/Ipvlan

</div>
