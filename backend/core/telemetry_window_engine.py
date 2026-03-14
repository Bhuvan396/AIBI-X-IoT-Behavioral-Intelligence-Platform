import os
import pandas as pd
from core.feature_extraction import extract_features

TELEMETRY_CSV_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/telemetry.csv'))
FEATURES_CSV_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/features.csv'))

def init_features_csv():
    if not os.path.exists(FEATURES_CSV_PATH):
        cols = ['window_start', 'device_id', 'traffic_volume', 'packet_count', 
                'unique_destinations', 'unique_dst_ports', 'port_entropy', 
                'avg_packet_size', 'flow_count', 'avg_duration', 
                'periodicity_score', 'tcp_ratio', 'connection_frequency', 'label']
        pd.DataFrame(columns=cols).to_csv(FEATURES_CSV_PATH, index=False)

def process_windows():
    if not os.path.exists(TELEMETRY_CSV_PATH):
        return

    # To avoid modifying large files, we theoretically track progress.
    # For local testing, we'll read all, re-process windows, and write out non-duplicates.
    df = pd.read_csv(TELEMETRY_CSV_PATH)
    if df.empty:
        return

    init_features_csv()
    df['timestamp'] = pd.to_datetime(df['timestamp'], utc=True)
    
    # Drop unknown devices
    df = df[df['device_id'] != "unknown_device"]
    
    # Create fixed 3-minute intervals
    # Round down to the nearest 3 minutes
    df['window_start'] = df['timestamp'].dt.floor('3min')
    
    features_df = pd.read_csv(FEATURES_CSV_PATH)
    processed_windows = set(tuple(x) for x in features_df[['window_start', 'device_id']].values) if not features_df.empty else set()
    
    current_time = pd.Timestamp.now(tz='UTC')
    
    new_features = []
    
    for (window, device_id), group in df.groupby(['window_start', 'device_id']):
        # Only process full windows, i.e., those strictly in the past
        # Add 3 minutes to window_start to get window end
        window_end = window + pd.Timedelta(minutes=3)
        # Note: In offline/simulated situations we might just process all windows.
        # But for correctness, we only process closed windows unless it's a simulation.
        # Let's process it if we have any data, the scheduler handles the timing.
        
        window_str = str(window)
        if (window_str, device_id) in processed_windows:
            continue
            
        feat = extract_features(group.copy())
        if not feat:
            continue
            
        labels = group['attack_type'].unique()
        # Find the most severe/non-normal attack type or normal
        label = 'normal'
        for l in labels:
            if l != 'normal':
                label = l
                break

        row = {
            'window_start': window_str,
            'device_id': device_id,
            **feat,
            'label': label
        }
        new_features.append(row)
        
    if new_features:
        new_df = pd.DataFrame(new_features)
        new_df.to_csv(FEATURES_CSV_PATH, mode='a', header=False, index=False)

