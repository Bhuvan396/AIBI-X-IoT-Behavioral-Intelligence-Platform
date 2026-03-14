"""
Adversarial ML Evasion Detector — detects attackers attempting
to evade ML models by staying near decision boundaries.
"""
import numpy as np


def compute_adversarial_score(
    anomaly_score: float,
    attack_breakdown: dict,
    features: dict,
    baseline: dict
) -> float:
    """
    Detect adversarial evasion attempts by looking for:
    1. Features near anomaly decision boundary
    2. Inconsistent feature correlations
    3. Multiple classes with similar probabilities (confusion attack)
    """
    signals = 0.0
    weight_total = 0.0
    
    # 1. Boundary proximity (40%)
    # If anomaly score is close to 0 (the decision boundary), suspicious
    boundary_distance = abs(anomaly_score)
    if boundary_distance < 0.3:
        # Very close to boundary = highly suspicious
        boundary_score = (1.0 - boundary_distance / 0.3) * 100
    else:
        boundary_score = 0.0
    signals += 0.40 * boundary_score
    weight_total += 0.40
    
    # 2. Classification confusion (30%)
    # If multiple attack classes have similar probabilities, attacker may be
    # crafting features to confuse the classifier
    probs = sorted(attack_breakdown.values(), reverse=True)
    if len(probs) >= 2:
        top_two_diff = probs[0] - probs[1]
        if top_two_diff < 15:  # Less than 15% difference between top 2 classes
            confusion_score = (1.0 - top_two_diff / 15.0) * 100
        else:
            confusion_score = 0.0
    else:
        confusion_score = 0.0
    signals += 0.30 * confusion_score
    weight_total += 0.30
    
    # 3. Feature correlation inconsistency (30%)
    # Normal traffic: high traffic_volume correlates with high packet_count
    # Adversarial: may have high volume but low packet count (or vice versa)
    tv = features.get('traffic_volume', 0)
    pc = features.get('packet_count', 1)
    avg_ps = features.get('avg_packet_size', 0)
    
    # Check if avg_packet_size is absurdly high or low
    if avg_ps > 50000 or (avg_ps < 10 and pc > 50):
        correlation_score = 80.0
    elif tv > 100000 and pc < 10:
        correlation_score = 90.0
    else:
        correlation_score = 0.0
    signals += 0.30 * correlation_score
    weight_total += 0.30
    
    return min(100.0, max(0.0, signals))
