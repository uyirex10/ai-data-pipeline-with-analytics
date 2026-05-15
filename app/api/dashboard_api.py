from fastapi import FastAPI

from app.db.database import SessionLocal
from app.db.models import AIInsight, AnomalyEvent, DailyKPI

app = FastAPI(
    title="AI Data Pipeline Dashboard API",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "AI Data Pipeline API is running"
    }


@app.get("/dashboard/kpis")
def get_latest_kpis():
    db = SessionLocal()

    try:
        latest_kpi = (
            db.query(DailyKPI)
            .order_by(DailyKPI.kpi_date.desc())
            .first()
        )

        if not latest_kpi:
            return {
                "message": "No KPI data available"
            }

        return {
            "kpi_date": latest_kpi.kpi_date,
            "total_revenue": latest_kpi.total_revenue,
            "total_orders": latest_kpi.total_orders,
            "average_order_value": latest_kpi.average_order_value
        }

    finally:
        db.close()


@app.get("/dashboard/anomalies")
def get_recent_anomalies():
    db = SessionLocal()

    try:
        anomalies = (
            db.query(AnomalyEvent)
            .order_by(AnomalyEvent.detected_at.desc())
            .limit(10)
            .all()
        )

        return [
            {
                "type": anomaly.anomaly_type,
                "description": anomaly.description,
                "severity": anomaly.severity,
                "detected_at": anomaly.detected_at
            }
            for anomaly in anomalies
        ]

    finally:
        db.close()


@app.get("/dashboard/insights")
def get_latest_ai_insight():
    db = SessionLocal()

    try:
        insight = (
            db.query(AIInsight)
            .order_by(AIInsight.generated_at.desc())
            .first()
        )

        if not insight:
            return {
                "message": "No AI insight available"
            }

        return {
            "insight_type": insight.insight_type,
            "insight_text": insight.insight_text,
            "generated_at": insight.generated_at
        }

    finally:
        db.close()