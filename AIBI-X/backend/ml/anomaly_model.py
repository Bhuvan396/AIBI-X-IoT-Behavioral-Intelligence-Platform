from sklearn.ensemble import IsolationForest
import joblib
import os

class AnomalyDetector:
    def __init__(self, n_estimators=200, contamination=0.05, random_state=42):
        self.model = IsolationForest(
            n_estimators=n_estimators,
            max_samples='auto',
            contamination=contamination,
            random_state=random_state
        )
    
    def train(self, X):
        self.model.fit(X)
    
    def predict(self, X):
        # Isolation Forest returns -1 for anomalies and 1 for normal
        # We convert it to 0 for normal and 1 for anomaly (as per common practice)
        return [1 if x == -1 else 0 for x in self.model.predict(X)]
    
    def score(self, X):
        # Higher score means more normal, lower (negative) means more anomalous
        # We negate it so higher positive score means more anomalous
        return -self.model.decision_function(X)

    def save(self, path):
        joblib.dump(self.model, path)
    
    def load(self, path):
        self.model = joblib.load(path)
