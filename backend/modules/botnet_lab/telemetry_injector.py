"""
Telemetry Injector
==================
Generates synthetic anomalous telemetry rows and appends them
to data/telemetry.csv when a botnet is injected. Each botnet
type produces traffic patterns characteristic of that attack style.
"""
import os
import csv
import random
from datetime import datetime, timedelta

TELEMETRY_CSV_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../../data/telemetry.csv")
)

# C2 / rendezvous IPs per botnet type
BOTNET_C2_IPS = {
    "Centralized Botnet":    ["185.220.101.50", "45.142.212.100", "194.165.16.87"],
    "Peer-to-Peer Botnet":   ["10.0.0.55", "10.0.0.88", "10.0.0.99", "192.168.1.222"],
    "Mirai-Style IoT Botnet":["172.245.192.10", "23.94.233.169", "185.156.74.60"],
}

# High-risk ports per botnet type
BOTNET_PORTS = {
    "Centralized Botnet":    [6667, 8080, 443, 9001],
    "Peer-to-Peer Botnet":   [4444, 5050, 6881, 9999],
    "Mirai-Style IoT Botnet":[23, 2323, 80, 8888],
}


class TelemetryInjector:
    def generate_malicious_rows(self, botnet_type: str, device_ips: list, num_rows: int = 5) -> list:
        rows = []
        c2_ips = BOTNET_C2_IPS.get(botnet_type, ["185.0.0.1"])
        ports  = BOTNET_PORTS.get(botnet_type, [8080])
        base   = datetime.now()

        for i, ip in enumerate(device_ips):
            for j in range(num_rows):
                ts  = (base + timedelta(seconds=(i * num_rows + j) * 2)).strftime("%Y-%m-%dT%H:%M:%S")
                dst = random.choice(c2_ips)
                prt = random.choice(ports)
                protocol = "TELNET" if prt == 23 else "TCP"

                if botnet_type == "Mirai-Style IoT Botnet":
                    byt = random.randint(50_000, 500_000)
                    dur = round(random.uniform(0.01, 0.5), 3)
                elif botnet_type == "Peer-to-Peer Botnet":
                    byt = random.randint(5_000, 50_000)
                    dur = round(random.uniform(1.0, 10.0), 3)
                else:
                    byt = random.randint(200, 2_000)
                    dur = round(random.uniform(0.5, 2.0), 3)

                rows.append({
                    "timestamp": ts,
                    "device_id": f"COMPROMISED_{ip.replace('.','_')}",
                    "src_ip":    ip,
                    "dst_ip":    dst,
                    "port":      prt,
                    "protocol":  protocol,
                    "bytes":     byt,
                    "duration":  dur,
                })
        return rows

    def append_to_csv(self, rows: list) -> int:
        if not rows:
            return 0
        fieldnames = ["timestamp", "device_id", "src_ip", "dst_ip", "port", "protocol", "bytes", "duration"]
        with open(TELEMETRY_CSV_PATH, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writerows(rows)
        return len(rows)

    def generate_and_append(self, botnet_type: str, device_ips: list) -> int:
        rows = self.generate_malicious_rows(botnet_type, device_ips)
        return self.append_to_csv(rows)


telemetry_injector = TelemetryInjector()
