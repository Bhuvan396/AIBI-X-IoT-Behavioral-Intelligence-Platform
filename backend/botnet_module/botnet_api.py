from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from botnet_module.topology_engine import topology_engine
from botnet_module.botnet_simulator import botnet_simulator
from botnet_module.botnet_detector import botnet_detector
from botnet_module.analysis_engine import analysis_engine
from botnet_module.intake_controller import intake_controller

router = APIRouter(prefix="/botnet", tags=["botnet"])

class BotnetInjectionRequest(BaseModel):
    botnet_type: str

@router.get("/topology")
async def get_topology():
    return topology_engine.get_topology()

@router.post("/inject")
async def inject_botnet(request: BotnetInjectionRequest):
    return botnet_simulator.inject_botnet(request.botnet_type)

@router.post("/reset")
async def reset_topology():
    return botnet_simulator.reset()

@router.get("/analysis")
async def run_analysis():
    # 1. Detection
    is_anomaly = botnet_detector.detect_topology_change()
    
    # 2. Classification
    simulated_type = botnet_simulator.active_botnet_type
    classification = botnet_detector.classify_botnet(simulated_type)
    
    # 3. Explanation
    topology = topology_engine.get_topology()
    explanation = analysis_engine.generate_explanation(
        classification["type"] if is_anomaly else "Normal Traffic",
        classification["confidence"],
        topology['metrics'],
        topology['baseline_metrics']
    )
    
    return {
        "is_anomaly": is_anomaly,
        "classification": classification,
        "analysis": explanation
    }

# --- Intake Control Endpoints ---

@router.get("/intake-status")
async def get_intake_status():
    return {"blocked": intake_controller.is_blocked()}

@router.post("/block-intake")
async def block_intake():
    intake_controller.block()
    return {"status": "success", "blocked": True, "message": "Telemetry intake has been blocked. IoT devices cannot send data."}

@router.post("/unblock-intake")
async def unblock_intake():
    intake_controller.unblock()
    return {"status": "success", "blocked": False, "message": "Telemetry intake is now active. IoT devices can send data."}
