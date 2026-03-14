import os
import pandas as pd
import numpy as np

FEATURES_CSV_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/features.csv'))
BASELINE_CSV_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/baseline.csv'))

def compute_baselines():
    if not os.path.exists(FEATURES_CSV_PATH):
        return
        
    df = pd.read_csv(FEATURES_CSV_PATH)
    if df.empty:
        return
        
    # Baseline computed ONLY on normal data
    df_normal = df[df['label'] == 'normal']
    if df_normal.empty:
        df_normal = df # Fallback if everything is attacked or undefined
        
    baselines = []
    
    for device_id, group in df_normal.groupby('device_id'):
        volume_mean = group['traffic_volume'].mean()
        volume_std = group['traffic_volume'].std()
        if pd.isna(volume_std):
            volume_std = 0.0
            
        unique_dest_mean = group['unique_destinations'].mean()
        entropy_mean = group['port_entropy'].mean()
        periodicity_mean = group['periodicity_score'].mean()
        
        # 95th percentile calculation (as required)
        volume_95 = group['traffic_volume'].quantile(0.95)
        
        baselines.append({
            'device_id': device_id,
            'traffic_volume_mean': float(volume_mean),
            'traffic_volume_std': float(volume_std),
            'traffic_volume_95th': float(volume_95) if not pd.isna(volume_95) else 0.0,
            'unique_destinations_mean': float(unique_dest_mean),
            'port_entropy_mean': float(entropy_mean),
            'periodicity_mean': float(periodicity_mean),
            'baseline_version': '1.0'
        })
        
    if baselines:
        pd.DataFrame(baselines).to_csv(BASELINE_CSV_PATH, index=False)
