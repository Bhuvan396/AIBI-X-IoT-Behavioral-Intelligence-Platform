import random
from botnet_module.topology_engine import topology_engine
from botnet_module.telemetry_injector import telemetry_injector

class BotnetSimulator:
    def __init__(self):
        self.botnet_active = False
        self.active_botnet_type = None
        self.last_injected_rows = 0

    def inject_botnet(self, botnet_type):
        self.botnet_active = True
        self.active_botnet_type = botnet_type
        
        # 1. Create Botnet Node
        botnet_node = {
            "id": "botnet_node",
            "type": "botnet",
            "data": {
                "label": "BOTNET",
                "ip": f"185.{random.randint(10, 255)}.{random.randint(10, 255)}.{random.randint(10, 255)}",
                "type": "botnet"
            },
            "position": {"x": 400, "y": 100},
            "className": "botnet-node"
        }
        
        topology_engine.current_nodes.append(botnet_node)
        
        # 2. Reroute Traffic
        new_edges = []
        device_ips = []
        for node in topology_engine.baseline_nodes:
            if node['type'] not in ['gateway', 'cloud', 'botnet']:
                device_ips.append(node['data']['ip'])
                new_edges.append({
                    "id": f"e-{node['id']}-botnet",
                    "source": node['id'],
                    "target": "botnet_node",
                    "animated": True,
                    "className": "suspicious-edge"
                })
        
        new_edges.append({
            "id": "e-botnet-gateway",
            "source": "botnet_node",
            "target": "gateway",
            "animated": True,
            "className": "suspicious-edge"
        })
        
        new_edges.append({
            "id": "e-gateway-cloud",
            "source": "gateway",
            "target": "cloud",
            "animated": True
        })
        
        topology_engine.current_edges = new_edges

        # 3. Inject anomalous telemetry rows into telemetry.csv
        self.last_injected_rows = telemetry_injector.generate_and_append(botnet_type, device_ips)
        
        return {
            **topology_engine.get_topology(),
            "telemetry_rows_injected": self.last_injected_rows
        }

    def reset(self):
        self.botnet_active = False
        self.active_botnet_type = None
        self.last_injected_rows = 0
        return topology_engine.reset_topology()

botnet_simulator = BotnetSimulator()
