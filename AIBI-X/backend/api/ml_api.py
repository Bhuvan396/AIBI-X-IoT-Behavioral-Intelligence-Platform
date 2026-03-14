from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import joblib
import os
import pandas as pd
import numpy as np

router = APIRouter(prefix="/ml")
MODELS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../models'))

FEATURE_ORDER = [
    'traffic_volume', 'packet_count', 'unique_destinations', 'unique_dst_ports',
    'port_entropy', 'avg_packet_size', 'flow_count', 'avg_duration',
    'periodicity_score', 'tcp_ratio', 'connection_frequency',
    'destination_repetition_score', 'time_of_day_activity'
]

class InferenceRequest(BaseModel):
    device_id: str
    features: dict

# Lazy loading of models
models = {}

def get_model(name):
    if name not in models:
        path = os.path.join(MODELS_DIR, f"{name}.pkl")
        if not os.path.exists(path):
            raise HTTPException(status_code=500, detail=f"Model {name} not found. Please run training.")
        models[name] = joblib.load(path)
    return models[name]

@router.post("/anomaly_score")
def get_anomaly_score(req: InferenceRequest):
    scaler = get_model('scaler')
    anomaly_model = get_model('anomaly_model')
    
    vec = [req.features.get(f, 0.0) for f in FEATURE_ORDER]
    X = np.array([vec])
    X_scaled = scaler.transform(X)
    
    score = -anomaly_model.decision_function(X_scaled)[0]
    
    return {"device_id": req.device_id, "anomaly_score": float(score)}

@router.post("/classify_attack")
def classify_attack(req: InferenceRequest):
    scaler = get_model('scaler')
    classifier = get_model('attack_classifier')
    le = get_model('label_encoder')
    
    vec = [req.features.get(f, 0.0) for f in FEATURE_ORDER]
    X = np.array([vec])
    X_scaled = scaler.transform(X)
    
    pred_idx = classifier.predict(X_scaled)[0]
    proba = classifier.predict_proba(X_scaled)[0][pred_idx]
    label = le.inverse_transform([pred_idx])[0]
    
    return {
        "device_id": req.device_id,
        "predicted_attack_type": label,
        "confidence_score": float(proba)
    }

@router.get("/explain_prediction")
def explain_prediction(device_id: str):
    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/explanations.csv'))
    if not os.path.exists(csv_path):
        return {"error": "No explanations found"}
    
    df = pd.read_csv(csv_path)
    device_exps = df[df['device_id'] == device_id]
    if device_exps.empty:
        return {"error": f"No explanations for device {device_id}"}
    
    import json
    latest = device_exps.iloc[-1]
    return json.loads(latest.to_json())
