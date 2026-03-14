import pandas as pd
import os

DEVICES_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/devices.csv'))

class TopologyEngine:
    def __init__(self):
        self.baseline_nodes = []
        self.baseline_edges = []
        self.current_nodes = []
        self.current_edges = []
        self.baseline_metrics = {}
        self.initialize_topology()

    def calculate_metrics(self, nodes, edges):
        """Calculates topological metrics for analysis evidence."""
        node_degrees = {n['id']: 0 for n in nodes}
        out_degrees = {n['id']: 0 for n in nodes}
        for e in edges:
            if e['source'] in node_degrees: node_degrees[e['source']] += 1
            if e['target'] in node_degrees: node_degrees[e['target']] += 1
            if e['source'] in out_degrees: out_degrees[e['source']] += 1

        # Calculate average metrics
        device_nodes = [n for n in nodes if n['type'] not in ['gateway', 'cloud', 'botnet']]
        num_devices = len(device_nodes) if device_nodes else 1
        
        avg_degree = sum(node_degrees.values()) / len(nodes)
        max_degree = max(node_degrees.values()) if nodes else 0
        avg_fan_out = sum(out_degrees.values()) / len(nodes)
        
        # Entropy heuristic (unique destination diversity)
        destinations = [e['target'] for e in edges]
        unique_dests = len(set(destinations))
        entropy_score = unique_dests / len(edges) if edges else 0

        return {
            "avg_node_degree": round(avg_degree, 2),
            "max_node_degree": max_degree,
            "fan_out_ratio": round(avg_fan_out, 2),
            "destination_entropy": round(entropy_score * 10, 2),
            "graph_density": round(len(edges) / (len(nodes) * (len(nodes)-1)/2), 4) if len(nodes) > 1 else 0
        }

    def initialize_topology(self):
        # Load devices
        if os.path.exists(DEVICES_PATH):
            df = pd.read_csv(DEVICES_PATH)
            
            # Nodes
            nodes = []
            # Gateway node
            nodes.append({
                "id": "gateway",
                "type": "gateway",
                "data": {
                    "label": "GATEWAY",
                    "ip": "192.168.1.1",
                    "type": "gateway"
                },
                "position": {"x": 400, "y": 250}
            })
            # Cloud node
            nodes.append({
                "id": "cloud",
                "type": "cloud",
                "data": {
                    "label": "CLOUD",
                    "ip": "54.239.28.85",
                    "type": "cloud"
                },
                "position": {"x": 700, "y": 250}
            })
            
            # Device nodes
            y_start = 100
            for i, row in df.iterrows():
                nodes.append({
                    "id": row['device_id'],
                    "type": row['device_type'],
                    "data": {
                        "label": row['device_id'].upper(),
                        "ip": row['ip_address'],
                        "type": row['device_type']
                    },
                    "position": {"x": 100, "y": y_start + (i * 100)}
                })
            
            # Edges
            edges = []
            for i, row in df.iterrows():
                edges.append({
                    "id": f"e-{row['device_id']}-gateway",
                    "source": row['device_id'],
                    "target": "gateway",
                    "animated": True
                })
            edges.append({
                "id": "e-gateway-cloud",
                "source": "gateway",
                "target": "cloud",
                "animated": True
            })
            
            self.baseline_nodes = nodes
            self.baseline_edges = edges
            self.current_nodes = list(nodes)
            self.current_edges = list(edges)
            self.baseline_metrics = self.calculate_metrics(nodes, edges)

    def get_topology(self):
        return {
            "nodes": self.current_nodes,
            "edges": self.current_edges,
            "metrics": self.calculate_metrics(self.current_nodes, self.current_edges),
            "baseline_metrics": self.baseline_metrics
        }

    def reset_topology(self):
        self.current_nodes = list(self.baseline_nodes)
        self.current_edges = list(self.baseline_edges)
        return self.get_topology()

topology_engine = TopologyEngine()
