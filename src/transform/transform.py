from utils.logger import logger
import pandas as pd

def transform_transaction(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("[TRANSFORM] Starting transformation process")
    
    try:
        df["amt"] = df["amt"].astype(float)
        logger.info("[TRANSFORM] Converted amount column to float")
    except Exception as e:
        logger.error(f"[TRANSFORM] Failed to convert amount column: {e}")
        raise
    
    df["is_fraud"] = df["is_fraud"].astype(int)
    
    df["transaction_hour"] = df["trans_date_trans_time"].dt.hour
    df["transaction_day_of_week"] = df["trans_date_trans_time"].dt.dayofweek
    df["is_weekend"] = df["transaction_day_of_week"].isin([5, 6]).astype(int)
    
    logger.info("[TRANSFORM] Added time-based features")
    
    df["flag_high_value"] = (df["amt"] > 2000).astype(int)
    
    logger.info("[TRANSFORM] Applied basic fraud rules")
    
    logger.info(f"[TRANSFORM] Transformation complete. Output rows: {len(df)}")
    return df