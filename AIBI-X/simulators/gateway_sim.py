import time
import requests
import random
import pandas as pd

API_URL = "http://localhost:8888/telemetry"

def generate_telemetry():
    while True:
        # Periodic syncs
        payload = {
            "timestamp": pd.Timestamp.now(tz="UTC").isoformat() ,
            "src_ip": "192.168.1.254",
            "dst_ip": "10.0.0.1",
            "port": 5000,
            "protocol": "UDP",
            "bytes": random.randint(500, 2000),
            "duration": random.uniform(0.1, 0.5)
        }
        try:
            requests.post(API_URL, json=payload)
        except Exception:
            pass
        time.sleep(10)

if __name__ == "__main__":
    generate_telemetry()
