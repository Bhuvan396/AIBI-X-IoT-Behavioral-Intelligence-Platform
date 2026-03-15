from fastapi import APIRouter
import pandas as pd
import os

router = APIRouter()
TRUST_CSV_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/trust_scores.csv'))

@router.get("/trust/history/{device_id}")
def get_trust_history(device_id: str):
    if not os.path.exists(TRUST_CSV_PATH):
        return []
    
    import json
    df = pd.read_csv(TRUST_CSV_PATH)
    history = df[df['device_id'] == device_id].tail(20)
    
    # Use pandas to_json helper as it handles numpy types correctly
    return json.loads(history.to_json(orient='records'))
