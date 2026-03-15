from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import pandas as pd
import os
import json
from realtime.realtime_pipeline import RealtimePipeline

router = APIRouter()
pipeline = RealtimePipeline()
DEVICES_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/devices.csv'))

class AnalyzeRequest(BaseModel):
    device_id: str

@router.get("/devices")
def get_devices():
    if not os.path.exists(DEVICES_PATH):
        return []
    df = pd.read_csv(DEVICES_PATH)
    return json.loads(df.to_json(orient='records'))

@router.get("/device/{device_id}/status")
def get_device_status(device_id: str):
    # Run the real-time pipeline for this device to get latest state
    result = pipeline.run_inference(device_id)
    if not result:
        return {
            "device_id": device_id,
            "trust_score": 100.0,
            "last_anomaly_score": 0.0,
            "predicted_attack_type": "normal",
            "attack_probability": 0.0,
            "attack_breakdown": {},
            "policy_score": 0.0
        }
    
    return {
        "device_id": device_id,
        "trust_score": result['trust_score'],
        "last_anomaly_score": result['anomaly_score'],
        "predicted_attack_type": result['attack_type'],
        "attack_probability": result['final_attack_score'],
        "attack_breakdown": result['attack_breakdown'],
        "policy_score": result['policy_score'],
        "drift_score": result['drift_score']
    }

@router.post("/analyze_now")
def analyze_now(req: AnalyzeRequest):
    """
    Upgrade 2: Instant analysis button trigger.
    Runs pipeline immediately and returns the latest state.
    """
    result = pipeline.run_inference(req.device_id)
    if not result:
        raise HTTPException(status_code=404, detail="No telemetry available for immediate analysis")
    
    return result
