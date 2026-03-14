import argparse
import requests
import random
import time
import pandas as pd
import os

API_URL = "http://localhost:8888/telemetry"
DEVICE_REGISTRY_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/devices.csv'))

def get_ip(device_id):
    if not os.path.exists(DEVICE_REGISTRY_PATH):
        return "192.168.1.99"
    df = pd.read_csv(DEVICE_REGISTRY_PATH)
    res = df[df['device_id'] == device_id]
    if not res.empty:
        return res.iloc[0]['ip_address']
    return "192.168.1.99"

def inject(device_id):
    src_ip = get_ip(device_id)
    print(f"Injecting SLOW POISON attack on {device_id} ({src_ip})...")
    # Gradual slow increase pattern
    baseline_volume = 12000
    for i in range(1, 51):
        # Logistic-like growth for gradual increase: 12000 -> 12500 -> 13100 -> 14000...
        current_bytes = int(baseline_volume + (i ** 1.8) * 10)
        
        payload = {
            "timestamp": pd.Timestamp.now(tz="UTC").isoformat(),
            "src_ip": src_ip,
            "dst_ip": f"192.168.1.{random.randint(100, 110)}",
            "port": 443,
            "protocol": "TCP",
            "bytes": current_bytes, 
            "duration": 0.5
        }
        try:
            requests.post(API_URL, json=payload, timeout=2)
        except Exception:
            pass
        time.sleep(1.0) # Faster increase for demo
    print("Injection complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--device_id", required=True)
    args = parser.parse_args()
    inject(args.device_id)
