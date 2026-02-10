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
```
Fraud-Detection-Pipeline/
├── src/                    # All pipeline logic as Python package
│   ├── extract/            # Data ingestion (CSV → DataFrame)
│   ├── transform/          # Cleaning + fraud business rules
│   ├── load/               # Write Parquet / future S3/DB
│   ├── quality/            # Data quality & validation checks
│   ├── utils/              # Logging, config loader, helpers
│   ├── main.py             # Pipeline entry point
│   └── init.py
├── config/                 # YAML configs (paths, thresholds, rules)
│   └── config.yaml
├── data/                   # Datasets (raw/processed/external) — gitignored for large files
├── dags/                   # Future Airflow/Dagster DAG definitions
├── docs/                   # Architecture diagrams, decisions
├── notebooks/              # Quick EDA only — not production
├── tests/                  # Unit tests (pytest coming soon)
├── .venv/                  # Virtual environment (gitignored)
├── requirements.txt        # Reproducible dependencies
└── README.md
```


### Quick Start 
1. Clone the repo:
  ```bash
   git clone https://github.com/YOUR_USERNAME/Fraud-Detection-Pipeline.git
   cd Fraud-Detection-Pipeline
  ```

2. Create & activate virtual environment (Windows example):
  ```powershell
  python -m venv .venv
  .\.venv\Scripts\Activate.ps1
  ```
3. Install dependencies:
  ```powershell
  python -m pip install --upgrade pip
  pip install -r requirements.txt
  ```
4. (Coming soon) Run the skeleton pipeline:
  ```powershell
  python src/main.py
  ```

Roadmap:
- Stage 2: Config-driven skeleton pipeline with dummy extract/transform/load
- Stage 3: Ingest real/mock transaction CSV + basic cleaning
- Stage 4: Implement core fraud rules (velocity, balance checks, etc.)
- Stage 5: Data quality layer (schema validation, completeness, Great Expectations)
- Stage 6: Parquet partitioning & local "lakehouse" simulation
- Stage 7: Orchestration (Airflow local / Dagster) + retries
- Stage 8: Dockerization + basic monitoring/alerting stubs
- Stage 9: Deployment simulation (S3 + Athena queries)
- Stage 10: Documentation, tests, LinkedIn write-up

### Licensing: 
MIT License - you are free to fork/use as inspiration.
