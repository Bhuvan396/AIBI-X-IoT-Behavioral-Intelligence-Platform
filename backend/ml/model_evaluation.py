import os
import joblib
import json
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
from ml.model_training import preprocess_data

MODELS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../models'))
REPORTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../reports'))

def evaluate():
    X, y, feature_names, le = preprocess_data()
    
    # Load models
    classifier_path = os.path.join(MODELS_DIR, 'attack_classifier.pkl')
    if not os.path.exists(classifier_path):
        print("Models not trained yet.")
        return

    classifier = joblib.load(classifier_path)
    
    y_pred = classifier.predict(X)
    y_proba = classifier.predict_proba(X)
    
    # Metrics
    accuracy = accuracy_score(y, y_pred)
    precision = precision_score(y, y_pred, average='weighted', zero_division=0)
    recall = recall_score(y, y_pred, average='weighted', zero_division=0)
    f1 = f1_score(y, y_pred, average='weighted', zero_division=0)
    
    # ROC-AUC depends on the number of classes
    if len(np.unique(y)) > 1:
        roc_auc = roc_auc_score(y, y_proba, multi_class='ovr')
    else:
        roc_auc = 0.0
        
    conf_matrix = confusion_matrix(y, y_pred).tolist()
    
    report = {
        "accuracy": float(accuracy),
        "precision": float(precision),
        "recall": float(recall),
        "f1_score": float(f1),
        "roc_auc": float(roc_auc),
        "confusion_matrix": conf_matrix,
        "target_met": bool(accuracy > 0.95 and precision > 0.95 and recall > 0.95)
    }
    
    os.makedirs(REPORTS_DIR, exist_ok=True)
    with open(os.path.join(REPORTS_DIR, 'evaluation_report.json'), 'w') as f:
        json.dump(report, f, indent=4)
    
    print("Evaluation Report Generated.")
    print(f"Accuracy: {accuracy:.4f}")
    return report

if __name__ == "__main__":
    evaluate()
