import time
import requests
import random
import pandas as pd

API_URL = "http://localhost:8888/telemetry"

THERMOSTATS = [
    {"src_ip": "192.168.1.131"}, # thermostat_01
]

def generate_telemetry():
    while True:
        # periodic cloud API calls
        for thermostat in THERMOSTATS:
            payload = {
                "timestamp": pd.Timestamp.now(tz="UTC").isoformat() ,
                "src_ip": thermostat["src_ip"],
                "dst_ip": "54.239.28.85", # AWS/Cloud IP
                "port": 443,
                "protocol": "TCP",
                "bytes": random.randint(1000, 3000), 
                "duration": random.uniform(0.1, 0.5)
            }
            try:
                requests.post(API_URL, json=payload)
            except Exception:
                pass
        
        # Idle for 30 seconds
        time.sleep(30)

if __name__ == "__main__":
    generate_telemetry()
