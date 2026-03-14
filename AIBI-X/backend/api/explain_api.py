from fastapi import APIRouter, HTTPException
from reports.report_generator import ReportGenerator
from realtime.realtime_pipeline import RealtimePipeline

router = APIRouter()
pipeline = RealtimePipeline()

@router.get("/explain/{device_id}")
def get_explanation(device_id: str):
    try:
        # 1. Get current pipeline state
        state = pipeline.run_inference(device_id)
        if not state:
            raise HTTPException(status_code=404, detail=f"Device {device_id} telemetry not found")
        
        # 2. Generate comprehensive report
        report = ReportGenerator.create_report(state)
        return report
    except Exception as e:
        import traceback
        print(f"EXPLAIN ERROR: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))
