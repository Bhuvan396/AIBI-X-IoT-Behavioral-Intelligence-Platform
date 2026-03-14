import os
import pandas as pd

FEATURES_CSV_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/features.csv'))
DATASET_CSV_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/dataset.csv'))

EXPECTED_SCHEMA = [
    'traffic_volume', 'packet_count', 'unique_destinations', 'unique_dst_ports',
    'port_entropy', 'avg_packet_size', 'flow_count', 'avg_duration', 
    'periodicity_score', 'tcp_ratio', 'connection_frequency', 'label'
]

def build_dataset():
    if not os.path.exists(FEATURES_CSV_PATH):
        return
        
    df = pd.read_csv(FEATURES_CSV_PATH)
    if df.empty:
        return
        
    missing = [c for c in EXPECTED_SCHEMA if c not in df.columns]
    if missing:
        print(f"Missing columns for dataset: {missing}")
        return
        
    dataset_df = df[EXPECTED_SCHEMA].copy()
    
    # Balanced dataset requirement logic could be implemented here
    # E.g., oversample/undersample to ensure balanced normal vs attack classes
    
    label_counts = dataset_df['label'].value_counts()
    min_count = label_counts.min() if not label_counts.empty else 0
    
    if min_count > 0 and len(label_counts) > 1:
        # A simple rudimentary balancing: take `min_count` samples of each label type.
        dataset_df = dataset_df.groupby('label').apply(lambda x: x.sample(n=min_count)).reset_index(drop=True)

    dataset_df.to_csv(DATASET_CSV_PATH, index=False)
