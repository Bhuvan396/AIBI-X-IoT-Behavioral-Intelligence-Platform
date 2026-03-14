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
    print(f"Injecting EXFILTRATION attack on {device_id} ({src_ip})...")
    dst_ip = f"{random.randint(100, 200)}.{random.randint(1, 254)}.{random.randint(1, 254)}.{random.randint(1, 254)}"
    for _ in range(50):
        payload = {
            "timestamp": pd.Timestamp.now(tz="UTC").isoformat(),
            "src_ip": src_ip,
            "dst_ip": dst_ip,
            "port": 443,
            "protocol": "TCP",
            "bytes": random.randint(1000000, 5000000),
            "duration": random.uniform(5.0, 15.0)
        }
        try:
            requests.post(API_URL, json=payload, timeout=2)
        except Exception:
            pass
        time.sleep(0.1)
    print("Injection complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--device_id", required=True)
    args = parser.parse_args()
    inject(args.device_id)
