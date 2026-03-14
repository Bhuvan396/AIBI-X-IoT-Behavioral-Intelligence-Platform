import pandas as pd
import numpy as np
import os

BASELINE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/baseline.csv'))

class DriftEngine:
    def __init__(self):
        self.baselines = {}
        self.load_baselines()

    def load_baselines(self):
        if os.path.exists(BASELINE_PATH):
            df = pd.read_csv(BASELINE_PATH)
            for _, row in df.iterrows():
                self.baselines[row['device_id']] = row.to_dict()

    def calculate_drift(self, device_id, current_features):
        if device_id not in self.baselines:
            return 50.0 # Unknown device, neutral drift
        
        base = self.baselines[device_id]
        deviations = []
        
        # Z-score based drift for key features
        feature_map = {
            'traffic_volume': 'traffic_volume_mean',
            'unique_destinations': 'unique_destinations_mean',
            'port_entropy': 'port_entropy_mean',
            'periodicity_score': 'periodicity_mean'
        }
        
        for feat, base_feat in feature_map.items():
            current_val = current_features.get(feat, 0)
            mean_val = base.get(base_feat, 0)
            std_val = base.get('traffic_volume_std', 1.0) # Using volume std as proxy or 1.0
            
            if std_val == 0: std_val = 1.0
            
            z_score = abs(current_val - mean_val) / std_val
            # Normalize z-score to a 0-100 scale (clamping at z=3 for max drift)
            dev = min(100, (z_score / 3.0) * 100)
            deviations.append(dev)
            
        drift_score = np.mean(deviations) if deviations else 0.0
        return float(drift_score)
