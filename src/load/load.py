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