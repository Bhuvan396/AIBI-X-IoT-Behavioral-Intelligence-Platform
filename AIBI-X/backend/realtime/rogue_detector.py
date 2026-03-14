"""
Rogue Device Impersonation Detector — flags behavior inconsistent with device identity.
Example: a camera performing port scanning, or a sensor doing large data transfers.
"""
import pandas as pd
import os
from realtime.prediction_memory import get_device_history

# Expected behavioral profiles per device type
DEVICE_PROFILES = {
    'camera': {
        'expected_port_entropy': (0, 1.5),       # cameras use few ports
        'expected_unique_destinations': (1, 5),    # stream to limited servers
        'expected_traffic_volume': (10000, 200000), # moderate steady traffic
        'expected_protocol': 'TCP',
        'expected_avg_duration': (0.1, 5.0),
    },
    'sensor': {
        'expected_port_entropy': (0, 0.5),        # sensors use 1-2 ports
        'expected_unique_destinations': (1, 3),    # report to MQTT broker
        'expected_traffic_volume': (50, 5000),     # tiny packets
        'expected_protocol': 'TCP',
        'expected_avg_duration': (0.01, 1.0),
    },
    'gateway': {
        'expected_port_entropy': (0, 2.0),
        'expected_unique_destinations': (1, 10),
        'expected_traffic_volume': (5000, 500000),
        'expected_protocol': 'TCP',
        'expected_avg_duration': (0.05, 3.0),
    },
    'router': {
        'expected_port_entropy': (0, 3.0),
        'expected_unique_destinations': (1, 254),
        'expected_traffic_volume': (10000, 10000000),
        'expected_protocol': 'TCP',
        'expected_avg_duration': (0.01, 30.0),
    },
    'printer': {
        'expected_port_entropy': (0, 1.0),
        'expected_unique_destinations': (1, 5),
        'expected_traffic_volume': (1000, 1000000),
        'expected_protocol': 'TCP',
        'expected_avg_duration': (0.5, 10.0),
    },
    'thermostat': {
        'expected_port_entropy': (0, 0.5),
        'expected_unique_destinations': (1, 2),
        'expected_traffic_volume': (100, 5000),
        'expected_protocol': 'TCP',
        'expected_avg_duration': (0.1, 2.0),
    }
}

DEVICES_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/devices.csv'))

def compute_attribute_mismatch(device_id):
    """Check for inconsistent static attributes in the registry."""
    if not os.path.exists(DEVICES_PATH):
        return 0.0
    
    df = pd.read_csv(DEVICES_PATH)
    dev = df[df['device_id'] == device_id]
    if dev.empty:
        return 100.0 # unknown device is high risk
    
    # Example: cameras shouldn't have manufacturing dates in the future
    m_date = pd.to_datetime(dev.iloc[0].get('manufacturing_date', '2020-01-01'))
    if m_date > pd.Timestamp.now():
        return 50.0
    
    return 0.0

def compute_impersonation_score(device_type: str, features: dict) -> float:
    """Score how much the observed behavior deviates from the expected profile."""
    # Normalize device type
    dtype = 'sensor'
    target = str(device_type).lower()
    for key in DEVICE_PROFILES:
        if key in target:
            dtype = key
            break
    
    profile = DEVICE_PROFILES.get(dtype, DEVICE_PROFILES['sensor'])
    violations = 0
    checks = 0
    
    # Check port entropy
    checks += 1
    if features.get('port_entropy', 0) > profile['expected_port_entropy'][1] * 2:
        violations += 1
    
    # Check unique destinations
    checks += 1
    if features.get('unique_destinations', 0) > profile['expected_unique_destinations'][1] * 2:
        violations += 1
    
    # Check traffic volume
    checks += 1
    tv = features.get('traffic_volume', 0)
    if tv > profile['expected_traffic_volume'][1] * 3:
        violations += 1
        
    return (violations / checks) * 100

def compute_rogue_score(device_id: str, features: dict) -> float:
    """
    Unified RogueScore = 0.5 * AttributeMismatch + 0.3 * ProfileDeviation + 0.2 * History
    """
    # 1. Attribute Mismatch (50%)
    mismatch = compute_attribute_mismatch(device_id)
    
    # 2. Profile Deviation (30%)
    # Need device type
    device_type = "sensor"
    if os.path.exists(DEVICES_PATH):
        df = pd.read_csv(DEVICES_PATH)
        dev = df[df['device_id'] == device_id]
        if not dev.empty:
            device_type = dev.iloc[0]['device_type']
            
    deviation = compute_impersonation_score(device_type, features)
    
    # 3. History (20%)
    history = get_device_history(device_id, last_n=10)
    rogue_count = sum(1 for h in history if str(h.get('predicted_attack', '')).lower() == 'rogue_device')
    historical_score = (rogue_count / max(len(history), 1)) * 100

    score = 0.5 * mismatch + 0.3 * deviation + 0.2 * historical_score
    return min(100.0, score)
