import time
import requests
import random
import pandas as pd

API_URL = "http://localhost:8888/telemetry"

def generate_telemetry():
    while True:
        # High volume, multiple destinations
        payload = {
            "timestamp": pd.Timestamp.now(tz="UTC").isoformat() ,
            "src_ip": "192.168.1.1",
            "dst_ip": f"8.8.8.{random.randint(1, 100)}",
            "port": random.choice([80, 443, 53]),
            "protocol": "TCP",
            "bytes": random.randint(10000, 500000),
            "duration": random.uniform(0.1, 10.0)
        }
        try:
            requests.post(API_URL, json=payload)
        except Exception:
            pass
        time.sleep(random.uniform(1.0, 5.0))

if __name__ == "__main__":
    generate_telemetry()
