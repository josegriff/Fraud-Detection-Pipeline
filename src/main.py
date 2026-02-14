"""
This script is the orchestrator for the ETL process.
It ties together Extraction, Transformation, and Loading in the stated order,
handles error at each step, and logs progress clearly

Steps:
1. Loads configuration (paths, settings) from YAML
2. Extract raw transaction data from CSV
3. Applies cleaning, feature engineering, and fraud flags
4. Saves the enriched data as daily-partitioned Parquet files
"""

from utils.logger import logger
from utils.config_loader import load_config

from extract.extract import extract_transactions
from transform.transform import transform_transaction
from load.load import load_transaction


def run_pipeline(config_path: str = "config/config.yaml") -> None:
    logger.info("Starting Fraud Detection ETL Pipeline")

    # Load configuration
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

    # Load to partitioned Parquet files
    try:
        logger.info(f"[ORCHESTRATION] Loading transformed data to {processed_path}")
        load_transaction(df_transformed, processed_path)
        
        # Show data flow health
        row_count_raw = len(df_raw)
        row_count_transformed = len(df_transformed)
        logger.info(
            f"[ORCHESTRATION] Processed {row_count_raw:,} raw -> "
            f"{row_count_transformed:,} transformed rows"
            )
        
        logger.info("[ORCHESTRATION] Load step completed successfully")
    except Exception as e:
        logger.error(f"[ORCHESTRATION] Load step failed: {e}")
        raise

    # Pipeline finished
    logger.info("[ORCHESTRATION] ETL Pipeline completed successfully")

if __name__ == "__main__":
    run_pipeline()