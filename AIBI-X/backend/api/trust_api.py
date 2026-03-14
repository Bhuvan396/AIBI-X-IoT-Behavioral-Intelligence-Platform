from fastapi import APIRouter
import pandas as pd
import os

router = APIRouter()
from realtime.prediction_memory import PREDICTION_HISTORY_PATH

@router.get("/api/trend/{device_id}")
def get_trend_api(device_id: str):
    if not os.path.exists(PREDICTION_HISTORY_PATH):
        return {
            "timestamps": [],
            "trust_scores": [],
            "drift_scores": [],
            "slow_poison_scores": []
        }
    
    df = pd.read_csv(PREDICTION_HISTORY_PATH)
    # Filter for device and get last 20 points
    history = df[df['device_id'] == device_id].tail(20)
    
    if history.empty:
         return {
            "timestamps": [],
            "trust_scores": [],
            "drift_scores": [],
            "slow_poison_scores": []
        }
    
    # Map digital_twin_deviation to drift_scores as requested
    return {
        "timestamps": history['timestamp'].tolist(),
        "trust_scores": history['trust_score'].tolist(),
        "drift_scores": history['digital_twin_deviation'].tolist(),
        "slow_poison_scores": history['slow_poison_score'].tolist()
    }

@router.get("/behavioral_trend/{device_id}")
def get_behavioral_trend(device_id: str):
    if not os.path.exists(PREDICTION_HISTORY_PATH):
        return []
    
    import json
    df = pd.read_csv(PREDICTION_HISTORY_PATH)
    # Filter for device and get last 20 points
    history = df[df['device_id'] == device_id].tail(20)
    
    return json.loads(history.to_json(orient='records'))

@router.get("/trust/history/{device_id}")
def get_trust_history(device_id: str):
    return get_behavioral_trend(device_id)
