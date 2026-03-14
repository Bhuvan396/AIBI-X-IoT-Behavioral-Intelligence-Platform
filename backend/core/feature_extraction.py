import pandas as pd
import numpy as np

def calculate_shannon_entropy(port_series):
    counts = port_series.value_counts()
    if len(counts) == 0:
        return 0.0
    probabilities = counts / len(port_series)
    entropy = -np.sum(probabilities * np.log2(probabilities))
    return float(entropy)

def extract_features(df_window: pd.DataFrame) -> dict:
    # df_window contains telemetry for ONE device in ONE 3-minute window
    if df_window.empty:
        return {}

    packet_count = len(df_window)
    traffic_volume = df_window['bytes'].sum()
    unique_destinations = df_window['dst_ip'].nunique()
    unique_dst_ports = df_window['port'].nunique()
    port_entropy = calculate_shannon_entropy(df_window['port'])
    avg_packet_size = int(traffic_volume / packet_count) if packet_count > 0 else 0
    
    # flow count loosely modeled as unique (dst_ip, port) pairs in this timeframe
    flow_count = len(df_window.groupby(['dst_ip', 'port']))
    
    avg_duration = df_window['duration'].mean()
    if pd.isna(avg_duration):
        avg_duration = 0.0

    # periodicity score (simulate variance of timestamp differences)
    # convert timestamp to seconds difference
    df_window = df_window.copy()
    df_window['timestamp'] = pd.to_datetime(df_window['timestamp'], utc=True)
    sorted_ts = df_window['timestamp'].sort_values()
    diffs = sorted_ts.diff().dt.total_seconds().dropna()
    periodicity_score = 0.0
    if len(diffs) > 1:
        # Lower variance in intervals = higher periodicity
        variance = diffs.var()
        if pd.isna(variance) or variance == 0:
            periodicity_score = 1.0 # very periodic
        else:
            periodicity_score = 1.0 / (1.0 + variance)

    tcp_ratio = df_window['protocol'].str.lower().eq('tcp').sum() / packet_count if packet_count > 0 else 0.0
    
    # connection frequency = packet_count / 180 (for a 3min window)
    connection_frequency = packet_count / 180.0

    return {
        'traffic_volume': float(traffic_volume),
        'packet_count': int(packet_count),
        'unique_destinations': int(unique_destinations),
        'unique_dst_ports': int(unique_dst_ports),
        'port_entropy': float(port_entropy),
        'avg_packet_size': float(avg_packet_size),
        'flow_count': int(flow_count),
        'avg_duration': float(avg_duration),
        'periodicity_score': float(periodicity_score),
        'tcp_ratio': float(tcp_ratio),
        'connection_frequency': float(connection_frequency)
    }
