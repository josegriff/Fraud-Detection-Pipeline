from utils.logger import logger
import pandas as pd


def transform_transaction(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("[TRANSFORM] Starting transformation process")

    # Basic type conversion & cleaning
    df["amt"] = df["amt"].astype(float)
    df["is_fraud"] = df["is_fraud"].astype(int)

    # Time-based features 
    df["trans_date_trans_time"] = pd.to_datetime(df["trans_date_trans_time"])
    df["transaction_hour"] = df["trans_date_trans_time"].dt.hour
    df["transaction_day_of_week"] = df["trans_date_trans_time"].dt.dayofweek
    df["is_weekend"] = df["transaction_day_of_week"].isin([5, 6]).astype(int)

    logger.info("[TRANSFORM] Added time-based features")

    # Fraud indicator flags:
     
    # High value transaction
    df["flag_high_value"] = (df["amt"] > 2000).astype(int)

    # Merchant/category anomaly
    df["flag_merchant_anomaly"] = (
    df.groupby(["cc_num", "category"])["amt"]
    .transform("count")
    .eq(1)
    .astype(int)
)
    
    # Unusual/late-night transaction
    df["flag_odd_hour"] = df["transaction_hour"].isin([0, 1, 2, 3, 4, 5]).astype(int)  

    logger.info("[TRANSFORM] Applied fraud rules and flags")
    
    logger.info(f"[TRANSFORM] Transformation complete. Output rows: {len(df)}")
    
    final_columns= [
        # Columns from original CSV
        "trans_date_trans_time", "cc_num", "merchant", "category", "amt",
        "city", "state", "zip", "lat", "long", "job", "dob", "trans_num",
        "unix_time", "merch_lat", "merch_long", "is_fraud",
        # New engineered columns
        "transaction_hour", "transaction_day_of_week", "is_weekend",
        "flag_high_value", "flag_merchant_anomaly", "flag_odd_hour"
    ]

    # Only keep columns that actually exist (Safety net against missing columns)
    existing_final = [col for col in final_columns if col in df.columns]
    df = df[existing_final]
    
    return df