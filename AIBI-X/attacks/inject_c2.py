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
    print(f"Injecting C2 BEACONING attack on {device_id} ({src_ip})...")
    dst_ip = "185.15.59.224"
    for _ in range(30):
        payload = {
            "timestamp": pd.Timestamp.now(tz="UTC").isoformat(),
            "src_ip": src_ip,
            "dst_ip": dst_ip,
            "port": 53,
            "protocol": "UDP",
            "bytes": 512,
            "duration": 0.05,
        }
        try:
            requests.post(API_URL, json=payload, timeout=2)
        except Exception:
            pass
        # beacon fast for demo
        time.sleep(1) 
    print("Injection complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--device_id", required=True)
    args = parser.parse_args()
    inject(args.device_id)
