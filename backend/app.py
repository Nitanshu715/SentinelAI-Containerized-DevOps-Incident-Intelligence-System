from fastapi import FastAPI
from sqlalchemy import create_engine, text
from sklearn.ensemble import IsolationForest
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:password@db:5432/sentinel"
)

engine = create_engine(DATABASE_URL)

app = FastAPI(title="SentinelAI")

@app.get("/health")
def health():
    return {"status": "running"}


@app.post("/incidents")
def create_incident(service_name: str, severity: str, downtime: int, region: str):

    with engine.connect() as conn:
        conn.execute(
            text(
                "INSERT INTO incidents(service_name,severity,downtime_minutes,region) VALUES(:s,:sev,:d,:r)"
            ),
            {"s": service_name, "sev": severity, "d": downtime, "r": region},
        )
        conn.commit()

    return {"message": "incident stored"}


@app.get("/incidents")
def get_incidents():

    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM incidents"))
        rows = [dict(r) for r in result]

    return rows


@app.get("/ai/risk-analysis")
def risk_analysis():

    with engine.connect() as conn:
        result = conn.execute(text("SELECT downtime_minutes FROM incidents"))
        values = [r[0] for r in result]

    if len(values) < 5:
        return {"message": "not enough incidents"}

    model = IsolationForest(contamination=0.2)
    model.fit([[v] for v in values])

    preds = model.predict([[v] for v in values])

    anomalies = [values[i] for i, p in enumerate(preds) if p == -1]

    return {"anomalous_downtime": anomalies}