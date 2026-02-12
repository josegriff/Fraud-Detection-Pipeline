"""
This script is the coordinator for the ETL process:
1. Load configuration and set up logging
2. Extract raw transaction data
3. Transform and enrich the dataset
4. Load partitioned Parquet output into the data lake
"""

from utils.logger import logger
from utils.config_loader import load_config

from extract.extract import extract_transactions
from transform.transform import transform_transaction
from load.load import load_transaction


def run_pipeline(config_path: str = "config/config.yaml") -> None:
    logger.info("Starting Fraud Detection ETL Pipeline")

    # Load config
    try:
        config = load_config(config_path)
        print("CONFIG LOADED:", config)
        
        logger.info(f"[ORCHESTRATION] Loaded configuration from {config_path}")
    except Exception as e:
        logger.error(f"[ORCHESTRATION] Failed to load configuration: {e}")
        raise

    raw_path = config["paths"]["raw"]
    processed_path = config["paths"]["processed"]

    # Extract
    try:
        df_raw = extract_transactions(raw_path)
    except Exception as e:
        logger.error(f"[ORCHESTRATION] Extract step failed: {e}")
        raise

    # Transform
    try:
        df_transformed = transform_transaction(df_raw)
    except Exception as e:
        logger.error(f"[ORCHESTRATION] Transform step failed: {e}")
        raise

    # Load
    try:
        load_transaction(df_transformed, processed_path)
        logger.info("[ORCHESTRATION] Load step completed successfully")
    except Exception as e:
        logger.error(f"[ORCHESTRATION] Load step failed: {e}")
        raise

    logger.success("ETL Pipeline completed successfully")

if __name__ == "__main__":
    run_pipeline()