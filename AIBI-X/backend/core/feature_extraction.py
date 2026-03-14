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
    if df_window.empty:
        return {}

    packet_count = len(df_window)
    traffic_volume = df_window['bytes'].sum()
    unique_destinations = df_window['dst_ip'].nunique()
    unique_dst_ports = df_window['port'].nunique()
    port_entropy = calculate_shannon_entropy(df_window['port'])
    avg_packet_size = int(traffic_volume / packet_count) if packet_count > 0 else 0
    
    flow_count = len(df_window.groupby(['dst_ip', 'port']))
    
    avg_duration = df_window['duration'].mean()
    if pd.isna(avg_duration):
        avg_duration = 0.0

    # Periodicity score
    df_window = df_window.copy()
    df_window['timestamp'] = pd.to_datetime(df_window['timestamp'], utc=True, errors='coerce')
    sorted_ts = df_window['timestamp'].sort_values()
    diffs = sorted_ts.diff().dt.total_seconds().dropna()
    periodicity_score = 0.0
    if len(diffs) > 1:
        variance = diffs.var()
        if pd.isna(variance) or variance == 0:
            periodicity_score = 1.0
        else:
            periodicity_score = 1.0 / (1.0 + variance)

    tcp_ratio = df_window['protocol'].str.lower().eq('tcp').sum() / packet_count if packet_count > 0 else 0.0
    connection_frequency = packet_count / 180.0

    # NEW: Destination Repetition Score
    # Measures how concentrated traffic is to a single destination
    dst_counts = df_window['dst_ip'].value_counts()
    if len(dst_counts) > 0:
        top_dst_ratio = dst_counts.iloc[0] / packet_count
        destination_repetition_score = float(top_dst_ratio)
    else:
        destination_repetition_score = 0.0

    # NEW: Top IP Periodicity
    top_ip_periodicity = 0.0
    if not df_window.empty and not df_window['dst_ip'].mode().empty:
        top_ip = df_window['dst_ip'].mode().iloc[0]
        top_ip_df = df_window[df_window['dst_ip'] == top_ip].copy()
        top_ip_df['timestamp'] = pd.to_datetime(top_ip_df['timestamp'], utc=True, errors='coerce')
        top_ip_ts = top_ip_df['timestamp'].sort_values()
        top_ip_diffs = top_ip_ts.diff().dt.total_seconds().dropna()
        if len(top_ip_diffs) > 1:
            v_top = top_ip_diffs.var()
            top_ip_periodicity = 1.0 / (1.0 + v_top) if not pd.isna(v_top) else 0.0

    # NEW: Time of Day Activity
    # Encodes hour as cyclic feature (0-1 scale using sin transform)
    valid_ts = df_window['timestamp'].dropna()
    if not valid_ts.empty:
        mean_hour = valid_ts.dt.hour.mean()
        time_of_day_activity = float(np.sin(2 * np.pi * mean_hour / 24.0) * 0.5 + 0.5)
    else:
        time_of_day_activity = 0.5

    # Raw context for recommendation engine
    most_freq_ip = str(df_window['dst_ip'].mode().iloc[0]) if 'dst_ip' in df_window and not df_window['dst_ip'].mode().empty else 'unknown'
    most_freq_port = str(df_window['port'].mode().iloc[0]) if 'port' in df_window and not df_window['port'].mode().empty else 'unknown'
    most_freq_proto = str(df_window['protocol'].mode().iloc[0]) if 'protocol' in df_window and not df_window['protocol'].mode().empty else 'unknown'

    return {
        'most_freq_ip': most_freq_ip,
        'most_freq_port': most_freq_port,
        'most_freq_proto': most_freq_proto,
        'traffic_volume': float(traffic_volume),
        'packet_count': int(packet_count),
        'unique_destinations': int(unique_destinations),
        'unique_dst_ports': int(unique_dst_ports),
        'port_entropy': float(port_entropy),
        'avg_packet_size': float(avg_packet_size),
        'flow_count': int(flow_count),
        'avg_duration': float(avg_duration),
        'periodicity_score': float(periodicity_score),
        'top_ip_periodicity': float(top_ip_periodicity),
        'tcp_ratio': float(tcp_ratio),
        'connection_frequency': float(connection_frequency),
        'destination_repetition_score': float(destination_repetition_score),
        'time_of_day_activity': float(time_of_day_activity)
    }
