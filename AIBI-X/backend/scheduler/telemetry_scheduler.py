import asyncio
from core.telemetry_window_engine import process_windows
from core.baseline_engine import compute_baselines
from core.dataset_builder import build_dataset

async def scheduler_loop():
    while True:
        # Run every 3 minutes (180 seconds)
        await asyncio.sleep(180)
        try:
            print("Running scheduled tasks: aggregate -> feature extract -> baseline -> dataset")
            process_windows()
            compute_baselines()
            build_dataset()
        except Exception as e:
            print(f"Scheduler Error: {e}")

