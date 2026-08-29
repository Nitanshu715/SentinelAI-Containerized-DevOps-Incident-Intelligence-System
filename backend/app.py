from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from sqlalchemy import create_engine, text
from sklearn.ensemble import IsolationForest
import os
from pathlib import Path
from typing import Optional

BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parent

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:password@db:5432/sentinel"
)

# Render / Neon / Supabase compatibility for postgres:// -> postgresql://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

def init_db():
    """Ensure table exists upon startup across any database environment."""
    try:
        with engine.connect() as conn:
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS incidents (
                    id SERIAL PRIMARY KEY,
                    service_name TEXT,
                    severity TEXT,
                    downtime_minutes INT,
                    region TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """))
            conn.commit()
    except Exception as e:
        print(f"Database init warning: {e}")

app = FastAPI(title="SentinelAI", description="DevOps Incident Intelligence & Anomaly Detection System")

# Enable CORS for external frontend or web clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_html_content() -> str:
    possible_paths = [
        BASE_DIR / "static" / "index.html",
        ROOT_DIR / "static" / "index.html",
        ROOT_DIR / "backend" / "static" / "index.html",
        Path("backend/static/index.html"),
        Path("static/index.html"),
    ]
    for p in possible_paths:
        if p.exists():
            with open(p, "r", encoding="utf-8") as f:
                return f.read()
    return "<h1>SentinelAI API is Active. Visit <a href='/docs'>/docs</a> for Swagger UI.</h1>"

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/", response_class=HTMLResponse)
@app.get("/api", response_class=HTMLResponse)
@app.get("/api/", response_class=HTMLResponse)
def read_root():
    return HTMLResponse(content=get_html_content())

@app.get("/health")
@app.get("/api/health")
def health():
    return {"status": "running"}

class IncidentCreate(BaseModel):
    service_name: str
    severity: str
    downtime_minutes: int
    region: str

@app.post("/incidents")
@app.post("/api/incidents")
def create_incident(
    incident: Optional[IncidentCreate] = None,
    service_name: Optional[str] = Query(None),
    severity: Optional[str] = Query(None),
    downtime: Optional[int] = Query(None),
    region: Optional[str] = Query(None)
):
    s_name = incident.service_name if incident else service_name
    s_sev = incident.severity if incident else severity
    s_down = incident.downtime_minutes if incident else downtime
    s_reg = incident.region if incident else (region or "global")

    if not s_name or s_down is None or not s_sev:
        return JSONResponse(status_code=400, content={"error": "Missing required fields"})

    init_db()
    with engine.connect() as conn:
        conn.execute(
            text(
                "INSERT INTO incidents(service_name, severity, downtime_minutes, region) VALUES(:s, :sev, :d, :r)"
            ),
            {"s": s_name, "sev": s_sev, "d": s_down, "r": s_reg},
        )
        conn.commit()

    return {"message": "incident stored"}

@app.get("/incidents")
@app.get("/api/incidents")
def get_incidents():
    init_db()
    with engine.connect() as conn:
        result = conn.execute(text("SELECT id, service_name, severity, downtime_minutes, region, created_at FROM incidents ORDER BY id ASC"))
        rows = [dict(r._mapping) for r in result]

    return rows

@app.get("/ai/risk-analysis")
@app.get("/api/ai/risk-analysis")
def risk_analysis():
    init_db()
    with engine.connect() as conn:
        result = conn.execute(text("SELECT downtime_minutes FROM incidents"))
        values = [r[0] for r in result]

    if len(values) < 5:
        return {"message": "not enough incidents"}

    model = IsolationForest(contamination=0.2, random_state=42)
    model.fit([[v] for v in values])

    preds = model.predict([[v] for v in values])

    anomalies = [values[i] for i, p in enumerate(preds) if p == -1]

    return {"anomalous_downtime": anomalies}

@app.post("/seed")
@app.post("/api/seed")
def seed_demo_data():
    init_db()
    demo_records = [
        ("auth-service", "low", 4, "us-east-1"),
        ("api-gateway", "low", 6, "us-east-1"),
        ("billing-service", "medium", 5, "eu-west-1"),
        ("search-worker", "low", 7, "us-west-2"),
        ("notification-hub", "low", 6, "ap-south-1"),
        ("inventory-db", "medium", 8, "eu-central-1"),
        ("payment-gateway", "critical", 65, "ap-south-1"),
        ("checkout-api", "critical", 52, "us-east-1"),
    ]

    with engine.connect() as conn:
        for s_name, s_sev, s_down, s_reg in demo_records:
            conn.execute(
                text("INSERT INTO incidents(service_name, severity, downtime_minutes, region) VALUES(:s, :sev, :d, :r)"),
                {"s": s_name, "sev": s_sev, "d": s_down, "r": s_reg}
            )
        conn.commit()

    return {"message": "Successfully seeded demo DevOps incident telemetry", "count": len(demo_records)}