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
        df = pd.read_csv(input_path)
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
    