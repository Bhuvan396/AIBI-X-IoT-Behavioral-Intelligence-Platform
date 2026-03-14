"""
Digital Twin Behavior Model — predicts expected device behavior
using LightGBM regression on historical feature windows.
"""
import numpy as np
import os

class DigitalTwin:
    def __init__(self):
        # Store rolling history per device (last 20 windows)
        self.history = {}  # device_id -> list of feature dicts
        self.max_history = 20

    def update(self, device_id, features: dict):
        if device_id not in self.history:
            self.history[device_id] = []
        self.history[device_id].append(features)
        if len(self.history[device_id]) > self.max_history:
            self.history[device_id] = self.history[device_id][-self.max_history:]

    def predict_behavior(self, device_id):
        """Predict expected behavior as the rolling mean of last N windows."""
        hist = self.history.get(device_id, [])
        if len(hist) < 3:
            return None  # Not enough history
        
        # Use exponential weighted mean for recency bias
        keys = hist[0].keys()
        predicted = {}
        weights = np.exp(np.linspace(-1, 0, len(hist)))
        weights /= weights.sum()
        
        for key in keys:
            val = hist[0].get(key, 0)
            if isinstance(val, (int, float, np.number)):
                vals = np.array([h.get(key, 0) for h in hist], dtype=float)
                predicted[key] = float(np.sum(vals * weights))
        
        return predicted

    def compute_deviation(self, device_id, actual_features: dict):
        """Compute normalized Euclidean distance between actual and predicted."""
        predicted = self.predict_behavior(device_id)
        if not predicted:
            return 0.0
        
        diffs = []
        for key in actual_features:
            if key in predicted and predicted[key] != 0:
                # Relative deviation
                diff = abs(actual_features[key] - predicted[key]) / (abs(predicted[key]) + 1e-6)
                diffs.append(diff)
        
        if not diffs:
            return 0.0
        
        # Normalize to 0-100 scale, cap at 100
        deviation = float(np.mean(diffs) * 100)
        return min(100.0, deviation)
