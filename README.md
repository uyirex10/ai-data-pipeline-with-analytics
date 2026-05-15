# AI Data Pipeline with Analytics & Business Intelligence

An enterprise-style automated ETL and analytics platform built with Python, PostgreSQL, FastAPI, Dash, and Ollama.

This project demonstrates modern data engineering, analytics engineering, AI orchestration, and backend system design concepts.

---

# Features

- Multi-source data extraction
  - CSV files
  - REST APIs
  - SQL databases

- Data transformation and validation

- PostgreSQL warehouse loading

- KPI analytics engine

- Revenue anomaly detection

- AI-generated business insights using Ollama

- Automated HTML report generation

- Dashboard API layer with FastAPI

- Interactive analytics dashboard with Dash & Plotly

- Automated ETL scheduling using APScheduler

- Production-ready modular architecture

---

# System Architecture

```text
Data Sources
    ↓
Extractors
    ↓
Transformers
    ↓
Validators
    ↓
Warehouse Loaders
    ↓
PostgreSQL Data Warehouse
    ↓
KPI Engine
    ↓
Anomaly Detection
    ↓
AI Insight Generation
    ↓
Report Generation
    ↓
FastAPI Layer
    ↓
Dash Dashboard
```

---

# Technologies Used

## Backend

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- APScheduler

## Analytics & Visualization

- Pandas
- Plotly
- Dash

## AI Layer

- Ollama
- Phi LLM

## Infrastructure Concepts

- ETL pipelines
- Data warehousing
- Scheduling
- Caching
- Bulk loading
- Fault tolerance
- Modular architecture

---

# Setup

## Clone Repository

```bash
git clone <your_repo_url>
cd ai-data-pipeline-with-analytics
```

---

## Create Virtual Environment

```bash
python -m venv .venv
```

Activate:

### Windows

```bash
.venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment Variables

Create:

```text
.env
```

using:

```text
.env.example
```

---

## Create Database Tables

```bash
python create_tables.py
```

---

# Running The System

## Run ETL Pipeline

```bash
python run_pipeline.py
```

---

## Run Scheduler

```bash
python run_scheduler.py
```

---

## Run FastAPI Backend

```bash
uvicorn app.api.dashboard_api:app --reload
```

---

## Run Dashboard

```bash
python app/dashboard/dashboard_app.py
```

Dashboard URL:

```text
http://127.0.0.1:8050
```

API Docs:

```text
http://127.0.0.1:8000/docs
```

---

# Engineering Concepts Demonstrated

- Clean Architecture
- Repository Pattern
- Factory Pattern
- Strategy Pattern
- ETL Orchestration
- KPI Aggregation
- Anomaly Detection
- AI-Orchestrated Analytics
- Production Logging
- Scheduling & Automation
- API-Driven Dashboards
- Performance Optimization
- Bulk Database Operations
- Fault-Tolerant AI Systems

---

# Future Improvements

- Docker deployment
- Redis caching
- Celery background workers
- Airflow orchestration
- Real-time streaming pipelines
- Cloud deployment
- Authentication & RBAC
- Kubernetes deployment

---

# Author

Uyi Rex