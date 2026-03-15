import subprocess
import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

class AttackPayload(BaseModel):
    device_id: str
    attack_type: str

ATTACK_SCRIPTS = {
    "recon": "inject_recon.py",
    "exfiltration": "inject_exfiltration.py",
    "c2_beaconing": "inject_c2.py",
    "policy_violation": "inject_policy_violation.py",
    "slow_poison": "inject_slow_poison.py"
}

@router.post("/inject_attack")
def inject_attack(payload: AttackPayload):
    if payload.attack_type not in ATTACK_SCRIPTS:
        raise HTTPException(status_code=400, detail="Invalid attack type")

    script_name = ATTACK_SCRIPTS[payload.attack_type]
    script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../attacks', script_name))

    if not os.path.exists(script_path):
        raise HTTPException(status_code=500, detail="Attack script not found")

    # Run attack script as a background process, pass device_id
    try:
        subprocess.Popen(['python', script_path, '--device_id', payload.device_id])
        
        # Upgrade 13: Trigger immediate evaluation
        # Note: We trigger it after a tiny delay so at least some packets are ingested
        from realtime.realtime_pipeline import RealtimePipeline
        pipeline = RealtimePipeline()
        # We run it in the background or just quickly
        import threading
        threading.Thread(target=pipeline.run_inference, args=(payload.device_id,)).start()
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"status": "success", "message": f"Injected {payload.attack_type} on {payload.device_id}"}
