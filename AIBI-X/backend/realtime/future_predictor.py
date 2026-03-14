"""
Future Prediction Engine — predicts future trust score
based on trend analysis over last 5-10 prediction windows.

FutureRisk = 0.35 * TrustTrend
           + 0.25 * FeatureDriftTrend
           + 0.20 * DigitalTwinDeviationTrend
           + 0.10 * SlowPoisonTrend
           + 0.10 * AnomalyTrend
"""
import numpy as np
from realtime.prediction_memory import get_device_history


def compute_future_risk(device_id: str, current_trust: float) -> dict:
    """
    Predict future risk and projected trust score using linear regression.
    Step 1: Load prediction history (last 10 records).
    Step 2: Compute trust trend using linear regression.
    Step 3: Forecast future trust (4 windows ahead approx 2 min).
    Step 4: Compute future risk (100 - future_trust).
    """
    history = get_device_history(device_id, last_n=10)
    
    # Extract trust scores
    historic_trusts = [float(h.get('trust_score', 0) or 100) for h in history]
    # Add current trust as the latest point
    trust_scores = historic_trusts + [float(current_trust)]
    
    if len(trust_scores) < 2:
        # No history at all, assume flat trend
        future_risk = max(0.0, 100.0 - current_trust)
        return {
            'future_risk': float(future_risk),
            'predicted_trust_2min': float(current_trust),
            'trend_data': {'trust_slope': 0.0, 'windows_available': 0}
        }
    
    # Use linear regression to find the slope
    x = np.arange(len(trust_scores))
    y = np.array(trust_scores)
    
    # slope = np.polyfit(range(len(trust_scores)), trust_scores, 1)[0]
    slope, _ = np.polyfit(x, y, 1)
    
    # Forecast future trust: 4 windows ahead (~2 minutes)
    future_trust = trust_scores[-1] + (slope * 4)
    future_trust = min(100.0, max(0.0, future_trust))
    
    # Compute future risk
    future_risk = max(0.0, (100.0 - future_trust))
    
    return {
        'future_risk': float(future_risk),
        'predicted_trust_2min': float(future_trust),
        'trend_data': {
            'trust_slope': float(slope),
            'windows_available': len(history)
        }
    }
