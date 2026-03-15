import pandas as pd
import numpy as np
import os
import joblib
import json
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import confusion_matrix, classification_report, f1_score, accuracy_score, roc_auc_score
from imblearn.over_sampling import SMOTE
from ml.anomaly_model import AnomalyDetector
from ml.classifier_model import AttackClassifier

DATASET_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/dataset.csv'))
MODELS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../models'))
REPORTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../reports'))

def preprocess_data():
    if not os.path.exists(DATASET_PATH):
        raise FileNotFoundError(f"Dataset not found at {DATASET_PATH}")
    
    df = pd.read_csv(DATASET_PATH)
    df = df.dropna()
    
    features = [
        'traffic_volume', 'packet_count', 'unique_destinations', 'unique_dst_ports',
        'port_entropy', 'avg_packet_size', 'flow_count', 'avg_duration', 
        'periodicity_score', 'tcp_ratio', 'connection_frequency'
    ]
    
    X = df[features]
    y = df['label']
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)
    
    os.makedirs(MODELS_DIR, exist_ok=True)
    joblib.dump(scaler, os.path.join(MODELS_DIR, 'scaler.pkl'))
    joblib.dump(le, os.path.join(MODELS_DIR, 'label_encoder.pkl'))
    
    return X_scaled, y_encoded, features, le

def train_models():
    X, y, feature_names, le = preprocess_data()
    
    unique, counts = np.unique(y, return_counts=True)
    print(f"Class distribution original: {dict(zip(le.inverse_transform(unique), counts))}")
    
    # SMOTE for balance (Upgrade 10)
    # Using a minimum of 2 samples for SMOTE k_neighbors
    k_neighbors = min(counts) - 1 if min(counts) > 1 else 1
    smote = SMOTE(random_state=42, k_neighbors=min(5, k_neighbors))
    X_res, y_res = smote.fit_resample(X, y)
    print(f"Resampled distribution: {pd.Series(y_res).value_counts().to_dict()}")

    X_train, X_test, y_train, y_test = train_test_split(X_res, y_res, test_size=0.2, random_state=42, stratify=y_res)
    
    # 1. Anomaly Model
    print("Training Anomaly Detector...")
    anomaly_detector = AnomalyDetector()
    anomaly_detector.train(X_train)
    anomaly_detector.save(os.path.join(MODELS_DIR, 'anomaly_model.pkl'))
    
    # 2. Classifier Model with Hyperparameter Tuning (Upgrade 10)
    print("Training Attack Classifier (Tuning Enabled)...")
    classifier = AttackClassifier()
    best_params = classifier.train(X_train, y_train)
    classifier.save(os.path.join(MODELS_DIR, 'attack_classifier.pkl'))
    
    # 3. Evaluation (Upgrade 10)
    print("Performing Evaluation...")
    y_pred = classifier.predict(X_test)
    y_proba = classifier.predict_proba(X_test)
    
    acc = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average='weighted')
    cm = confusion_matrix(y_test, y_pred).tolist()
    
    # Feature Importance
    raw_importance = {}
    if hasattr(classifier.model, 'feature_importances_'):
        raw_importance = dict(zip(feature_names, classifier.model.feature_importances_.tolist()))
    
    report = {
        "accuracy": float(acc),
        "f1_score": float(f1),
        "best_params": best_params,
        "confusion_matrix": cm,
        "class_report": classification_report(y_test, y_pred, target_names=le.classes_, output_dict=True),
        "feature_importance": raw_importance
    }
    
    os.makedirs(REPORTS_DIR, exist_ok=True)
    with open(os.path.join(REPORTS_DIR, 'ml_evaluation_report.json'), 'w') as f:
        json.dump(report, f, indent=4)
    
    print(f"Training Complete. Accuracy: {acc:.4f}, F1: {f1:.4f}")
    return report

if __name__ == "__main__":
    train_models()
