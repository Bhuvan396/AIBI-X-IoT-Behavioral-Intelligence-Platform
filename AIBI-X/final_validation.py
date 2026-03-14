import requests
import time
import json

BASE_URL = "http://localhost:8888"

def test_device(device_id):
    print(f"--- Testing {device_id} ---")
    # Run analysis
    res = requests.post(f"{BASE_URL}/analyze_now", json={"device_id": device_id})
    if res.status_code == 200:
        data = res.json()
        print(f"Attack Breakdown: {data.get('attack_breakdown', {})}")
        print(f"Trust Score: {data['trust_score']}")
        print(f"Attack Type: {data['attack_type']}")
        print(f"Future Risk: {data['future_risk']}")
        print(f"Drift Score: {data['drift_score']}")
        
        # Get report
        res_rep = requests.get(f"{BASE_URL}/explain/{device_id}")
        if res_rep.status_code == 200:
            report = res_rep.json()
            print(f"Indicators: {report['indicators']}")
            print(f"Recommendations: {report['recommendations'][:2]}...")
        else:
            print(f"Failed to get report for {device_id}: {res_rep.status_code} - {res_rep.text}")
    else:
        print(f"Failed to analyze {device_id}: {res.text}")

if __name__ == "__main__":
    devices = ["camera_01", "printer_01", "thermostat_01"]
    for d in devices:
        test_device(d)
        time.sleep(2)
