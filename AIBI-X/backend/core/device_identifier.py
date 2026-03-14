import pandas as pd
import os

DEVICE_REGISTRY_PATH = os.path.join(os.path.dirname(__file__), '../../data/devices.csv')

class DeviceIdentifier:
    def __init__(self):
        self.ip_to_device = {}
        self.device_info = {}
        self.load_registry()

    def load_registry(self):
        if not os.path.exists(DEVICE_REGISTRY_PATH):
            return
        df = pd.read_csv(DEVICE_REGISTRY_PATH)
        for _, row in df.iterrows():
            self.ip_to_device[row['ip_address']] = row['device_id']
            self.device_info[row['device_id']] = row.to_dict()

    def identify_device(self, src_ip: str) -> str:
        return self.ip_to_device.get(src_ip, "unknown_device")

device_identifier = DeviceIdentifier()
