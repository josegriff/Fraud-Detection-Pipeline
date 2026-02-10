# Fraud Detection ETL Pipeline

**Rule-based batch ETL pipeline for detecting suspicious transactions**
Built as a portfolio project to demonstrate solid data engineering practices: ingestion, validation, business-rule enrichment, data quality checks, and scalable output (Parquet / future lakehouse)

### Why this project?
In real FinTech fraud systems, the data pipeline is the foundation. It must be reliable, auditable, and fast even before any ML model is added.
This project focuses on that core layer:
- Ingest raw transaction CSVs
- Apply rule-based fraud checks (velocity checks, amount > balance, type mismatches, etc.)
- Enforce data quality & validation
- Output clean, partitioned Parquet files (ready for Athena / S3 lakehouse / future ML)
- Prepare for orchestration (Airflow-style DAGs coming soon)

**No machine learning in this project**, this is purely a data engineering project: The main aim is to make data trustworthy and timely so a future model can consume it without garbage-in-garbage-out problems.

### Current Status
- Repository & folder structure set up
- Virtual environment & dependencies isolated
- Core packages installed (pandas, pyyaml. loguru, python-dotenv)
- Imports & basic environment verified
- Stage 2 in progress: Config + pipeline skeleton

### Tech Stack (So far)
- **Languages**: Python 3.12+
- **Core Libraries**:
  - pandas (Data handling)
  - pyyaml (Configuration)
  - loguru (Structured logging)
  - python-dotenv (env vars)
- **Tools / planned**:
  - Great Expectations (Data quality)
  - Airflow or Dagster (Orchestration)
  - Docker (Containerisation)
  - AWS S3 + Athena (Storage/Qyerying)
- **IDE**: Visual Studio Code

### Project Structure
