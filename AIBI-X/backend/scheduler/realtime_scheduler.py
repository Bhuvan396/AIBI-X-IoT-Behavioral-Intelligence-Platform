import asyncio
import os
import pandas as pd
from realtime.realtime_pipeline import RealtimePipeline

pipeline = RealtimePipeline()
DEVICES_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/devices.csv'))

async def realtime_loop():
    """
    Periodic task that runs the full Stage-3 pipeline 
    (Drift, ML, Trust) for all registered devices.
    """
    while True:
        try:
            if os.path.exists(DEVICES_PATH):
                devices_df = pd.read_csv(DEVICES_PATH)
                for _, row in devices_df.iterrows():
                    device_id = row['device_id']
                    # Process current window
                    result = pipeline.run_inference(device_id)
                    if result:
                        print(f"[{device_id}] Analysis: {result['attack_type']}, Trust: {result['trust_score']:.1f}")
            
        except Exception as e:
            print(f"Error in realtime scheduler: {e}")
            
        # Frequency: 30 seconds as requested
        await asyncio.sleep(30)
