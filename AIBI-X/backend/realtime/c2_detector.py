"""
C2 Beaconing Detector — identifies heartbeat patterns using:
- periodicity_score (low variance in time intervals)
- destination repetition (contacting same IP)
- packet size consistency (small packets)
"""
import numpy as np
from realtime.prediction_memory import get_device_history

def compute_c2_score(device_id: str, features: dict, baseline: dict) -> float:
    score = 0.0
    
    # 1. Periodicity Analysis
    periodicity = features.get('top_ip_periodicity', features.get('periodicity_score', 0.0))
    if periodicity > 0.6:
        score += 50
    elif periodicity > 0.3:
        score += 25
        
    # 2. Destination Repetition
    repetition = features.get('destination_repetition_score', 0.0)
    if repetition > 0.8:
        score += 60  # Major indicator
    elif repetition > 0.5:
        score += 30
        
    # 3. Packet Size Consistency (C2 usually uses small packets)
    avg_size = features.get('avg_packet_size', 0.0)
    if 50 < avg_size < 500:
        score += 20
    
    # 4. Historical Trends
    history = get_device_history(device_id, last_n=10)
    c2_history_count = sum(1 for h in history if str(h.get('predicted_attack', '')).lower() == 'c2_beaconing')
    if c2_history_count >= 2:
        score += 10

    return min(100.0, score)
