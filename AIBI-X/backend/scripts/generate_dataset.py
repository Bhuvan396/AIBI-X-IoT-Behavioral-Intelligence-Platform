"""
Synthetic Dataset Generator — produces 6000 rows with 13 behavioral features.
"""
import pandas as pd
import numpy as np
import os

DATASET_CSV_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/dataset.csv'))

def generate_synthetic_data(num_rows=6000):
    np.random.seed(42)
    
    classes = {
        "normal": 2000,
        "recon": 800,
        "exfiltration": 800,
        "c2_beaconing": 800,
        "policy_violation": 800,
        "slow_poisoning": 800
    }
    
    data = []
    
    for label, count in classes.items():
        for _ in range(count):
            row = {}
            if label == "normal":
                row['traffic_volume'] = np.random.normal(50000, 10000)
                row['packet_count'] = np.random.normal(100, 20)
                row['unique_destinations'] = np.random.randint(1, 3)
                row['unique_dst_ports'] = np.random.randint(1, 4)
                row['port_entropy'] = np.random.uniform(0, 0.5)
                row['avg_packet_size'] = row['traffic_volume'] / max(row['packet_count'], 1)
                row['flow_count'] = np.random.randint(1, 5)
                row['avg_duration'] = np.random.uniform(0.1, 1.0)
                row['periodicity_score'] = np.random.uniform(0.1, 0.4)
                row['tcp_ratio'] = np.random.uniform(0.7, 1.0)
                row['connection_frequency'] = row['packet_count'] / 180.0
                row['destination_repetition_score'] = np.random.uniform(0.7, 1.0)
                row['time_of_day_activity'] = np.random.uniform(0.3, 0.7)
            
            elif label == "recon":
                row['traffic_volume'] = np.random.normal(10000, 2000)
                row['packet_count'] = np.random.normal(200, 50)
                row['unique_destinations'] = np.random.randint(10, 50)
                row['unique_dst_ports'] = np.random.randint(20, 100)
                row['port_entropy'] = np.random.uniform(2.5, 5.0)
                row['avg_packet_size'] = row['traffic_volume'] / max(row['packet_count'], 1)
                row['flow_count'] = np.random.randint(50, 200)
                row['avg_duration'] = np.random.uniform(0.01, 0.1)
                row['periodicity_score'] = np.random.uniform(0.0, 0.2)
                row['tcp_ratio'] = np.random.uniform(0.6, 1.0)
                row['connection_frequency'] = row['packet_count'] / 180.0
                row['destination_repetition_score'] = np.random.uniform(0.01, 0.15)
                row['time_of_day_activity'] = np.random.uniform(0.0, 1.0)

            elif label == "exfiltration":
                row['traffic_volume'] = np.random.normal(5000000, 1000000)
                row['packet_count'] = np.random.normal(1000, 200)
                row['unique_destinations'] = np.random.randint(1, 2)
                row['unique_dst_ports'] = np.random.randint(1, 2)
                row['port_entropy'] = np.random.uniform(0, 0.1)
                row['avg_packet_size'] = row['traffic_volume'] / max(row['packet_count'], 1)
                row['flow_count'] = np.random.randint(1, 3)
                row['avg_duration'] = np.random.uniform(10.0, 30.0)
                row['periodicity_score'] = np.random.uniform(0.0, 0.2)
                row['tcp_ratio'] = 1.0
                row['connection_frequency'] = row['packet_count'] / 180.0
                row['destination_repetition_score'] = np.random.uniform(0.95, 1.0)
                row['time_of_day_activity'] = np.random.uniform(0.0, 0.3)

            elif label == "c2_beaconing":
                row['traffic_volume'] = np.random.normal(5000, 1000)
                row['packet_count'] = np.random.normal(50, 10)
                row['unique_destinations'] = 1
                row['unique_dst_ports'] = 1
                row['port_entropy'] = 0.0
                row['avg_packet_size'] = row['traffic_volume'] / max(row['packet_count'], 1)
                row['flow_count'] = 1
                row['avg_duration'] = np.random.uniform(0.05, 0.2)
                row['periodicity_score'] = np.random.uniform(0.8, 1.0)
                row['tcp_ratio'] = np.random.choice([0.0, 1.0])
                row['connection_frequency'] = row['packet_count'] / 180.0
                row['destination_repetition_score'] = 1.0
                row['time_of_day_activity'] = np.random.uniform(0.0, 1.0)

            elif label == "policy_violation":
                row['traffic_volume'] = np.random.normal(20000, 5000)
                row['packet_count'] = np.random.normal(50, 10)
                row['unique_destinations'] = np.random.randint(2, 10)
                row['unique_dst_ports'] = np.random.randint(5, 15)
                row['port_entropy'] = np.random.uniform(1.5, 3.0)
                row['avg_packet_size'] = row['traffic_volume'] / max(row['packet_count'], 1)
                row['flow_count'] = np.random.randint(5, 20)
                row['avg_duration'] = np.random.uniform(0.5, 5.0)
                row['periodicity_score'] = np.random.uniform(0.1, 0.5)
                row['tcp_ratio'] = np.random.uniform(0.1, 0.5)
                row['connection_frequency'] = row['packet_count'] / 180.0
                row['destination_repetition_score'] = np.random.uniform(0.2, 0.5)
                row['time_of_day_activity'] = np.random.uniform(0.0, 1.0)

            elif label == "slow_poisoning":
                row['traffic_volume'] = np.random.normal(80000, 20000)
                row['packet_count'] = np.random.normal(150, 40)
                row['unique_destinations'] = np.random.randint(2, 5)
                row['unique_dst_ports'] = np.random.randint(2, 6)
                row['port_entropy'] = np.random.uniform(0.5, 1.5)
                row['avg_packet_size'] = row['traffic_volume'] / max(row['packet_count'], 1)
                row['flow_count'] = np.random.randint(2, 10)
                row['avg_duration'] = np.random.uniform(0.2, 2.0)
                row['periodicity_score'] = np.random.uniform(0.2, 0.6)
                row['tcp_ratio'] = np.random.uniform(0.6, 0.9)
                row['connection_frequency'] = row['packet_count'] / 180.0
                row['destination_repetition_score'] = np.random.uniform(0.5, 0.8)
                row['time_of_day_activity'] = np.random.uniform(0.3, 0.7)

            row['label'] = label
            data.append(row)
            
    df = pd.DataFrame(data)
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    df[numeric_cols] = df[numeric_cols].clip(lower=0)
    
    os.makedirs(os.path.dirname(DATASET_CSV_PATH), exist_ok=True)
    df.to_csv(DATASET_CSV_PATH, index=False)
    print(f"Generated {len(df)} rows with {len(df.columns)} columns in {DATASET_CSV_PATH}")
    print(f"Columns: {df.columns.tolist()}")
    print(f"Distribution:\n{df['label'].value_counts()}")

if __name__ == "__main__":
    generate_synthetic_data()
