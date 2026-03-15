import joblib
import os
import numpy as np
import pandas as pd
from botnet_module.topology_engine import topology_engine

MODEL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../models/botnet_classifier.pkl'))
LE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../models/botnet_classifier_le.pkl'))

class BotnetDetector:
    def __init__(self):
        self.model = None
        self.le = None
        self.load_model()

    def load_model(self):
        if os.path.exists(MODEL_PATH) and os.path.exists(LE_PATH):
            self.model = joblib.load(MODEL_PATH)
            self.le = joblib.load(LE_PATH)

    def detect_topology_change(self):
        # Suspicious if botnet_node exists in current edges
        for edge in topology_engine.current_edges:
            if edge['target'] == 'botnet_node' or edge['source'] == 'botnet_node':
                return True
        return False

    def classify_botnet(self, botnet_type_simulated=None):
        if not self.model or not self.le:
            return {"type": "Unknown", "confidence": 0.0}
        
        # Extract features from current topology state
        # (In a real system, these would be calculated from graph metrics)
        # For simulation, we map the simulated type to realistic features for the model
        
        features = {}
        if botnet_type_simulated == "Centralized Botnet":
            features = {
                'node_degree': 150,
                'traffic_volume': 3500,
                'fan_out_connections': 1,
                'packet_rate': 30,
                'periodicity_score': 0.85,
                'topology_centrality': 0.9,
                'destination_entropy': 0.3
            }
        elif botnet_type_simulated == "Peer-to-Peer Botnet":
            features = {
                'node_degree': 20,
                'traffic_volume': 1200,
                'fan_out_connections': 10,
                'packet_rate': 12,
                'periodicity_score': 0.5,
                'topology_centrality': 0.5,
                'destination_entropy': 5.0
            }
        elif botnet_type_simulated == "Mirai-Style IoT Botnet":
            features = {
                'node_degree': 3,
                'traffic_volume': 25000,
                'fan_out_connections': 60,
                'packet_rate': 500,
                'periodicity_score': 0.1,
                'topology_centrality': 0.2,
                'destination_entropy': 7.0
            }
        else:
            # Normal state
            features = {
                'node_degree': 2,
                'traffic_volume': 500,
                'fan_out_connections': 2,
                'packet_rate': 5,
                'periodicity_score': 0.2,
                'topology_centrality': 0.3,
                'destination_entropy': 1.0
            }
            
        df_feats = pd.DataFrame([features])
        probs = self.model.predict_proba(df_feats)[0]
        pred_idx = np.argmax(probs)
        pred_type = self.le.inverse_transform([pred_idx])[0]
        confidence = float(probs[pred_idx])
        
        # Map labels to human-readable types
        name_map = {
            'centralized_botnet': 'Centralized Botnet',
            'p2p_botnet': 'Peer-to-Peer Botnet',
            'mirai_botnet': 'Mirai-Style IoT Botnet',
            'normal': 'Normal Traffic'
        }
        
        return {
            "type": name_map.get(pred_type, pred_type),
            "confidence": confidence
        }

botnet_detector = BotnetDetector()
