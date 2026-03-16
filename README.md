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
- Runs as modular, config-driven ETL pipeline ready for orchestration (Airflow) and cloud deployment (AWS S3 and Athena)

Instead of focusing on machine learning, this project is to display skills in the core engineering layer that fradu systems can rely on:
- Clean data
- Reproducible transformations
- Auditable Logic
- Scalable storage

### Roadmap

**Stage 1: Project Setup and Environment**
- Create repository and folder structure (```src/```, ```config/```, ```data```, ```utils```, etc.)
- Set up virtual environment and reproducible ```requirements.txt.```
- Verify imports, logging, and basic environment behaviour

**Stage 2: Config-driven Architecture**
- Introduce YAML configuration (```config/config.yaml```)
- Implement ```config_loader.py``` for safe, reusable config access
- Ensure all paths and setting are externalised

**Stage 3: Extract Module**
- Build ```extract_transactions()``` to ingest raw CSV files
- Normalise column names (strip, lowercase, underscores)
- Implement required-column validation
- Add warnings for unexpected columns
- Convert timestamps to proper datetime format
- Log extraction details and row counts

**Stage 4: Transform Module**
- Implement ```transform_transaction()``` for cleaning and enrichment
- Add type conversions (amount, fraud label)
- Engineer time-based features (hour, weekday, weekend)
- Add rule-based fraud indicators:
  - high-value transaction
  - merchant anomalies
  - odd-hour activity
- Define a controlled output schema
- Log transformation progress and output size

**Stage 5: Load Module**
- Build ```load_transaction()``` to weite partitioned Parquet files
- Enforce a strict set of persisted columns
- Add safety checks for missing partition keys
- Implement daily partitioning (year/month/day)
- Write Parquet files with Snappy compression
- Log partition paths and row counts

**Stage 6: Centralised Logging System**
- Implement Loguru-based logger with:
  - rotating logs (1 MB)
  - 7 day retention
  - ZIP compression
- Ensure consistent logging across all ETL stages

**Stage 7: Pipeline Orchestration**
- Build ```run_pipeline()``` in ```main.py```
- Connect extract -> transform -> load into a single flow
- Add error handling for each stage
- Log pipeline start, end and data-flow health
- Prepare structure for future orchestration (Airflow)

**Stage 8: Data Lake Output and Validation**
- Verify Parquet output structure
- Confirm partitioning logic
- Ensure compatablility with future AWS S3 and Athena deployment

**Stage 9: Documentation
- Write detailed README with:
  - Project overview
  - Roadmap
  - Tech stack
  - Project Structure
  - Quick start guide
  - Justification of design decisions

**Stage 10: Future Enhancements**
- Add Great Expectations for data quality
- Add Airflow for orchestration
- Containerise with Docker
- Deploy with AWS S3 and Athena
- Add unit tests with pytest
- Add monitoring stubs

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
├── src/                    # All ETL pipeline logic
│   ├── extract/            # Data ingestion (CSV → DataFrame)
│   ├── transform/          # Cleaning and fraud business rules
│   ├── load/               # Partitioned Parquet writer 
│   ├── utils/              # Logging, config loader, helpers
│   ├── main.py             # Pipeline entry point
│   └── init.py
├── config/                 # YAML configs (paths, thresholds, rules)
│   └── config.yaml
├── data/                   # Raw and processed datasets
├── dags/                   # Placeholder for future Airflow orchestration
├── docs/                   # Architecture diagrams, decisions
├── tests/                  # Placeholder for future pytest suite
│    └── __init__.py
├── logs/                   # Rotating Loguru logs
├── requirements.txt        # Reproducible dependencies
└── README.md               #  Project documentation
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

### Design Decisions
This pipeline is designed to intentionally avoids over-engineering while following patterns used for real data platforms. Each decision was made by comparing practical alternatives and choosing the option that delivers the best blance for reliability, clarity and future scalability.

I chose Python and pandas over Spark because this dataset fits comfortably in memory, with pandas providing fast transformations with minimal overhead. Spark adds cluster complexity without performance beenfits at this scale. It slows down iteration for a single-developer project and requires additional infrastructure (executors, schedulers, configs). This pipeline is simple, fast and easy to reason about. However, the way the architecture has been set up, it can scale to Spark at a later date if needed.

I decided to have a modular ETL package instead of a single monolithic script because separating extract/transform/load mirros how production pipelines are structured in Airflow. Additional reasons for this design decision:

- **Harder to test**

Transformations can be unit-tested in isolation with fast, reliable fixtures. Monolithic scripts force     end-to-end tests only, leading to poor coverage and slow feedback loops.

- **Harder to orchestratate**

Orchestration tools like Airflow expect tasks to be independent units. A single script can't be broken into tasks with refactoring, a modular ETL on the other hand directly maps to DAG nodes.

- **Harder to extend**

Adding new rules, data sources or new outputs become messy in a monolithic file. In contrast, a modular ETL lets you extend/replace components without having to rewrite an entire pipeline.

- **Encourages hidden side effects**

Monolithic scripts often rely on shared state or implicit assumptions. A modular ETL forces explicit inputs/outputs, which makes pipelines easier to reason about and safer to modify.

I chose to have YAML configuration driven pipelines over hard-coded paths because I prioritise an agnostic environment over short-term development speed. Hard-coding values ties the logic to one specific setup and creates friction as soon as multiple environments or modest changes appear. I also had conerns over:

- **Breaks when moving between dev/staging/prod**

Paths, buckets, endpoints and credentials differ across environments. Hard-coded values cause immediate failures on promotion; an advantage of YAML configurations is that they allow the same code to run unchanged with environment-specific files. 

- **Forces code changes for simple config tweaks**

Adjusting a path, threshold, retry count or new output requires a full PR/review/deploy cycle even when business logic is untouched. With YAML, we avoid redeploying code with lightweight config-only commits.



### Licensing: 
MIT License - you are free to fork/use as inspiration.
