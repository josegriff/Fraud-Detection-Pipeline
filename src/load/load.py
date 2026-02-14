"""
This script handles the [LOAD] phase of the ETL process:
1. Receives the transformed DataFrame from the previous step
2. Defines and enforces the exact set of columns to be persisted (matches transform output)
3. Performs safety checks: ensures columns exist and the partitioning column is present
4. Adds a daily partition key based on transaction date
5. Groups data by day and writes each group as a partitioned Parquet file
   (path structure: year=YYYY/month=MM/day=DD/transactions.parquet)
6. Uses snappy compression for efficient storage
7. Logs detailed progress including number of rows per partition and total partitions written
8. Completes the ETL pipeline by saving cleaned, enriched data to the data lake
"""

from utils.logger import logger
from pathlib import Path
import pandas as pd

def load_transaction(df: pd.DataFrame, base_path: str) -> None:
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

    # Apply filter once and early
    df = df[persist_columns].copy()

    # Quick sanity check
    # Vital column for partitioning
    if "trans_date_trans_time" not in df.columns:
        logger.error("[LOAD] Missing required column 'trans_date_trans_time' – cannot partition")
        return

    # Create partition key
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
        )

        written_count += 1
        logger.info(f"[LOAD] Wrote partition: {output_file} ({len(group_df)} rows)")

    logger.info(f"[LOAD] Partitioned load completed – {written_count} daily partitions written")