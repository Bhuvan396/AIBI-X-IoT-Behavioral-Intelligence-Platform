import shap
import joblib
import os
import pandas as pd
import csv
from datetime import datetime

MODELS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../models'))
EXPLANATIONS_CSV_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/explanations.csv'))

class ExplainabilityEngine:
    def __init__(self):
        self.model = joblib.load(os.path.join(MODELS_DIR, 'attack_classifier.pkl'))
        self.scaler = joblib.load(os.path.join(MODELS_DIR, 'scaler.pkl'))
        self.le = joblib.load(os.path.join(MODELS_DIR, 'label_encoder.pkl'))
        self.features = [
            'traffic_volume', 'packet_count', 'unique_destinations', 'unique_dst_ports',
            'port_entropy', 'avg_packet_size', 'flow_count', 'avg_duration', 
            'periodicity_score', 'tcp_ratio', 'connection_frequency'
        ]
        # Use TreeExplainer for XGBoost
        self.explainer = shap.TreeExplainer(self.model)

    def explain(self, device_id, feature_vector):
        # SHAP expects a dataframe if we used feature names in training
        df = pd.DataFrame([feature_vector], columns=self.features)
        shap_values = self.explainer.shap_values(df)
        
        # In multi-class, shap_values is a list of arrays (one per class)
        # We find the predicted class
        pred_idx = self.model.predict(df)[0]
        pred_label = self.le.inverse_transform([pred_idx])[0]
        
        # Get SHAP values for the predicted class
        prediction_shap = shap_values[pred_idx][0]
        
        # Find top feature
        top_feature_idx = prediction_shap.argmax()
        top_feature = self.features[top_feature_idx]
        impact_score = prediction_shap[top_feature_idx]
        
        # Save to csv
        self.log_explanation(device_id, top_feature, impact_score, pred_label)
        
        return {
            "top_feature": top_feature,
            "impact_score": float(impact_score),
            "attack_prediction": pred_label
        }

    def log_explanation(self, device_id, top_feature, impact_score, prediction):
        file_exists = os.path.exists(EXPLANATIONS_CSV_PATH)
        with open(EXPLANATIONS_CSV_PATH, 'a', newline='') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(['device_id', 'timestamp', 'top_feature', 'impact_score', 'attack_prediction'])
            writer.writerow([
                device_id,
                datetime.utcnow().isoformat() + "Z",
                top_feature,
                float(impact_score),
                prediction
            ])
