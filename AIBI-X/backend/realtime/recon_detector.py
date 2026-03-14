"""
Reconnaissance Detector — behavioral pattern detection using:
  50% Destination Repetition
  30% Border Behavior (entropy + port scan signals)
  20% Historical Recon Predictions
"""
from realtime.prediction_memory import get_device_history


def compute_recon_score(
    device_id: str,
    features: dict,
    baseline: dict
) -> float:
    """
    ReconScore = 0.50 * DestinationRepetition
              + 0.30 * BorderBehavior
              + 0.20 * HistoricalReconPredictions
    """
    # 1. Destination Repetition & Diversity (50%)
    unique_dst = features.get('unique_destinations', 0)
    unique_ports = features.get('unique_dst_ports', 0)
    
    # High unique destinations = scanning behavior
    baseline_dst = baseline.get('unique_destinations_mean', 2)
    dst_ratio = unique_dst / max(baseline_dst, 1)
    # Normalize: if 5x baseline destinations, score = 100
    dst_score = min(100.0, (dst_ratio / 5.0) * 100)
    
    # 2. Border Behavior (30%)
    port_entropy = features.get('port_entropy', 0)
    baseline_entropy = baseline.get('port_entropy_mean', 0.5)
    
    # High entropy = scanning many ports
    entropy_ratio = port_entropy / max(baseline_entropy, 0.1)
    entropy_score = min(100.0, (entropy_ratio / 3.0) * 100)
    
    # Short connection durations are also recon signals
    avg_duration = features.get('avg_duration', 1.0)
    duration_score = max(0, 100 - avg_duration * 50)  # Very short = high score
    
    border_score = 0.6 * entropy_score + 0.4 * duration_score

    # 3. Historical Recon Predictions (20%)
    history = get_device_history(device_id, last_n=20)
    recon_count = sum(
        1 for h in history 
        if str(h.get('predicted_attack', '')).lower() == 'recon'
    )
    historical_score = min(100.0, (recon_count / max(len(history), 1)) * 100)

    score = 0.50 * dst_score + 0.30 * border_score + 0.20 * historical_score
    return min(100.0, max(0.0, score))
