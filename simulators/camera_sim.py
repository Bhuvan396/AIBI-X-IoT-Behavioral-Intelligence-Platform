import time
import requests
import random
import pandas as pd
import json

API_URL = "http://localhost:8888/telemetry"

CAMERAS = [
    {"src_ip": "192.168.1.101"}, # camera_01
    {"src_ip": "192.168.1.102"}, # camera_02
]

def generate_telemetry():
    print(f"Starting camera telemetry simulation to {API_URL}...")
    while True:
        for cam in CAMERAS:
            payload = {
                "timestamp": pd.Timestamp.now(tz="UTC").isoformat(),
                "src_ip": cam["src_ip"],
                "dst_ip": "104.21.34." + str(random.randint(10, 50)),
                "port": 443,
                "protocol": "TCP",
                "bytes": random.randint(50000, 150000), 
                "duration": random.uniform(0.1, 2.0)
            }
            try:
                requests.post(API_URL, json=payload, timeout=2)
            except Exception as e:
                print(f"Error sending telemetry: {e}")
                
        time.sleep(random.uniform(1, 3))

if __name__ == "__main__":
    generate_telemetry()
