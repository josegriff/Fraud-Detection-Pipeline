from utils.logger import logger
from pathlib import Path
import pandas as pd
import os

def load_transaction(df: pd.DataFrame, base_path: str) -> None:
    logger.info("Starting partitioned load step...")
    
    df["day_period"] = df["trans_date_trans_time"].dt.to_period("D")
    
    for period, group_df in df.groupby("day_period"):
        year = period.year
        month = period.month
        day = period.day
        
        partition_path = (
            Path(base_path)
            / f"year={year}"
            / f"month={month:02d}"
            / f"day={day:02d}"
        )
        
        os.makedirs(partition_path, exist_ok=True)
        
        clean_df = group_df.drop(columns=["day_period"])
        
        output_file = partition_path / "transactions.parquet"
        
        clean_df.to_parquet(output_file, index=False)
        
        logger.info(f"Wrote partition: {output_file}")
    
    logger.success("Partitioned load step completed successfully!")

def load_transaction(df: pd.DataFrame, base_path: str) -> None:
    """
    Loads the transformed transaction DataFrame into daily partitioned Parquet files.
    
    Expects a DataFrame that has already been processed by transform_transaction().
    Only persists the columns defined in persist_columns.
    """
    logger.info("[LOAD] Starting partitioned load step")

    # Define exactly which columns should be saved 
    # Matches transform intended output
    persist_columns = [
        # Original dataset columns
        "trans_date_trans_time", "cc_num", "merchant", "category", "amt",
        "city", "state", "zip", "lat", "long", "job", "dob", "trans_num",
        "unix_time", "merch_lat", "merch_long", "is_fraud",
        # Engineered columns added by transform.py
        "transaction_hour", "transaction_day_of_week", "is_weekend",
        "flag_high_value", "flag_merchant_anomaly", "flag_odd_hour"
    ]

    # Safety: only keep columns that actually exist in the incoming df
    persist_columns = [col for col in persist_columns if col in df.columns]

    if not persist_columns:
        logger.error("[LOAD] No columns to persist – aborting")
        return

    # Apply filter once (cheaper than doing per partition)
    df = df[persist_columns].copy()

    # Quick sanity check
    # Vital column for partitioning
    if "trans_date_trans_time" not in df.columns:
        logger.error("[LOAD] Missing required column 'trans_date_trans_time' – cannot partition")
        return

    # Create partition key (daily)
    df["day_period"] = df["trans_date_trans_time"].dt.to_period("D")

    written_count = 0

    for period, group_df in df.groupby("day_period"):
        year = period.year
        month = period.month
        day = period.day

        partition_path = (
            Path(base_path)
            / f"year={year}"
            / f"month={month:02d}"
            / f"day={day:02d}"
        )

        partition_path.mkdir(parents=True, exist_ok=True)

        output_file = partition_path / "transactions.parquet"

        # Drop the temporary partition column before writing
        group_df = group_df.drop(columns=["day_period"])

        group_df.to_parquet(
            output_file,
            index=False,
            compression="snappy",      # good balance of size & speed
            # row_group_size=100_000,  # optional – uncomment if you have large days
        )

        written_count += 1
        logger.info(f"[LOAD] Wrote partition: {output_file} ({len(group_df)} rows)")

    logger.info(f"[LOAD] Partitioned load completed – {written_count} daily partitions written")