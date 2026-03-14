"""
Slow Poison Detector — trend-based detection using:
  70% baseline drift
  20% digital twin deviation
  10% historical predictions
"""
from realtime.prediction_memory import get_device_history


def compute_slow_poison_score(
    device_id: str,
    features: dict,
    baseline: dict,
    digital_twin_deviation: float
) -> float:
    """
    SlowPoisonScore = 0.70 * BaselineDriftTrend
                    + 0.20 * DigitalTwinDeviationTrend
                    + 0.10 * HistoricalSlowPoison
    """
    # 1. Baseline Drift Trend (70%)
    drift_signals = 0
    drift_checks = 0
    feature_map = {
        'traffic_volume': 'traffic_volume_mean',
        'unique_destinations': 'unique_destinations_mean',
        'port_entropy': 'port_entropy_mean',
    }
    
    for feat, base_key in feature_map.items():
        current = features.get(feat, 0)
        mean_val = baseline.get(base_key, 0)
        std_val = baseline.get('traffic_volume_std', 1.0)
        if std_val == 0:
            std_val = 1.0
        
        drift_checks += 1
        # Rule: feature_value > baseline_mean + 0.7 * baseline_std
        if current > mean_val + 0.7 * std_val:
            drift_signals += 1
    
    baseline_drift = (drift_signals / max(drift_checks, 1)) * 100

    # 2. Digital Twin Deviation (20%) — already computed, scale to 0-100
    twin_component = min(100.0, digital_twin_deviation)

    # 3. Historical Slow Poison Predictions (10%)
    history = get_device_history(device_id, last_n=20)
    slow_poison_count = sum(
        1 for h in history 
        if str(h.get('predicted_attack', '')).lower() in ('slow_poisoning', 'slow_poison')
    )
    historical_score = min(100.0, (slow_poison_count / max(len(history), 1)) * 100)

    score = 0.70 * baseline_drift + 0.20 * twin_component + 0.10 * historical_score
    return min(100.0, max(0.0, score))
