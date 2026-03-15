"""
Botnet Lab API
==============
FastAPI router for the Botnet Topology Lab.
Provides endpoints for topology state, botnet injection,
analysis, and intake control.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List

from modules.botnet_lab.topology_engine   import topology_engine
from modules.botnet_lab.botnet_simulator  import botnet_simulator
from modules.botnet_lab.botnet_detector   import botnet_detector
from modules.botnet_lab.analysis_engine   import analysis_engine
from modules.botnet_lab.intake_controller import intake_controller

router = APIRouter(prefix="/botnet-lab", tags=["Botnet Lab"])


class InjectRequest(BaseModel):
    botnet_type: str


@router.get("/topology")
async def get_topology():
    return topology_engine.get_topology()


@router.post("/inject")
async def inject_botnet(req: InjectRequest):
    return botnet_simulator.inject_botnet(req.botnet_type)


@router.post("/reset")
async def reset_topology():
    return botnet_simulator.reset()


@router.get("/intake-status")
async def get_intake_status():
    return {"blocked": intake_controller.is_blocked()}


@router.post("/block-intake")
async def block_intake():
    intake_controller.block()
    return {"status": "success", "blocked": True}


@router.post("/unblock-intake")
async def unblock_intake():
    intake_controller.unblock()
    return {"status": "success", "blocked": False}


@router.get("/analyze")
async def run_analysis():
    # 1 — Detect changes
    is_changed = botnet_detector.detect_topology_change()
    
    # 2 — Run ML classification
    botnet_type = botnet_simulator.active_botnet_type
    classification = botnet_detector.classify_botnet(botnet_type)
    
    # 3 — Generate explanation
    topo    = topology_engine.get_topology()
    metrics = topo["metrics"]
    baseline = topo["baseline_metrics"]
    
    analysis = analysis_engine.generate_explanation(
        classification["type"],
        classification["confidence"],
        metrics,
        baseline
    )
    
    return {
        "alert": "SUSPICIOUS NETWORK TOPOLOGY CHANGE DETECTED" if is_changed else None,
        "analysis": analysis
    }
