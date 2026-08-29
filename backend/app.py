from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy import create_engine, text
from sklearn.ensemble import IsolationForest
import os
from pathlib import Path
from typing import Optional

BASE_DIR = Path(__file__).resolve().parent

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
        print(f"Database init warning (will retry on request): {e}")

app = FastAPI(title="SentinelAI", description="DevOps Incident Intelligence & Anomaly Detection System")

# Enable CORS for external frontend or web clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static directory if it exists
static_dir = BASE_DIR / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/")
def read_root():
    index_file = BASE_DIR / "static" / "index.html"
    if index_file.exists():
        return FileResponse(str(index_file))
    return {"message": "SentinelAI API is active. Visit /docs for Swagger documentation."}

@app.get("/health")
def health():
    return {"status": "running"}

class IncidentCreate(BaseModel):
    service_name: str
    severity: str
    downtime_minutes: int
    region: str

@app.post("/incidents")
def create_incident(
    incident: Optional[IncidentCreate] = None,
    service_name: Optional[str] = Query(None),
    severity: Optional[str] = Query(None),
    downtime: Optional[int] = Query(None),
    region: Optional[str] = Query(None)
):
    # Support both JSON body and query parameters for full compatibility
    s_name = incident.service_name if incident else service_name
    s_sev = incident.severity if incident else severity
    s_down = incident.downtime_minutes if incident else downtime
    s_reg = incident.region if incident else (region or "global")

    if not s_name or s_down is None or not s_sev:
        return {"error": "Missing required fields (service_name, severity, downtime_minutes)"}

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
def get_incidents():
    init_db()
    with engine.connect() as conn:
        result = conn.execute(text("SELECT id, service_name, severity, downtime_minutes, region, created_at FROM incidents ORDER BY id ASC"))
        rows = [dict(r._mapping) for r in result]

    return rows

@app.get("/ai/risk-analysis")
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
def seed_demo_data():
    """Seeds realistic demo DevOps incident telemetry to immediately showcase ML anomaly detection."""
    init_db()
    demo_records = [
        ("auth-service", "low", 4, "us-east-1"),
        ("api-gateway", "low", 6, "us-east-1"),
        ("billing-service", "medium", 5, "eu-west-1"),
        ("search-worker", "low", 7, "us-west-2"),
        ("notification-hub", "low", 6, "ap-south-1"),
        ("inventory-db", "medium", 8, "eu-central-1"),
        ("payment-gateway", "critical", 65, "ap-south-1"),  # Clear Outlier / Anomaly
        ("checkout-api", "critical", 52, "us-east-1"),      # Clear Outlier / Anomaly
    ]

    with engine.connect() as conn:
        for s_name, s_sev, s_down, s_reg in demo_records:
            conn.execute(
                text("INSERT INTO incidents(service_name, severity, downtime_minutes, region) VALUES(:s, :sev, :d, :r)"),
                {"s": s_name, "sev": s_sev, "d": s_down, "r": s_reg}
            )
        conn.commit()

    return {"message": "Successfully seeded demo DevOps incident telemetry", "count": len(demo_records)}