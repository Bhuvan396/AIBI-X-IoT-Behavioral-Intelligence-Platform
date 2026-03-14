import os
import csv
from threading import Lock
from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict
from core.device_identifier import device_identifier
from botnet_module.intake_controller import intake_controller

router = APIRouter()
telemetry_lock = Lock()
TELEMETRY_CSV_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/telemetry.csv'))

class TelemetryEvent(BaseModel):
    timestamp: str
    src_ip: str
    dst_ip: str
    port: int
    protocol: str
    bytes: int
    duration: float

# Simple deduplication cache
recent_events = set()

def initialize_csv():
    if not os.path.exists(TELEMETRY_CSV_PATH):
        with open(TELEMETRY_CSV_PATH, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['timestamp', 'device_id', 'src_ip', 'dst_ip', 'port', 'protocol', 'bytes', 'duration'])

initialize_csv()

@router.post("/telemetry")
def ingest_telemetry(event: TelemetryEvent):
    # Check if intake is blocked
    if intake_controller.is_blocked():
        raise HTTPException(status_code=403, detail="Telemetry intake is blocked. IoT device data is not being accepted.")
    
    # 1 check valid timestamp
    if not event.timestamp:
        raise HTTPException(status_code=400, detail="Invalid timestamp")
    
    # 2 identify device
    device_id = device_identifier.identify_device(event.src_ip)
    
    # 3 duplicate detection
    event_tuple = (event.timestamp, event.src_ip, event.dst_ip, event.port, event.protocol, event.bytes)
    if event_tuple in recent_events:
        return {"status": "skipped", "reason": "duplicate"}
    
    recent_events.add(event_tuple)
    if len(recent_events) > 10000:
        recent_events.clear()  # basic cleanup
        
    # 4 append to csv
    with telemetry_lock:
        with open(TELEMETRY_CSV_PATH, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                event.timestamp,
                device_id,
                event.src_ip,
                event.dst_ip,
                event.port,
                event.protocol,
                event.bytes,
                event.duration
            ])
            
    return {"status": "success", "device_id": device_id}
