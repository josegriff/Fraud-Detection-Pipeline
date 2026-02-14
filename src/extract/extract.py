"""
This script handles the [EXTRACT] phase of the ETL process:
1. Reads the raw transaction CSV file from the specified input path
2. Strip whitespace, convert to lowercase, replace spaces with underscores
3. Validates that all required core columns are present, raises error if any are missing
4. Logs warning if extra/unexpected columns are found
5. Selects and reorders columns: required columns first, followed by any extras
6. Converts the transaction timestamp to proper datetime format
7. Return a cleaned and validated pandas DataFrame readu for the [TRANSFORM] step
"""

from utils.logger import logger
import pandas as pd

required_columns = [
    "trans_num",
    "trans_date_trans_time",
    "amt",
    "merchant",
    "category",
    "is_fraud"
]

def extract_transactions(input_path: str) -> pd.DataFrame:
    logger.info(f"[EXTRACT] Reading CSV from {input_path}")
    
    try: 
        df = pd.read_csv(input_path).head(500)
    except Exception as e:
        logger.error(f"Error reading CSV: {e}")
        raise
    
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )
    
    logger.info(f"[EXTRACT] Columns after normalisation: {list(df.columns)}")
    
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        logger.error(f"[EXTRACT] Missing required columns: {missing}")
        raise ValueError(f"Missing required columns: {missing}")
        
    extra = [col for col in df.columns if col not in required_columns]
    if extra:
        logger.warning(f"[EXTRACT] Extra columns detected: {extra}")
    
    df = df[required_columns + extra]
    
    df["trans_date_trans_time"] = pd.to_datetime(df["trans_date_trans_time"])
    
    logger.info(f"[EXTRACT] Successfully extracted {len(df)} rows")
    return df
    