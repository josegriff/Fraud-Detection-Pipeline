# Fraud Detection ETL Pipeline

**Rule-based batch ETL pipeline for detecting suspicious transactions**

Built as a portfolio project to demonstrate data engineering practices: ingestion, validation, business-rule enrichment

### Why this project?

Fraud detection starts long before any machine learning model is trained, it begins with clean, reliable data. The ETL pipeline is the foundation that ensures every downstream fraud model, dashboard, or alerting system receives trustworthy input.

The primary focus of this project is to build that foundation and demonstrate how a modern fraud pipeline should behave:
- Ingest raw transaction data from CSV files
- Normalise and validate schema to enforce data quality
- Engineer time-based features (hour, weekday, weekend)
- Apply rule-based fraud checks:
  - High-value flags
  - Odd-hour activity
  - Merchant anomalies
- Write partitioned Parquet datasets using a datasets using a data-lake layout (year/month/day)
- Log every step with a centralised, rotating Loguru logger
- Runs as modular, config-driven ETL pipeline ready for orchestration (Airflow) and cloud deployment (Athena)

Instead of focusing on machine learning, this project is to display skills in the core engineering layer that fradu systems can rely on:
- Clean data
- Reproducible transformations
- Auditable Logic
- Scalable storage

### Tech Stack 

This project uses an intentionally lightweight tech stack, these components were chosen to reflect real data engineering practices while keeping the pipeline easy to run locally.

- **Languages**: Python 3.12+
- **Core Libraries**:
  - pandas (Data handling)
  - pyarrow (Parquet engine + Snappy compression)
  - pyyaml (Configuration loading)
  - loguru (Structured logging)
  - pathlib (filesystem-safe path handling)
  - python-dotenv (env vars)
  - datetime (Timestamp parsing & time-based feature engineering)
 
- **Architecture & Design**
  - Config-driven ETL (YAML-based paths and settings)
  - Modular pipeline (Extract -> Transform -> Load)
  - Centralised logging with rotation, retention, compression
  - Partitioned data lake output (year/month/day folders)
  - Rule-based fraud detection (high-value, odd-hour, merchant anomaly)
  - Feature engineering layer (hour, day-of-week, weekend)
  - Error-handled orchestration in ```main.py```
 
- **Data Formats**
  - CSV
  - Parquet with Snappy compression

- **Development Environment**
  - Visual Studio Code
  - Virtual environment

I have intentionally avoided heavyweight tools such as Spark, Airflow becaause they add complexity without improving the learning outcome, they require cloud infrastructure that stop this project from running locally. The architecture I have used is ready for this next stage. YAML config is Airflow friendly, the Parquet partitions is Spark compatible and the modular ETL is easy to contain.

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

2. Create & activate virtual environment
  Windows:
  ```powershell
  python -m venv .venv
  .\.venv\Scripts\Activate.ps1
  ```

  macOS / Linux
  ```Bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

3. Install dependencies:
  ```powershell
  python -m pip install --upgrade pip
  pip install -r requirements.txt
  ```
4. Configure your paths
   Edit config/config.yaml to point to:
   - the raw CSV input file
   - the output directory for processed Parquet partitions
   
  ```Yaml
  paths:
    raw: "data/raw/transactions.csv"
    processed: "data/processed/"
  ```

5. Run the ETL pipeline
   
```Bash
python src/main.py
```

This pipeline will:
- Extract the raw CSV
- Clean and enrich the data
- Apply rule-based fraud checks
- Write partitioned Parquet files to the output directory
- Log all activity to ```logs/pipeline.log```




### Licensing: 
MIT License - you are free to fork/use as inspiration.
