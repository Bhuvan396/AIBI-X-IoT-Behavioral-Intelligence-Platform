import os
import pandas as pd
import joblib
import numpy as np
import shap
from datetime import datetime
from core.feature_extraction import extract_features
from realtime.drift_engine import DriftEngine
from realtime.trust_engine import TrustEngine

MODELS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../models'))
TELEMETRY_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/telemetry.csv'))
DEVICES_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/devices.csv'))

class RealtimePipeline:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RealtimePipeline, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self.drift_engine = DriftEngine()
        self.trust_engine = TrustEngine()
        self.load_models()
        self.explainer = None
        self._initialized = True

    def load_models(self):
        try:
            # Check if models exist before loading
            required = ['scaler.pkl', 'anomaly_model.pkl', 'attack_classifier.pkl', 'label_encoder.pkl']
            for f in required:
                if not os.path.exists(os.path.join(MODELS_DIR, f)):
                    print(f"Error: {f} missing in {MODELS_DIR}")
                    return

            self.scaler = joblib.load(os.path.join(MODELS_DIR, 'scaler.pkl'))
            self.anomaly_model = joblib.load(os.path.join(MODELS_DIR, 'anomaly_model.pkl'))
            self.classifier = joblib.load(os.path.join(MODELS_DIR, 'attack_classifier.pkl'))
            self.le = joblib.load(os.path.join(MODELS_DIR, 'label_encoder.pkl'))
            
            # Using shap.Explainer as it's more generic if TreeExplainer fails
            try:
                self.explainer = shap.TreeExplainer(self.classifier)
            except:
                self.explainer = shap.Explainer(self.classifier)
            print("ML Models and SHAP Explainer loaded successfully.")
        except Exception as e:
            print(f"Critical Error loading models: {e}")

    def get_device_age(self, device_id):
        if os.path.exists(DEVICES_PATH):
            df = pd.read_csv(DEVICES_PATH)
            dev = df[df['device_id'] == device_id]
            if not dev.empty and 'manufacturing_date' in dev.columns:
                m_date = pd.to_datetime(dev.iloc[0]['manufacturing_date'])
                age_years = (pd.Timestamp.now() - m_date).days / 365.25
                return age_years
        return None

    def run_inference(self, device_id):
        if not os.path.exists(TELEMETRY_PATH):
            return None

        # Read only the necessary data if possible, but for simplicity read all
        # In a real system, we'd use a database or a tail reading
        df = pd.read_csv(TELEMETRY_PATH)
        if df.empty:
            return None
            
        # Standardize timestamp parsing to handle mixed formats from old data
        df['timestamp'] = pd.to_datetime(df['timestamp'], utc=True, errors='coerce')
        df = df.dropna(subset=['timestamp'])
        
        # Use a 3-minute window for feature extraction stability, 
        # but triggered every 30s by scheduler.
        eval_window = pd.Timestamp.now(tz='UTC') - pd.Timedelta(minutes=3)
        device_df = df[(df['device_id'] == device_id) & (df['timestamp'] > eval_window)]
        
        if device_df.empty:
            return None

        # 1. Feature Extraction
        features = extract_features(device_df)
        if not features: return None

        feature_names = [
            'traffic_volume', 'packet_count', 'unique_destinations', 'unique_dst_ports',
            'port_entropy', 'avg_packet_size', 'flow_count', 'avg_duration', 
            'periodicity_score', 'tcp_ratio', 'connection_frequency'
        ]
        X = np.array([[features.get(f, 0.0) for f in feature_names]])
        
        try:
            X_scaled = self.scaler.transform(X)
        except Exception as e:
            print(f"Scaler transformation error: {e}")
            return None

        # 2. ML Inference
        raw_anomaly_score = -self.anomaly_model.decision_function(X_scaled)[0]
        
        probas = self.classifier.predict_proba(X_scaled)[0]
        class_names = self.le.classes_
        attack_breakdown = {str(name): float(prob) * 100 for name, prob in zip(class_names, probas)}
        
        attack_probs_only = {k: v for k, v in attack_breakdown.items() if k != 'normal'}
        final_attack_score = max(attack_probs_only.values()) if attack_probs_only else 0.0
        
        pred_idx = np.argmax(probas)
        attack_type = str(class_names[pred_idx])

        # 3. Drift Detection
        drift_score = float(self.drift_engine.calculate_drift(device_id, features))

        # 4. Trust Score
        baseline_data = self.drift_engine.baselines.get(device_id, {})
        trust_results = self.trust_engine.compute_trust(
            device_id, drift_score, final_attack_score, features, baseline_data
        )

        # 5. SHAP Explanations
        feature_importance = {}
        if self.explainer:
            try:
                # Use pred_idx to get explanation for the winning class
                sv = self.explainer.shap_values(X_scaled)
                # sv is list of arrays for multi-class
                class_shap = sv[pred_idx] if isinstance(sv, list) else sv[0]
                if len(class_shap.shape) > 1: class_shap = class_shap[0]
                
                for i, name in enumerate(feature_names):
                    feature_importance[name] = float(class_shap[i])
            except Exception as e:
                print(f"SHAP explanation omitted due to error: {e}")

        # 6. Device Context
        device_age = self.get_device_age(device_id)

        return {
            "device_id": device_id,
            "timestamp": pd.Timestamp.now(tz='UTC').isoformat(),
            "features": features,
            "baseline": baseline_data,
            "drift_score": drift_score,
            "anomaly_score": float(raw_anomaly_score),
            "attack_type": attack_type,
            "attack_breakdown": attack_breakdown,
            "final_attack_score": float(final_attack_score),
            "feature_importance": feature_importance,
            "device_age": device_age,
            "trust_score": float(trust_results['trust_score']),
            "risk_score": float(trust_results['risk_score']),
            "policy_score": float(trust_results['policy_score'])
        }
