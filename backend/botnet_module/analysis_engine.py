from botnet_module.topology_engine import topology_engine

class AnalysisEngine:
    def generate_explanation(self, botnet_type, confidence, current_metrics, baseline_metrics):
        explanations = {
            "Centralized Botnet": {
                "description": "A traditional botnet where all infected nodes communicate with a single Command & Control (C2) server.",
                "indicators": [
                    "Single points of failure identified in communication paths",
                    "Extremely high node degree for central C2 node",
                    "Strong periodic beaconing signals detected",
                    "Traffic concentrated through a single intermediate IP"
                ],
                "impact": "High risk of total network seizure through a single point of control."
            },
            "Peer-to-Peer Botnet": {
                "description": "A decentralized botnet where nodes communicate directly with each other to receive commands.",
                "indicators": [
                    "Decentralized communication topology",
                    "High mesh-like connectivity between nodes",
                    "Moderate traffic volume across many simultaneous paths",
                    "High destination IP entropy indicating multi-point coordination"
                ],
                "impact": "Difficult to mitigate due to lack of a central server; infected nodes must be isolated individually."
            },
            "Mirai-Style IoT Botnet": {
                "description": "Specialized in compromising low-power IoT devices to perform large-scale DDoS attacks.",
                "indicators": [
                    "Massive traffic burst recorded from low-power devices",
                    "High fan-out rate indicating active scanning of local network",
                    "Packet rate exceeding normal hardware operating specs",
                    "Connections targeting known vulnerable IoT ports"
                ],
                "impact": "Extreme risk of bandwidth exhaustion and participation in large-scale DDoS attacks."
            }
        }
        
        affected_devices = [node['id'] for node in topology_engine.current_nodes if node['type'] not in ['gateway', 'cloud', 'botnet']]
        
        # Calculate irregularities for "Proof of Analysis"
        irregularities = []
        if current_metrics['avg_node_degree'] > baseline_metrics['avg_node_degree'] * 1.1:
            diff = round((current_metrics['avg_node_degree'] / baseline_metrics['avg_node_degree'] - 1) * 100)
            irregularities.append(f"Network connectivity density increased by {diff}% (Evidence of C2/P2P clustering)")
        
        if current_metrics['fan_out_ratio'] > baseline_metrics['fan_out_ratio'] * 1.3:
            irregularities.append(f"Suspicious fan-out ratio ({current_metrics['fan_out_ratio']}) detected; indicators of active horizontal scanning.")

        if current_metrics['destination_entropy'] > baseline_metrics['destination_entropy'] * 1.2:
            irregularities.append("Target IP entropy shift: Nodes are communicating with abnormal diversity of external addresses.")

        default_exp = {
            "description": "The network is operating within baseline behavioral parameters.",
            "indicators": ["Normal behavioral patterns observed."],
            "impact": "No immediate threat detected."
        }
        
        exp = explanations.get(botnet_type, default_exp)

        # Generate AI Rationale (XAI)
        rationale = []
        if botnet_type != "Normal Traffic":
            if current_metrics['destination_entropy'] > baseline_metrics['destination_entropy'] * 1.2:
                rationale.append(f"Destination Entropy ({current_metrics['destination_entropy']}) is {round((current_metrics['destination_entropy']/baseline_metrics['destination_entropy']-1)*100)}% above baseline, indicating coordination with diverse external command nodes.")
            if current_metrics['fan_out_ratio'] > baseline_metrics['fan_out_ratio'] * 1.3:
                rationale.append(f"Fan-out Ratio ({current_metrics['fan_out_ratio']}) exceeded the 30% threshold, suggesting active internal scanning consistent with {botnet_type}.")
            if current_metrics['avg_node_degree'] > baseline_metrics['avg_node_degree'] * 1.1:
                rationale.append(f"Average Node Degree ({current_metrics['avg_node_degree']}) shows abnormal clustering, a signature of {botnet_type} peer/centralized structures.")
        
        return {
            "type": botnet_type,
            "confidence": f"{confidence*100:.1f}%" if isinstance(confidence, float) else confidence,
            "description": exp.get("description", ""),
            "indicators": exp["indicators"],
            "impact": exp["impact"],
            "affected_devices": affected_devices,
            "irregularities": irregularities,
            "rationale": rationale,
            "forensics": {
                "current": current_metrics,
                "baseline": baseline_metrics
            }
        }

analysis_engine = AnalysisEngine()
