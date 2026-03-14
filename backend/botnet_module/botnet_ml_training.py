import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os

# Ensure directories exist
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data'))
MODELS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../backend/models'))
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)

DATASET_PATH = os.path.join(DATA_DIR, 'botnet_training_dataset.csv')
MODEL_PATH = os.path.join(MODELS_DIR, 'botnet_classifier.pkl')

def generate_synthetic_botnet_data(n_samples=5000):
    np.random.seed(42)
    data = []
    
    classes = ['normal', 'centralized_botnet', 'p2p_botnet', 'mirai_botnet']
    
    for _ in range(n_samples):
        cls = np.random.choice(classes)
        
        if cls == 'normal':
            node_degree = np.random.randint(1, 3)
            traffic_volume = np.random.uniform(100, 1000)
            fan_out = np.random.randint(1, 3)
            packet_rate = np.random.uniform(1, 10)
            periodicity = np.random.uniform(0.1, 0.3)
            centrality = np.random.uniform(0.1, 0.4)
            dst_entropy = np.random.uniform(0.5, 1.5)
            
        elif cls == 'centralized_botnet':
            # Pattern: Higher fan-out from C2, but many nodes connecting to ONE central node
            node_degree = np.random.randint(50, 200) # central node
            traffic_volume = np.random.uniform(1000, 5000)
            fan_out = np.random.randint(1, 2)
            packet_rate = np.random.uniform(10, 50)
            periodicity = np.random.uniform(0.7, 0.9)
            centrality = np.random.uniform(0.8, 1.0)
            dst_entropy = np.random.uniform(0.1, 0.5)
            
        elif cls == 'p2p_botnet':
            # Pattern: Mesh-like communication, high node degree across many nodes
            node_degree = np.random.randint(10, 30)
            traffic_volume = np.random.uniform(500, 2000)
            fan_out = np.random.randint(5, 15)
            packet_rate = np.random.uniform(5, 20)
            periodicity = np.random.uniform(0.4, 0.6)
            centrality = np.random.uniform(0.4, 0.6)
            dst_entropy = np.random.uniform(4.0, 6.0)
            
        elif cls == 'mirai_botnet':
            # Pattern: Extremely high traffic bursts, specific ports, high fan-out for scanning
            node_degree = np.random.randint(2, 5)
            traffic_volume = np.random.uniform(5000, 50000)
            fan_out = np.random.randint(20, 100)
            packet_rate = np.random.uniform(100, 1000)
            periodicity = np.random.uniform(0.0, 0.2) # chaotic scanning
            centrality = np.random.uniform(0.1, 0.3)
            dst_entropy = np.random.uniform(6.0, 8.0)
            
        data.append({
            'node_degree': node_degree,
            'traffic_volume': traffic_volume,
            'fan_out_connections': fan_out,
            'packet_rate': packet_rate,
            'periodicity_score': periodicity,
            'topology_centrality': centrality,
            'destination_entropy': dst_entropy,
            'label': cls
        })
        
    df = pd.DataFrame(data)
    df.to_csv(DATASET_PATH, index=False)
    print(f"Dataset generated at {DATASET_PATH}")
    return df

def train_botnet_model():
    if not os.path.exists(DATASET_PATH):
        df = generate_synthetic_botnet_data()
    else:
        df = pd.read_csv(DATASET_PATH)
        
    X = df.drop('label', axis=1)
    y = df['label']
    
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)
    
    model = xgb.XGBClassifier(
        n_estimators=200,
        max_depth=6,
        learning_rate=0.05,
        objective='multi:softprob',
        random_state=42
    )
    
    print("Training Botnet Classification Model...")
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    
    print(f"\nModel Accuracy: {acc:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=le.classes_))
    
    # Save model and label encoder
    joblib.dump(model, MODEL_PATH)
    joblib.dump(le, MODEL_PATH.replace('.pkl', '_le.pkl'))
    print(f"Model saved to {MODEL_PATH}")

if __name__ == "__main__":
    train_botnet_model()
