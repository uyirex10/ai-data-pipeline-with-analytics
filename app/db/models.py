from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
    Text,
    Boolean
)

from sqlalchemy.orm import relationship

from app.db.database import Base


# =========================================================
# PIPELINE METADATA MODELS
# =========================================================

class PipelineRun(Base):
    """
    Tracks each full pipeline execution.
    """

    __tablename__ = "pipeline_runs"

    id = Column(Integer, primary_key=True, index=True)

    pipeline_name = Column(String, nullable=False)

    status = Column(String, nullable=False)

    started_at = Column(DateTime, default=datetime.utcnow)

    finished_at = Column(DateTime)

    records_processed = Column(Integer, default=0)

    error_message = Column(Text)

    created_at = Column(DateTime, default=datetime.utcnow)

    steps = relationship(
        "PipelineStep",
        back_populates="pipeline_run",
        cascade="all, delete-orphan"
    )


class PipelineStep(Base):
    """
    Tracks individual pipeline step execution.
    """

    __tablename__ = "pipeline_steps"

    id = Column(Integer, primary_key=True, index=True)

    pipeline_run_id = Column(
        Integer,
        ForeignKey("pipeline_runs.id"),
        nullable=False
    )

    step_name = Column(String, nullable=False)

    status = Column(String, nullable=False)

    started_at = Column(DateTime, default=datetime.utcnow)

    finished_at = Column(DateTime)

    records_processed = Column(Integer, default=0)

    error_message = Column(Text)

    created_at = Column(DateTime, default=datetime.utcnow)

    pipeline_run = relationship(
        "PipelineRun",
        back_populates="steps"
    )


class RawDataBatch(Base):
    """
    Tracks extracted raw data batches.
    """

    __tablename__ = "raw_data_batches"

    id = Column(Integer, primary_key=True, index=True)

    source_name = Column(String, nullable=False)

    batch_identifier = Column(
        String,
        unique=True,
        nullable=False
    )

    records_count = Column(Integer, default=0)

    extraction_time = Column(
        DateTime,
        default=datetime.utcnow
    )

    status = Column(String, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)


# =========================================================
# WAREHOUSE DIMENSION MODELS
# =========================================================

class CustomerDimension(Base):
    """
    Stores customer descriptive information.
    """

    __tablename__ = "customer_dimension"

    id = Column(Integer, primary_key=True, index=True)

    customer_name = Column(String, nullable=False)

    email = Column(String)

    city = Column(String)

    country = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)


class ProductDimension(Base):
    """
    Stores product descriptive information.
    """

    __tablename__ = "product_dimension"

    id = Column(Integer, primary_key=True, index=True)

    product_name = Column(String, nullable=False)

    category = Column(String)

    unit_price = Column(Float)

    created_at = Column(DateTime, default=datetime.utcnow)


# =========================================================
# FACT TABLES
# =========================================================

class SalesFact(Base):
    """
    Stores measurable sales events.
    """

    __tablename__ = "sales_fact"

    id = Column(Integer, primary_key=True, index=True)

    customer_id = Column(
        Integer,
        ForeignKey("customer_dimension.id")
    )

    product_id = Column(
        Integer,
        ForeignKey("product_dimension.id")
    )

    quantity = Column(Integer, nullable=False)

    revenue = Column(Float, nullable=False)

    sale_timestamp = Column(
        DateTime,
        nullable=False
    )

    created_at = Column(DateTime, default=datetime.utcnow)

    customer = relationship("CustomerDimension")

    product = relationship("ProductDimension")


# =========================================================
# ANALYTICS TABLES
# =========================================================

class DailyKPI(Base):
    """
    Stores precomputed daily KPIs.
    """

    __tablename__ = "daily_kpis"

    id = Column(Integer, primary_key=True, index=True)

    kpi_date = Column(DateTime, nullable=False)

    total_revenue = Column(Float, default=0)

    total_orders = Column(Integer, default=0)

    average_order_value = Column(Float, default=0)

    created_at = Column(DateTime, default=datetime.utcnow)


class AnomalyEvent(Base):
    """
    Stores detected business anomalies.
    """

    __tablename__ = "anomaly_events"

    id = Column(Integer, primary_key=True, index=True)

    anomaly_type = Column(String, nullable=False)

    description = Column(Text)

    severity = Column(String)

    detected_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    resolved = Column(Boolean, default=False)


# =========================================================
# AI INSIGHT TABLES
# =========================================================

class AIInsight(Base):
    """
    Stores generated AI business insights.
    """

    __tablename__ = "ai_insights"

    id = Column(Integer, primary_key=True, index=True)

    insight_type = Column(String, nullable=False)

    insight_text = Column(Text, nullable=False)

    generated_at = Column(
        DateTime,
        default=datetime.utcnow
    )


# =========================================================
# REPORTING TABLES
# =========================================================

class ReportLog(Base):
    __tablename__ = "report_logs"

    id = Column(Integer, primary_key=True, index=True)

    report_name = Column(String, nullable=False)

    report_type = Column(String, nullable=False)

    file_path = Column(String, nullable=False)

    status = Column(String, nullable=False)

    generated_at = Column(
        DateTime,
        default=datetime.utcnow
    )