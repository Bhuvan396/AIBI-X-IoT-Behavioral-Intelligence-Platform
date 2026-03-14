"""
ML Training Pipeline
=====================
Trains an XGBoost classifier to detect and classify botnet network topologies.

Usage:
    python -m modules.botnet_lab.ml_training
    # OR
    python backend/modules/botnet_lab/ml_training.py

Dataset : data/botnet_training_dataset.csv
Model   : backend/modules/botnet_lab/models/botnet_classifier.pkl
Scaler  : backend/modules/botnet_lab/models/botnet_scaler.pkl

Features:
    node_degree, fan_out_connections, packet_rate, traffic_volume,
    periodicity_score, topology_centrality, destination_entropy

Labels:
    0 = normal
    1 = centralized_botnet
    2 = p2p_botnet
    3 = mirai_botnet
"""
import os
import sys
import random
import numpy as np
import pandas as pd

# Ensure project root is in path when run directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

DATASET_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../data/botnet_training_dataset.csv"))
MODEL_DIR    = os.path.join(os.path.dirname(__file__), "models")
os.makedirs(MODEL_DIR, exist_ok=True)


# --------------------------------------------------------------------------- #
#  Dataset Generation                                                           #
# --------------------------------------------------------------------------- #
def generate_dataset(n_per_class: int = 500) -> pd.DataFrame:
    """
    Generate a synthetic labelled dataset based on known botnet signatures.
    Features are drawn from realistic distributions per class.
    """
    random.seed(42)
    np.random.seed(42)

    rows = []

    for _ in range(n_per_class):
        # Normal traffic — low degree, low fan-out, low byte count
        rows.append({
            "node_degree":         np.random.uniform(1, 3),
            "fan_out_connections": np.random.uniform(0.1, 0.5),
            "packet_rate":         np.random.uniform(10, 60),
            "traffic_volume":      np.random.uniform(500, 5000),
            "periodicity_score":   np.random.uniform(0.0, 0.2),
            "topology_centrality": np.random.uniform(0.1, 0.3),
            "destination_entropy": np.random.uniform(0.5, 1.8),
            "label": 0,
        })

    for _ in range(n_per_class):
        # Centralized Botnet — high centrality, high degree for C2 node, periodic beaconing
        rows.append({
            "node_degree":         np.random.uniform(6, 12),
            "fan_out_connections": np.random.uniform(0.7, 1.2),
            "packet_rate":         np.random.uniform(80, 200),
            "traffic_volume":      np.random.uniform(200, 2000),
            "periodicity_score":   np.random.uniform(0.7, 1.0),
            "topology_centrality": np.random.uniform(0.7, 1.0),
            "destination_entropy": np.random.uniform(2.5, 4.0),
            "label": 1,
        })

    for _ in range(n_per_class):
        # P2P Botnet — moderate degree, spread across many nodes, high entropy
        rows.append({
            "node_degree":         np.random.uniform(3, 7),
            "fan_out_connections": np.random.uniform(0.4, 0.8),
            "packet_rate":         np.random.uniform(40, 120),
            "traffic_volume":      np.random.uniform(5000, 50000),
            "periodicity_score":   np.random.uniform(0.3, 0.6),
            "topology_centrality": np.random.uniform(0.3, 0.6),
            "destination_entropy": np.random.uniform(3.5, 5.0),
            "label": 2,
        })

    for _ in range(n_per_class):
        # Mirai-style IoT — massive traffic, high fan-out (scanning), low entropy (DDoS target)
        rows.append({
            "node_degree":         np.random.uniform(8, 15),
            "fan_out_connections": np.random.uniform(1.2, 2.5),
            "packet_rate":         np.random.uniform(250, 600),
            "traffic_volume":      np.random.uniform(50000, 500000),
            "periodicity_score":   np.random.uniform(0.0, 0.3),
            "topology_centrality": np.random.uniform(0.4, 0.8),
            "destination_entropy": np.random.uniform(0.5, 2.0),
            "label": 3,
        })

    df = pd.DataFrame(rows).sample(frac=1, random_state=42).reset_index(drop=True)
    df.to_csv(DATASET_PATH, index=False)
    print(f"[ml_training] Dataset generated: {len(df)} rows → {DATASET_PATH}")
    return df


# --------------------------------------------------------------------------- #
#  Training                                                                     #
# --------------------------------------------------------------------------- #
def train():
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler
    from sklearn.metrics import classification_report, accuracy_score
    from xgboost import XGBClassifier
    import joblib

    # Build dataset if missing
    if not os.path.exists(DATASET_PATH):
        df = generate_dataset()
    else:
        df = pd.read_csv(DATASET_PATH)
        if "label" not in df.columns:
            df = generate_dataset()

    # Map string labels to numeric if necessary
    label_map = {
        "normal":             0,
        "centralized_botnet": 1,
        "p2p_botnet":         2,
        "mirai_botnet":        3
    }
    if df["label"].dtype == object:
        print(f"[ml_training] Mapping string labels to numeric: {df['label'].unique()}")
        df["label"] = df["label"].map(label_map)
        # Drop rows that didn't map (if any)
        df = df.dropna(subset=["label"])
        df["label"] = df["label"].astype(int)

    features = ["node_degree", "fan_out_connections", "packet_rate",
                "traffic_volume", "periodicity_score", "topology_centrality", "destination_entropy"]
    X = df[features].values
    y = df["label"].values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    scaler  = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test  = scaler.transform(X_test)

    clf = XGBClassifier(
        n_estimators  = 200,
        max_depth     = 6,
        learning_rate = 0.05,
        eval_metric   = "mlogloss",
        use_label_encoder=False,
        random_state  = 42,
    )
    clf.fit(X_train, y_train)

    preds    = clf.predict(X_test)
    accuracy = accuracy_score(y_test, preds)
    print(f"\n[ml_training] Test Accuracy: {accuracy*100:.2f}%")
    print(classification_report(y_test, preds, target_names=["Normal", "Centralized", "P2P", "Mirai"]))

    joblib.dump(clf,    os.path.join(MODEL_DIR, "botnet_classifier.pkl"))
    joblib.dump(scaler, os.path.join(MODEL_DIR, "botnet_scaler.pkl"))
    print(f"[ml_training] Models saved to {MODEL_DIR}")
    return accuracy


if __name__ == "__main__":
    train()
