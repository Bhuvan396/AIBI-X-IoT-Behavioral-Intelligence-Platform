import pandas as pd
import numpy as np
import os

DATASET_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/dataset.csv'))

def generate_synthetic_data():
    np.random.seed(42)
    
    data = []
    
    # helper for shannon entropy
    def get_port_entropy(ports):
        series = pd.Series(ports)
        counts = series.value_counts()
        probs = counts / len(series)
        return -np.sum(probs * np.log2(probs))

    # 1. Normal Traffic (2000 rows)
    for _ in range(2000):
        data.append({
            'traffic_volume': np.random.randint(5000, 50000),
            'packet_count': np.random.randint(50, 500),
            'unique_destinations': np.random.randint(1, 3),
            'unique_dst_ports': np.random.randint(1, 5),
            'port_entropy': np.random.uniform(0.1, 1.5),
            'avg_packet_size': np.random.uniform(64, 1500),
            'flow_count': np.random.randint(1, 10),
            'avg_duration': np.random.uniform(0.1, 5.0),
            'periodicity_score': np.random.uniform(0.1, 0.4),
            'tcp_ratio': np.random.uniform(0.7, 1.0),
            'connection_frequency': np.random.uniform(0.1, 2.0),
            'label': 'normal'
        })

    # 2. Recon Attack (800 rows)
    # pattern: high port entropy, many destinations, many ports, short connections
    for _ in range(800):
        data.append({
            'traffic_volume': np.random.randint(500, 5000),
            'packet_count': np.random.randint(100, 1000),
            'unique_destinations': np.random.randint(10, 50),
            'unique_dst_ports': np.random.randint(50, 200),
            'port_entropy': np.random.uniform(5.0, 7.5),
            'avg_packet_size': np.random.uniform(40, 100),
            'flow_count': np.random.randint(100, 500),
            'avg_duration': np.random.uniform(0.01, 0.1),
            'periodicity_score': np.random.uniform(0.0, 0.1),
            'tcp_ratio': 1.0,
            'connection_frequency': np.random.uniform(1.0, 10.0),
            'label': 'recon'
        })

    # 3. Exfiltration Attack (800 rows)
    # pattern: very large volume, long duration, large packet size
    for _ in range(800):
        data.append({
            'traffic_volume': np.random.randint(10**7, 5*10**7),
            'packet_count': np.random.randint(5000, 20000),
            'unique_destinations': np.random.randint(1, 2),
            'unique_dst_ports': np.random.randint(1, 2),
            'port_entropy': np.random.uniform(0.0, 0.5),
            'avg_packet_size': np.random.uniform(1200, 1500),
            'flow_count': np.random.randint(1, 5),
            'avg_duration': np.random.uniform(10.0, 60.0),
            'periodicity_score': np.random.uniform(0.0, 0.2),
            'tcp_ratio': 1.0,
            'connection_frequency': np.random.uniform(5.0, 30.0),
            'label': 'exfiltration'
        })

    # 4. C2 Beaconing (800 rows)
    # pattern: high periodicity, small packets, same destination
    for _ in range(800):
        data.append({
            'traffic_volume': np.random.randint(1000, 10000),
            'packet_count': np.random.randint(10, 50),
            'unique_destinations': 1,
            'unique_dst_ports': 1,
            'port_entropy': 0.0,
            'avg_packet_size': np.random.uniform(64, 256),
            'flow_count': 1,
            'avg_duration': np.random.uniform(0.05, 0.2),
            'periodicity_score': np.random.uniform(0.8, 1.0),
            'tcp_ratio': np.random.choice([0.0, 1.0]),
            'connection_frequency': np.random.uniform(0.1, 0.5),
            'label': 'c2_beaconing'
        })

    # 5. Policy Violation (800 rows)
    # pattern: unexpected ports (SSH on IoT), unusual intervals
    for _ in range(800):
        data.append({
            'traffic_volume': np.random.randint(5000, 20000),
            'packet_count': np.random.randint(20, 100),
            'unique_destinations': np.random.randint(2, 10),
            'unique_dst_ports': np.random.randint(2, 5),
            'port_entropy': np.random.uniform(1.0, 2.5),
            'avg_packet_size': np.random.uniform(100, 1000),
            'flow_count': np.random.randint(5, 20),
            'avg_duration': np.random.uniform(1.0, 10.0),
            'periodicity_score': np.random.uniform(0.1, 0.3),
            'tcp_ratio': 1.0,
            'connection_frequency': np.random.uniform(0.1, 1.0),
            'label': 'policy_violation'
        })

    # 6. Slow Poisoning (800 rows)
    # pattern: gradual drift (simulated as slightly increased volume/frequency over normal)
    for _ in range(800):
        data.append({
            'traffic_volume': np.random.randint(60000, 150000),
            'packet_count': np.random.randint(600, 1500),
            'unique_destinations': np.random.randint(2, 5),
            'unique_dst_ports': np.random.randint(2, 10),
            'port_entropy': np.random.uniform(2.0, 4.0),
            'avg_packet_size': np.random.uniform(100, 1500),
            'flow_count': np.random.randint(10, 50),
            'avg_duration': np.random.uniform(0.5, 2.0),
            'periodicity_score': np.random.uniform(0.2, 0.5),
            'tcp_ratio': np.random.uniform(0.8, 1.0),
            'connection_frequency': np.random.uniform(2.0, 5.0),
            'label': 'slow_poison'
        })

    df = pd.DataFrame(data)
    # shuffle
    df = df.sample(frac=1).reset_index(drop=True)
    
    os.makedirs(os.path.dirname(DATASET_PATH), exist_ok=True)
    df.to_csv(DATASET_PATH, index=False)
    print(f"Generated {len(df)} rows and saved to {DATASET_PATH}")

if __name__ == "__main__":
    generate_synthetic_data()
