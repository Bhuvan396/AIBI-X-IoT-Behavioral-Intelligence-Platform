import uvicorn
import asyncio
import os
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Add the backend directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api import telemetry_api, attack_api, ml_api, detection_api, explain_api, trust_api
from botnet_module import botnet_api
from scheduler.realtime_scheduler import realtime_loop

from contextlib import asynccontextmanager
import numpy as np
from fastapi.encoders import ENCODERS_BY_TYPE

# Global NumPy compatibility for FastAPI JSON serialization
ENCODERS_BY_TYPE[np.float32] = float
ENCODERS_BY_TYPE[np.float64] = float
ENCODERS_BY_TYPE[np.int32] = int
ENCODERS_BY_TYPE[np.int64] = int
ENCODERS_BY_TYPE[np.uint32] = int
ENCODERS_BY_TYPE[np.uint64] = int
ENCODERS_BY_TYPE[np.ndarray] = lambda x: x.tolist()
ENCODERS_BY_TYPE[np.bool_] = bool

@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(realtime_loop())
    yield
    task.cancel()

app = FastAPI(title="AIBI-X Telemetry Platform", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(telemetry_api.router)
app.include_router(attack_api.router)
app.include_router(ml_api.router)
app.include_router(detection_api.router)
app.include_router(explain_api.router)
app.include_router(trust_api.router)
app.include_router(botnet_api.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8888, reload=True)
