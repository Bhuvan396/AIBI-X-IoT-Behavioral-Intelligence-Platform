import time
import requests
import random
import pandas as pd

API_URL = "http://localhost:8888/telemetry"

PRINTERS = [
    {"src_ip": "192.168.1.121"}, # printer_01
]

def generate_telemetry():
    while True:
        # occasional LAN traffic bursts
        for printer in PRINTERS:
            burst_size = random.randint(3, 8)
            for _ in range(burst_size):
                payload = {
                    "timestamp": pd.Timestamp.now(tz="UTC").isoformat() + "Z",
                    "src_ip": printer["src_ip"],
                    "dst_ip": f"192.168.1.{random.randint(2, 254)}",
                    "port": 9100, # common printer port
                    "protocol": "TCP",
                    "bytes": random.randint(5000, 200000), 
                    "duration": random.uniform(0.1, 5.0)
                }
                try:
                    requests.post(API_URL, json=payload)
                except Exception:
                    pass
                time.sleep(random.uniform(0.1, 0.5))
        
        # Idle for 30 to 60 seconds
        time.sleep(random.randint(30, 60))

if __name__ == "__main__":
    generate_telemetry()
