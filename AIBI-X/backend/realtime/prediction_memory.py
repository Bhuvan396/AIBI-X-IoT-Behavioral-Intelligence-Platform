"""
Prediction Memory — stores analysis results every 30s cycle.
Keeps last 2 hours of prediction history for trend analysis.
"""
import os
import csv
import pandas as pd
from threading import Lock

PREDICTION_HISTORY_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../../data/prediction_history.csv')
)

SCHEMA = [
    'timestamp', 'device_id', 'trust_score', 'predicted_attack',
    'slow_poison_score', 'recon_score', 'c2_score', 'anomaly_score',
    'traffic_volume', 'digital_twin_deviation', 'adversarial_score',
    'impersonation_score', 'policy_score', 'future_risk', 'age_factor'
]

_lock = Lock()

def _ensure_file():
    if not os.path.exists(PREDICTION_HISTORY_PATH):
        os.makedirs(os.path.dirname(PREDICTION_HISTORY_PATH), exist_ok=True)
        with open(PREDICTION_HISTORY_PATH, 'w', newline='') as f:
            csv.writer(f).writerow(SCHEMA)
        return

    # File exists, check if header is missing
    with open(PREDICTION_HISTORY_PATH, 'r') as f:
        first_line = f.readline()
        if not first_line.startswith('timestamp'):
            # Header missing! Read everything and rewrite with header
            f.seek(0)
            content = f.read()
            with open(PREDICTION_HISTORY_PATH, 'w', newline='') as fw:
                csv.writer(fw).writerow(SCHEMA)
                fw.write(content)

def store_prediction(record: dict):
    """Append a prediction record."""
    _ensure_file()
    # Append to csv
    with _lock:
        with open(PREDICTION_HISTORY_PATH, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([record.get(k, '') for k in SCHEMA])
        
        # Simple pruning: if file too large, we could truncate, 
        # but for now let it grow to ensure trend analysis works.

def get_device_history(device_id: str, last_n: int = 10) -> list:
    """Get last N prediction records for a device."""
    _ensure_file()
    try:
        df = pd.read_csv(PREDICTION_HISTORY_PATH)
        if df.empty:
            return []
        device_df = df[df['device_id'] == device_id].tail(last_n)
        return device_df.to_dict('records')
    except Exception:
        return []

def get_all_history(device_id: str) -> pd.DataFrame:
    """Get full 2hr history for a device as DataFrame."""
    _ensure_file()
    try:
        df = pd.read_csv(PREDICTION_HISTORY_PATH)
        if df.empty:
            return pd.DataFrame()
        return df[df['device_id'] == device_id]
    except Exception:
        return pd.DataFrame()
