"""
Topology Engine
==============
Manages the IoT network graph state.
Stores baseline and current topology, calculates graph metrics.
"""
import math
import copy
import random


class TopologyEngine:
    def __init__(self):
        self.baseline_nodes = []
        self.baseline_edges = []
        self.current_nodes = []
        self.current_edges = []
        self.baseline_metrics = {}
        self._initialize()

    def _initialize(self):
        """Build the default clean IoT network topology."""
        nodes = [
            {"id": "camera_01", "type": "camera",     "data": {"label": "CAMERA_01",     "ip": "192.168.1.101", "type": "camera"}},
            {"id": "camera_02", "type": "camera",     "data": {"label": "CAMERA_02",     "ip": "192.168.1.102", "type": "camera"}},
            {"id": "sensor_01", "type": "sensor",     "data": {"label": "SENSOR_01",     "ip": "192.168.1.111", "type": "sensor"}},
            {"id": "sensor_02", "type": "sensor",     "data": {"label": "SENSOR_02",     "ip": "192.168.1.112", "type": "sensor"}},
            {"id": "printer_01","type": "printer",    "data": {"label": "PRINTER_01",    "ip": "192.168.1.121", "type": "printer"}},
            {"id": "thermo_01", "type": "thermostat", "data": {"label": "THERMOSTAT_01", "ip": "192.168.1.131", "type": "thermostat"}},
            {"id": "gateway",   "type": "gateway",    "data": {"label": "GATEWAY",       "ip": "192.168.1.1",   "type": "gateway"}},
            {"id": "cloud",     "type": "cloud",      "data": {"label": "CLOUD",         "ip": "54.239.28.85",  "type": "cloud"}},
        ]
        edges = [
            {"id": "e-cam01-gw",   "source": "camera_01",  "target": "gateway"},
            {"id": "e-cam02-gw",   "source": "camera_02",  "target": "gateway"},
            {"id": "e-sen01-gw",   "source": "sensor_01",  "target": "gateway"},
            {"id": "e-sen02-gw",   "source": "sensor_02",  "target": "gateway"},
            {"id": "e-pri01-gw",   "source": "printer_01", "target": "gateway"},
            {"id": "e-thr01-gw",   "source": "thermo_01",  "target": "gateway"},
            {"id": "e-gw-cloud",   "source": "gateway",    "target": "cloud"},
        ]
        self.baseline_nodes = copy.deepcopy(nodes)
        self.baseline_edges = copy.deepcopy(edges)
        self.current_nodes  = copy.deepcopy(nodes)
        self.current_edges  = copy.deepcopy(edges)
        self.baseline_metrics = self._calculate_metrics(nodes, edges)

    def _calculate_metrics(self, nodes, edges) -> dict:
        """Calculate topological graph metrics for baseline comparison."""
        n = len(nodes)
        if n == 0:
            return {}

        degree = {}
        for e in edges:
            degree[e["source"]] = degree.get(e["source"], 0) + 1
            degree[e["target"]] = degree.get(e["target"], 0) + 1

        degrees = list(degree.values())
        avg_degree = round(sum(degrees) / len(degrees), 2) if degrees else 0
        max_degree = max(degrees) if degrees else 0

        dst_counts = {}
        for e in edges:
            dst_counts[e["target"]] = dst_counts.get(e["target"], 0) + 1
        total = sum(dst_counts.values())
        entropy = 0.0
        for cnt in dst_counts.values():
            p = cnt / total
            if p > 0:
                entropy -= p * math.log2(p)

        device_count = sum(1 for nd in nodes if nd["type"] not in ["gateway", "cloud", "botnet"])
        fan_out = round(max_degree / device_count, 2) if device_count else 0
        density = round((2 * len(edges)) / (n * (n - 1)), 4) if n > 1 else 0

        return {
            "avg_node_degree":    round(avg_degree, 2),
            "max_node_degree":    max_degree,
            "fan_out_ratio":      round(fan_out, 2),
            "destination_entropy": round(entropy, 2),
            "graph_density":      density,
        }

    def get_topology(self) -> dict:
        return {
            "nodes":          [{"id": n["id"], "type": n["type"], "data": n["data"],
                                "position": self._node_position(i, len(self.current_nodes))}
                               for i, n in enumerate(self.current_nodes)],
            "edges":          self.current_edges,
            "metrics":        self._calculate_metrics(self.current_nodes, self.current_edges),
            "baseline_metrics": self.baseline_metrics,
        }

    def _node_position(self, index: int, total: int) -> dict:
        positions = [
            {"x": 150, "y": 100}, {"x": 150, "y": 220},
            {"x": 150, "y": 340}, {"x": 150, "y": 460},
            {"x": 150, "y": 580}, {"x": 150, "y": 700},
            {"x": 600, "y": 400}, {"x": 1050, "y": 400},
            {"x": 400, "y": 100},
        ]
        return positions[index] if index < len(positions) else {"x": 400, "y": index * 120}

    def reset_topology(self):
        self.current_nodes = copy.deepcopy(self.baseline_nodes)
        self.current_edges = copy.deepcopy(self.baseline_edges)
        return self.get_topology()


topology_engine = TopologyEngine()
