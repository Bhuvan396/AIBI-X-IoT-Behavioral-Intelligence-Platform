import os
import csv
import random
import math
from datetime import datetime, timedelta

TELEMETRY_CSV_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../../data/telemetry.csv')
)

# Known C2 IP ranges by botnet type
BOTNET_C2_IPS = {
    "Centralized Botnet": ["185.220.101.50", "45.142.212.100", "194.165.16.87"],
    "Peer-to-Peer Botnet": ["10.0.0.55", "10.0.0.88", "10.0.0.99", "192.168.1.222"],
    "Mirai-Style IoT Botnet": ["172.245.192.10", "23.94.233.169", "185.156.74.60"],
}

# High-risk ports by botnet type
BOTNET_PORTS = {
    "Centralized Botnet": [6667, 8080, 443, 9001],  # IRC C2, HTTP tunneling, Tor
    "Peer-to-Peer Botnet": [4444, 5050, 6881, 9999],  # Peer comms
    "Mirai-Style IoT Botnet": [23, 2323, 80, 8888],  # Telnet, HTTP brute force
}


class TelemetryInjector:
    def generate_malicious_rows(self, botnet_type: str, device_ips: list, num_rows: int = 5) -> list:
        """Generate synthetic anomalous telemetry rows for the given botnet type."""
        rows = []
        c2_ips = BOTNET_C2_IPS.get(botnet_type, ["185.0.0.1"])
        ports = BOTNET_PORTS.get(botnet_type, [8080])
        base_time = datetime.now()

        for i, device_ip in enumerate(device_ips):
            for j in range(num_rows):
                timestamp = (base_time + timedelta(seconds=(i * num_rows + j) * 2)).strftime("%Y-%m-%dT%H:%M:%S")
                dst_ip = random.choice(c2_ips)
                port = random.choice(ports)
                protocol = "TCP" if port != 23 else "TELNET"

                # Anomalous traffic patterns
                if botnet_type == "Mirai-Style IoT Botnet":
                    # High volume DDoS-style
                    byte_count = random.randint(50000, 500000)
                    duration = round(random.uniform(0.01, 0.5), 3)
                elif botnet_type == "Peer-to-Peer Botnet":
                    # Moderate, distributed
                    byte_count = random.randint(5000, 50000)
                    duration = round(random.uniform(1.0, 10.0), 3)
                else:
                    # Centralized — periodic beaconing
                    byte_count = random.randint(200, 2000)
                    duration = round(random.uniform(0.5, 2.0), 3)

                rows.append({
                    "timestamp": timestamp,
                    "device_id": f"COMPROMISED_{device_ip.replace('.', '_')}",
                    "src_ip": device_ip,
                    "dst_ip": dst_ip,
                    "port": port,
                    "protocol": protocol,
                    "bytes": byte_count,
                    "duration": duration,
                })

        return rows

    def append_to_csv(self, rows: list) -> int:
        """Append generated rows to telemetry.csv. Returns count of rows written."""
        if not rows:
            return 0
        with open(TELEMETRY_CSV_PATH, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['timestamp', 'device_id', 'src_ip', 'dst_ip', 'port', 'protocol', 'bytes', 'duration'])
            writer.writerows(rows)
        return len(rows)

    def generate_and_append(self, botnet_type: str, device_ips: list) -> int:
        """Full pipeline: generate + append. Returns count of rows injected."""
        rows = self.generate_malicious_rows(botnet_type, device_ips)
        return self.append_to_csv(rows)


telemetry_injector = TelemetryInjector()
