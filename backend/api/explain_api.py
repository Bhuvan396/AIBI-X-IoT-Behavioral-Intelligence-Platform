from fastapi import APIRouter, HTTPException
from reports.report_generator import ReportGenerator
from realtime.realtime_pipeline import RealtimePipeline

router = APIRouter()
pipeline = RealtimePipeline()

@router.get("/explain/{device_id}")
def get_explanation(device_id: str):
    # 1. Get current pipeline state
    state = pipeline.run_inference(device_id)
    if not state:
        raise HTTPException(status_code=404, detail="Device data not found for explanation")
    
    # 2. Generate comprehensive report
    report = ReportGenerator.create_report(state)
    
    return report
