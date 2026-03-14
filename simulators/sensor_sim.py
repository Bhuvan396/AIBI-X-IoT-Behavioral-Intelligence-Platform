import time
import requests
import random
import pandas as pd

API_URL = "http://localhost:8888/telemetry"

SENSORS = [
    {"src_ip": "192.168.1.111"}, # sensor_01
    {"src_ip": "192.168.1.112"}, # sensor_02
]

def generate_telemetry():
    print(f"Starting sensor telemetry simulation to {API_URL}...")
    while True:
        for sensor in SENSORS:
            payload = {
                "timestamp": pd.Timestamp.now(tz="UTC").isoformat(),
                "src_ip": sensor["src_ip"],
                "dst_ip": "192.168.1.50", 
                "port": 1883,
                "protocol": "TCP",
                "bytes": random.randint(100, 300),
                "duration": random.uniform(0.01, 0.1)
            }
            try:
                requests.post(API_URL, json=payload, timeout=2)
            except Exception:
                pass
                
        time.sleep(10)

if __name__ == "__main__":
    generate_telemetry()
