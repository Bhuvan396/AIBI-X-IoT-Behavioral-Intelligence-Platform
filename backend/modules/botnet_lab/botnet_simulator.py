"""
Botnet Simulator
================
Injects botnet nodes into the topology, reroutes traffic,
and writes synthetic anomalous telemetry to telemetry.csv.
"""
import random
from modules.botnet_lab.topology_engine   import topology_engine
from modules.botnet_lab.telemetry_injector import telemetry_injector


class BotnetSimulator:
    def __init__(self):
        self.botnet_active       = False
        self.active_botnet_type  = None
        self.last_injected_rows  = 0

    def inject_botnet(self, botnet_type: str) -> dict:
        self.botnet_active      = True
        self.active_botnet_type = botnet_type

        # 1 — Create the malicious BOTNET node
        cnt = random.randint(10, 255)
        botnet_node = {
            "id":   "botnet_node",
            "type": "botnet",
            "data": {
                "label": "BOTNET",
                "ip":    f"185.{random.randint(10,255)}.{random.randint(10,255)}.{cnt}",
                "type":  "botnet",
            },
        }
        topology_engine.current_nodes.append(botnet_node)

        # 2 — Reroute: device → BOTNET_NODE → gateway
        new_edges   = []
        device_ips  = []
        for node in topology_engine.baseline_nodes:
            if node["type"] not in ["gateway", "cloud", "botnet"]:
                device_ips.append(node["data"]["ip"])
                new_edges.append({
                    "id":        f"e-{node['id']}-botnet",
                    "source":    node["id"],
                    "target":    "botnet_node",
                    "animated":  True,
                    "className": "suspicious-edge",
                })
        new_edges.append({"id": "e-botnet-gw",    "source": "botnet_node", "target": "gateway",   "animated": True, "className": "suspicious-edge"})
        new_edges.append({"id": "e-gw-cloud",     "source": "gateway",     "target": "cloud",     "animated": True})
        topology_engine.current_edges = new_edges

        # 3 — Write anomalous telemetry
        self.last_injected_rows = telemetry_injector.generate_and_append(botnet_type, device_ips)

        return {
            **topology_engine.get_topology(),
            "telemetry_rows_injected": self.last_injected_rows,
        }

    def reset(self) -> dict:
        self.botnet_active      = False
        self.active_botnet_type = None
        self.last_injected_rows = 0
        return topology_engine.reset_topology()


botnet_simulator = BotnetSimulator()
