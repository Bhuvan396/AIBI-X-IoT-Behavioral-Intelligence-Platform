"""
Realtime Pipeline — the central orchestrator that ties together:
  Feature Extraction → ML Inference → Digital Twin → Detectors → Trust Engine
"""
import os
import pandas as pd
import joblib
import numpy as np
import shap
from core.feature_extraction import extract_features
from realtime.drift_engine import DriftEngine
from realtime.trust_engine import UnifiedTrustEngine
from realtime.digital_twin import DigitalTwin
from realtime.slow_poison_detector import compute_slow_poison_score
from realtime.recon_detector import compute_recon_score
from realtime.rogue_detector import compute_rogue_score
from realtime.rogue_detector import compute_impersonation_score
from realtime.adversarial_detector import compute_adversarial_score
from realtime.future_predictor import compute_future_risk
from realtime import prediction_memory

MODELS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../models'))
TELEMETRY_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/telemetry.csv'))
DEVICES_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/devices.csv'))

FEATURE_NAMES = [
    'traffic_volume', 'packet_count', 'unique_destinations', 'unique_dst_ports',
    'port_entropy', 'avg_packet_size', 'flow_count', 'avg_duration',
    'periodicity_score', 'tcp_ratio', 'connection_frequency',
    'destination_repetition_score', 'time_of_day_activity'
]


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
        self.trust_engine = UnifiedTrustEngine()
        self.digital_twin = DigitalTwin()
        self.load_models()
        self.explainer = None
        self._initialized = True

    def load_models(self):
        try:
            required = ['scaler.pkl', 'anomaly_model.pkl', 'attack_classifier.pkl', 'label_encoder.pkl']
            for f in required:
                if not os.path.exists(os.path.join(MODELS_DIR, f)):
                    print(f"Error: {f} missing in {MODELS_DIR}")
                    return

            self.scaler = joblib.load(os.path.join(MODELS_DIR, 'scaler.pkl'))
            self.anomaly_model = joblib.load(os.path.join(MODELS_DIR, 'anomaly_model.pkl'))
            self.classifier = joblib.load(os.path.join(MODELS_DIR, 'attack_classifier.pkl'))
            self.le = joblib.load(os.path.join(MODELS_DIR, 'label_encoder.pkl'))

            try:
                self.explainer = shap.TreeExplainer(self.classifier)
            except Exception:
                self.explainer = shap.Explainer(self.classifier)
            print("ML Models and SHAP Explainer loaded successfully.")
        except Exception as e:
            print(f"Critical Error loading models: {e}")

    def get_device_info(self, device_id):
        """Get device type and age."""
        device_type = "sensor"
        device_age = None
        if os.path.exists(DEVICES_PATH):
            df = pd.read_csv(DEVICES_PATH)
            dev = df[df['device_id'] == device_id]
            if not dev.empty:
                device_type = str(dev.iloc[0].get('device_type', 'sensor'))
                if 'manufacturing_date' in dev.columns:
                    try:
                        m_date = pd.to_datetime(dev.iloc[0]['manufacturing_date'])
                        device_age = (pd.Timestamp.now() - m_date).days / 365.25
                    except Exception:
                        pass
        return device_type, device_age

    def run_inference(self, device_id):
        if not os.path.exists(TELEMETRY_PATH):
            return None

        df = pd.read_csv(TELEMETRY_PATH)
        if df.empty:
            return None

        df['timestamp'] = pd.to_datetime(df['timestamp'], utc=True, errors='coerce')
        df = df.dropna(subset=['timestamp'])

        eval_window = pd.Timestamp.now(tz='UTC') - pd.Timedelta(minutes=3)
        device_df = df[(df['device_id'] == device_id) & (df['timestamp'] > eval_window)]

        if device_df.empty:
            return None

        # === 1. FEATURE EXTRACTION ===
        features = extract_features(device_df)
        if not features:
            return None

        X = np.array([[features.get(f, 0.0) for f in FEATURE_NAMES]])

        try:
            X_scaled = self.scaler.transform(X)
        except Exception as e:
            print(f"Scaler error: {e}")
            return None

        # === 2. ML INFERENCE ===
        raw_anomaly_score = -self.anomaly_model.decision_function(X_scaled)[0]

        probas = self.classifier.predict_proba(X_scaled)[0]
        class_names = self.le.classes_
        attack_breakdown = {str(name): float(prob) * 100 for name, prob in zip(class_names, probas)}

        attack_probs_only = {k: v for k, v in attack_breakdown.items() if k != 'normal'}
        final_attack_score = max(attack_probs_only.values()) if attack_probs_only else 0.0

        pred_idx = np.argmax(probas)
        attack_type = str(class_names[pred_idx])

        # === 3. DRIFT DETECTION ===
        # Use digital twin deviation as the primary drift metric for the UI
        twin_deviation = float(self.digital_twin.compute_deviation(device_id, features))
        self.digital_twin.update(device_id, features)
        
        drift_score = twin_deviation
        baseline_data = self.drift_engine.baselines.get(device_id, {})

        # === 5. DEVICE CONTEXT ===
        device_type, device_age = self.get_device_info(device_id)
        age_factor = 0.0
        if device_age is not None:
            if device_age > 5:
                age_factor = min(50.0, (device_age - 5) * 10)
        # === 6. SPECIALIZED DETECTORS ===
        from realtime.c2_detector import compute_c2_score
        c2_score = compute_c2_score(device_id, features, baseline_data)
        slow_poison_score = compute_slow_poison_score(device_id, features, baseline_data, twin_deviation)
        recon_score = compute_recon_score(device_id, features, baseline_data)
        impersonation_score = compute_impersonation_score(device_type, features)
        rogue_score = compute_rogue_score(device_id, features)
        adversarial_score = compute_adversarial_score(raw_anomaly_score, attack_breakdown, features, baseline_data)

        # Fusion Logic
        heuristic_scores = {
            "c2_beaconing": c2_score if c2_score > 30 else 0,
            "slow_poisoning": slow_poison_score if slow_poison_score > 30 else 0,
            "recon": recon_score if recon_score > 30 else 0,
            "rogue_device": rogue_score if rogue_score > 30 else 0,
            "adversarial": adversarial_score if adversarial_score > 30 else 0,
            "impersonation": impersonation_score if impersonation_score > 30 else 0
        }

        # Fuse with ML (attack_breakdown has 0-100 values)
        fused_scores = {}
        for atk, ml_score in attack_breakdown.items():
            if atk == 'normal': continue
            h_score = heuristic_scores.get(atk, 0)
            # 60% Heuristic, 40% ML
            fused_scores[atk] = (h_score * 0.6) + (ml_score * 0.4)
        
        if fused_scores:
            final_attack_score = max(fused_scores.values())
            # Update attack type based on fused winner if it's significant
            if final_attack_score > 20:
                attack_type = max(fused_scores, key=lambda k: fused_scores[k])
            else:
                attack_type = "normal"
        else:
            final_attack_score = 0.0
            attack_type = "normal"

        # === 7. FUTURE PREDICTION ===
        # Need current trust to predict future — compute preliminary trust first
        policy_score = self.trust_engine.compute_policy_score(device_id, features, device_type)
        
        # Get trend-based prediction trend (anomaly slope as proxy)
        from realtime.trend_engine import get_trends
        trends = get_trends(device_id, last_n=10)
        prediction_trend = min(100.0, max(0.0, trends['anomaly_slope'] * 30))

        # Preliminary trust for future prediction
        prelim_trust = max(0, 100 - final_attack_score * 0.5)
        future_result = compute_future_risk(device_id, prelim_trust)
        future_risk = future_result['future_risk']

        # === 8. UNIFIED TRUST SCORE ===
        temporal_deviation = drift_score  # drift captures temporal behavioral shift
        trust_results = self.trust_engine.compute_trust(
            device_id=device_id,
            attack_probability=final_attack_score,
            digital_twin_deviation=twin_deviation,
            temporal_deviation=temporal_deviation,
            adversarial_score=adversarial_score,
            policy_score=policy_score,
            prediction_trend=prediction_trend,
            future_risk=future_risk,
            slow_poison_score=slow_poison_score,
            age_factor=age_factor
        )

        # === 9. SHAP EXPLANATIONS ===
        feature_importance = {}
        if self.explainer:
            try:
                sv = self.explainer.shap_values(X_scaled)
                class_shap = sv[pred_idx] if isinstance(sv, list) else sv[0]
                if len(class_shap.shape) > 1:
                    class_shap = class_shap[0]
                for i, name in enumerate(FEATURE_NAMES):
                    feature_importance[name] = float(class_shap[i])
            except Exception as e:
                print(f"SHAP error: {e}")

        # === 10. STORE PREDICTION ===
        prediction_memory.store_prediction({
            'timestamp': pd.Timestamp.now(tz='UTC').isoformat(),
            'device_id': device_id,
            'trust_score': trust_results['trust_score'],
            'predicted_attack': attack_type,
            'slow_poison_score': slow_poison_score,
            'recon_score': recon_score,
            'c2_score': c2_score,
            'anomaly_score': float(raw_anomaly_score),
            'traffic_volume': float(features.get('traffic_volume', 0)),
            'digital_twin_deviation': float(twin_deviation),
            'adversarial_score': adversarial_score,
            'impersonation_score': impersonation_score,
            'policy_score': policy_score,
            'future_risk': future_risk,
            'age_factor': age_factor
        })

        return {
            "device_id": device_id,
            "timestamp": pd.Timestamp.now(tz='UTC').isoformat(),
            "features": features,
            "baseline": baseline_data,
            "drift_score": float(drift_score),
            "anomaly_score": float(raw_anomaly_score),
            "attack_type": attack_type,
            "attack_breakdown": fused_scores, # Use fused scores for the UI
            "final_attack_score": float(final_attack_score),
            "heuristic_breakdown": heuristic_scores,
            "feature_importance": feature_importance,
            "device_age": device_age,
            "device_type": device_type,
            "trust_score": float(trust_results['trust_score']),
            "risk_score": float(trust_results['risk_score']),
            "policy_score": float(trust_results['policy_score']),
            "digital_twin_deviation": float(twin_deviation),
            "slow_poison_score": float(slow_poison_score),
            "recon_score": float(recon_score),
            "c2_score": float(c2_score),
            "impersonation_score": float(impersonation_score),
            "adversarial_score": float(adversarial_score),
            "future_risk": float(future_risk),
            "predicted_trust_2min": float(future_result['predicted_trust_2min']),
            "trend_data": future_result['trend_data'],
            "age_factor": float(age_factor)
        }
