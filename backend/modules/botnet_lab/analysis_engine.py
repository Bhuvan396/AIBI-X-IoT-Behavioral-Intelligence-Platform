"""
Analysis Engine
===============
Generates forensic evidence and XAI (Explainable AI) rationale
for botnet classification results.
"""
from modules.botnet_lab.topology_engine import topology_engine


BOTNET_PROFILES = {
    "Centralized Botnet": {
        "description": "A traditional botnet where all infected nodes communicate with a single Command & Control (C2) server. High centrality and periodic beaconing are primary signatures.",
        "indicators":  [
            "Single point of failure identified in communication paths",
            "Extremely high node degree for the central C2 node",
            "Strong periodic beaconing signals detected from IoT devices",
            "Traffic concentrated through a single intermediate IP",
        ],
        "impact": "High risk of total network seizure through a single point of control. Attacker can issue synchronized commands to all compromised devices.",
    },
    "Peer-to-Peer Botnet": {
        "description": "A decentralized botnet where nodes communicate directly with each other. No single C2 — commands propagate through the mesh.",
        "indicators":  [
            "Decentralized communication topology detected",
            "High mesh-like connectivity between peer nodes",
            "Moderate traffic across many simultaneous communication paths",
            "High destination IP entropy indicating multi-point coordination",
        ],
        "impact": "Difficult to mitigate — no single takedown point. Each infected node must be isolated individually.",
    },
    "Mirai-Style IoT Botnet": {
        "description": "Specializes in compromising low-power IoT devices using default credentials to form massive DDoS botnets.",
        "indicators":  [
            "Massive traffic burst from low-power IoT devices",
            "High fan-out rate indicating active scanning of local network",
            "Packet rate exceeding normal IoT device operating specs",
            "Connections targeting known vulnerable IoT ports (23, 2323, 80)",
        ],
        "impact": "Extreme risk of bandwidth exhaustion and participation in volumetric DDoS attacks affecting upstream infrastructure.",
    },
}

NORMAL_PROFILE = {
    "description": "The network is operating within normal baseline behavioral parameters.",
    "indicators":  ["All traffic flows match expected device-to-gateway paths."],
    "impact":      "No immediate threat detected.",
}


class AnalysisEngine:
    def generate_explanation(
        self,
        botnet_type:      str,
        confidence:       float,
        current_metrics:  dict,
        baseline_metrics: dict,
    ) -> dict:
        profile  = BOTNET_PROFILES.get(botnet_type, NORMAL_PROFILE)
        affected = [
            n["id"]
            for n in topology_engine.current_nodes
            if n["type"] not in ["gateway", "cloud", "botnet"]
        ]

        # --- Irregularities (Evidence Checklist) ---
        irregularities = []
        if current_metrics.get("avg_node_degree", 0) > baseline_metrics.get("avg_node_degree", 0) * 1.1:
            diff = round((current_metrics["avg_node_degree"] / max(baseline_metrics["avg_node_degree"], 0.01) - 1) * 100)
            irregularities.append(f"Network connectivity density increased by {diff}% (evidence of C2/P2P clustering).")
        if current_metrics.get("fan_out_ratio", 0) > baseline_metrics.get("fan_out_ratio", 0) * 1.3:
            irregularities.append(f"Fan-out ratio ({current_metrics['fan_out_ratio']}) exceeds 30% threshold — indicative of active horizontal scanning.")
        if current_metrics.get("destination_entropy", 0) > baseline_metrics.get("destination_entropy", 0) * 1.2:
            irregularities.append("Target IP entropy shift: Nodes communicating with abnormal diversity of external addresses.")

        # --- XAI Rationale ---
        rationale = []
        if botnet_type != "Normal Traffic":
            ent   = current_metrics.get("destination_entropy", 0)
            b_ent = baseline_metrics.get("destination_entropy", 0.01)
            if ent > b_ent * 1.2:
                rationale.append(f"Destination Entropy ({ent}) is {round((ent/b_ent-1)*100)}% above baseline — indicates coordination with diverse external command nodes.")
            fan   = current_metrics.get("fan_out_ratio", 0)
            b_fan = baseline_metrics.get("fan_out_ratio", 0.01)
            if fan > b_fan * 1.3:
                rationale.append(f"Fan-out Ratio ({fan}) exceeded the 30% threshold — active internal scanning consistent with {botnet_type}.")
            deg   = current_metrics.get("avg_node_degree", 0)
            b_deg = baseline_metrics.get("avg_node_degree", 0.01)
            if deg > b_deg * 1.1:
                rationale.append(f"Average Node Degree ({deg}) shows abnormal clustering — a structural signature of {botnet_type}.")

        return {
            "type":             botnet_type,
            "confidence":       f"{confidence*100:.1f}%" if isinstance(confidence, float) else confidence,
            "description":      profile.get("description", ""),
            "indicators":       profile["indicators"],
            "impact":           profile["impact"],
            "affected_devices": affected,
            "irregularities":   irregularities,
            "rationale":        rationale,
            "forensics": {
                "current":  current_metrics,
                "baseline": baseline_metrics,
            },
        }


analysis_engine = AnalysisEngine()
