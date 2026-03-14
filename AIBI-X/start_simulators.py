import subprocess
import os
import sys

scripts = [
    "camera_sim.py",
    "sensor_sim.py",
    "printer_sim.py",
    "thermostat_sim.py",
    "router_sim.py",
    "gateway_sim.py"
]

processes = []

for s in scripts:
    p = subprocess.Popen([sys.executable, f"simulators/{s}"], 
                         stdout=subprocess.PIPE, 
                         stderr=subprocess.PIPE,
                         cwd=os.getcwd())
    processes.append(p)
    print(f"Started {s}")

print("All simulators started.")
