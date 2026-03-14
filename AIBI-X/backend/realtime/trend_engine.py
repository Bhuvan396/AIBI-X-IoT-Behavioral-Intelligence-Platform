"""
Trend Analysis Engine — computes linear regression slopes
over the last N prediction windows for key metrics.
"""
import numpy as np
from realtime.prediction_memory import get_device_history


def compute_slope(values: list) -> float:
    """Compute linear regression slope over a series of values."""
    if len(values) < 3:
        return 0.0
    x = np.arange(len(values), dtype=float)
    y = np.array(values, dtype=float)
    # Simple linear regression
    n = len(x)
    slope = (n * np.sum(x * y) - np.sum(x) * np.sum(y)) / (n * np.sum(x**2) - np.sum(x)**2 + 1e-10)
    return float(slope)


def get_trends(device_id: str, last_n: int = 10) -> dict:
    """
    Return trend slopes for key metrics over the last N windows.
    Negative slopes for trust = degradation.
    Positive slopes for anomaly = escalation.
    """
    history = get_device_history(device_id, last_n)
    if len(history) < 3:
        return {
            'trust_slope': 0.0,
            'anomaly_slope': 0.0,
            'slow_poison_slope': 0.0,
            'recon_slope': 0.0,
            'twin_deviation_slope': 0.0,
            'adversarial_slope': 0.0,
            'windows_available': len(history)
        }
    
    def safe_extract(key):
        return [float(h.get(key, 0) or 0) for h in history]
    
    return {
        'trust_slope': compute_slope(safe_extract('trust_score')),
        'anomaly_slope': compute_slope(safe_extract('anomaly_score')),
        'slow_poison_slope': compute_slope(safe_extract('slow_poison_score')),
        'recon_slope': compute_slope(safe_extract('recon_score')),
        'twin_deviation_slope': compute_slope(safe_extract('digital_twin_deviation')),
        'adversarial_slope': compute_slope(safe_extract('adversarial_score')),
        'windows_available': len(history)
    }
