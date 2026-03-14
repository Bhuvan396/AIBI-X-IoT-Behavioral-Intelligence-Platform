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
        "trust_score": result.get('trust_score', 100.0),
        "last_anomaly_score": result.get('anomaly_score', 0.0),
        "predicted_attack_type": result.get('attack_type', 'normal'),
        "attack_probability": result.get('final_attack_score', 0.0),
        "attack_breakdown": result.get('attack_breakdown', {}),
        "policy_score": result.get('policy_score', 0.0),
        "drift_score": result.get('drift_score', 0.0),
        "digital_twin_deviation": result.get('digital_twin_deviation', 0.0),
        "slow_poison_score": result.get('slow_poison_score', 0.0),
        "recon_score": result.get('recon_score', 0.0),
        "impersonation_score": result.get('impersonation_score', 0.0),
        "adversarial_score": result.get('adversarial_score', 0.0),
        "future_risk": result.get('future_risk', 0.0),
        "predicted_trust_2min": result.get('predicted_trust_2min', result.get('trust_score', 100.0)),
        "trend_data": result.get('trend_data', {}),
        "age_factor": result.get('age_factor', 0.0)
    }

@router.post("/analyze_now")
def analyze_now(req: AnalyzeRequest):
    """
    Upgrade 2: Instant analysis button trigger.
    Runs pipeline immediately and returns the latest state.
    """
    try:
        result = pipeline.run_inference(req.device_id)
        if not result:
            raise HTTPException(status_code=404, detail="No telemetry available for immediate analysis")
        return result
    except Exception as e:
        import traceback
        err = traceback.format_exc()
        raise HTTPException(status_code=500, detail=str(err))
