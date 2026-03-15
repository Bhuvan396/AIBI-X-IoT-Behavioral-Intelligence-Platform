import os
import pandas as pd
import numpy as np

TRUST_CSV_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/trust_scores.csv'))

class TrustEngine:
    def __init__(self):
        pass

    def compute_policy_score(self, current_features, baseline_data):
        """
        Calculates PolicyScore between 0 and 100 based on:
        - Communication with unknown IP (excessive destinations)
        - Unexpected port usage (shannon entropy/port count)
        - Excessive destination diversity
        """
        score = 0.0
        
        # 1. Unexpected Port Usage / Entropy
        if 'port_entropy' in current_features and 'port_entropy_mean' in baseline_data:
            dev = abs(current_features['port_entropy'] - baseline_data['port_entropy_mean'])
            if dev > 0.5: # Significant entropy shift
                score += 30
                
        # 2. Destination Diversity
        if 'unique_destinations' in current_features and 'unique_destinations_mean' in baseline_data:
            ratio = current_features['unique_destinations'] / (baseline_data['unique_destinations_mean'] + 1)
            if ratio > 2.0: # Double the expected destinations
                score += 40
                
        # 3. Connection Frequency Spikes
        if 'connection_frequency' in current_features:
            # Baseline connection frequency not explicitly in baseline.csv yet, using a heuristic
            if current_features['connection_frequency'] > 5.0: # > 5 packets/sec average in window
                score += 30
                
        return min(100.0, score)

    def compute_trust(self, device_id, drift_score, attack_score, current_features, baseline_data):
        """
        New Formula (Upgrade 4):
        RiskScore = 0.35 * DriftScore + 0.25 * PolicyScore + 0.40 * AttackScore
        TrustScore = 100 - RiskScore
        """
        policy_score = self.compute_policy_score(current_features, baseline_data)
        
        risk_score = (
            0.35 * drift_score +
            0.25 * policy_score +
            0.40 * attack_score
        )
        
        risk_score = min(100.0, max(0.0, risk_score))
        trust_score = 100.0 - risk_score
        
        self.log_trust(device_id, trust_score, drift_score, attack_score, policy_score)
        
        return {
            "trust_score": float(trust_score),
            "risk_score": float(risk_score),
            "policy_score": float(policy_score)
        }

    def log_trust(self, device_id, trust_score, drift, attack, policy):
        file_exists = os.path.exists(TRUST_CSV_PATH)
        timestamp = pd.Timestamp.now(tz='UTC').isoformat()
        import csv
        with open(TRUST_CSV_PATH, 'a', newline='') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["timestamp", "device_id", "trust_score", "drift_score", "attack_score", "policy_score"])
            writer.writerow([timestamp, device_id, trust_score, drift, attack, policy])
