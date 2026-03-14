"""
Report Generator — creates comprehensive forensic analysis reports
with digital twin, trend analysis, future prediction, and security recommendations.
"""


class ReportGenerator:
    @staticmethod
    def generate_mitigation(attack_type, trust_score, indicators, pipeline_result=None):
        if trust_score > 90 and not indicators:
            return ["No immediate action required", "Continue routine monitoring"]

        mitigations = {
            "recon": [
                "Isolate device segment immediately",
                "Deploy honeypot on adjacent IPs",
                "Enable deep packet inspection for port 22/23/445",
                "Block scanning source at perimeter firewall"
            ],
            "exfiltration": [
                "Revoke outbound certificates",
                "Apply strict rate-limiting to destination IPs",
                "Implement 24h data lockdown for this node",
                "Audit data access logs for unauthorized reads"
            ],
            "c2_beaconing": [
                "Kill suspicious processes on device",
                "Block external C2 domain via DNS sinkhole",
                "Forced firmware re-flash recommended",
                "Enable DNS query logging for forensic analysis"
            ],
            "policy_violation": [
                "Disable unauthorized ports/services",
                "Audit device session logs for privilege escalation",
                "Re-enroll device in NAC system",
                "Review and update device access policies"
            ],
            "slow_poisoning": [
                "Reset ML baseline training points",
                "Sanitize incoming data streams",
                "Quarantine device for forensic analysis",
                "Enable behavioral drift alerting"
            ],
            "normal": [
                "Regular maintenance cycle",
                "Update security signatures"
            ]
        }

        base = mitigations.get(attack_type, ["Manual forensic audit required", "Isolate node"])

        if any("High periodicity" in ind for ind in indicators):
            base.append("Monitor for Heartbeat patterns")

        # Add contextual mitigations based on new detectors
        if pipeline_result:
            features = pipeline_result.get('features', {})
            ip = features.get('most_freq_ip', 'unknown')
            port = features.get('most_freq_port', 'unknown')
            proto = features.get('most_freq_proto', 'unknown')

            # Prepend exact mitigation commands specified in the prompt
            if attack_type != 'normal':
                base.insert(0, f"Detected suspicious communication with IP {ip} on port {port} ({proto})")
                base.insert(1, f"block IP {ip}")
                base.insert(2, "isolate device")
                base.insert(3, "verify firmware")

            if pipeline_result.get('impersonation_score', 0) > 30:
                base.append("Verify device identity — possible rogue impersonation detected")
            if pipeline_result.get('adversarial_score', 0) > 30:
                base.append("ML evasion attempt detected — increase monitoring granularity")
            if pipeline_result.get('future_risk', 0) > 50:
                base.append(f"URGENT: Trust projected to drop to {pipeline_result.get('predicted_trust_2min', 0):.0f} within 2 minutes")
            if pipeline_result.get('digital_twin_deviation', 0) > 30:
                base.append(f"Device behavior deviates {pipeline_result.get('digital_twin_deviation', 0):.0f}% from digital twin prediction")

        return base

    @staticmethod
    def create_report(pipeline_result):
        # Ensure we have a dict
        if not isinstance(pipeline_result, dict):
            return {"error": "Invalid pipeline result format"}

        device_id = pipeline_result.get('device_id', 'unknown')
        attack_type = pipeline_result.get('attack_type', 'normal')
        trust_score = pipeline_result.get('trust_score', 100.0)
        drift_score = pipeline_result.get('drift_score', 0.0)

        # 1. Drift Analysis
        drift_details = []
        features = pipeline_result.get('features', {})
        baseline = pipeline_result.get('baseline', {})

        monitored_features = {
            'traffic_volume': 'traffic_volume_mean',
            'unique_destinations': 'unique_destinations_mean',
            'port_entropy': 'port_entropy_mean',
            'periodicity_score': 'periodicity_mean'
        }

        for feat, base_key in monitored_features.items():
            curr_val = features.get(feat, 0)
            base_val = baseline.get(base_key, 0)
            if base_val > 0:
                dev_pct = ((curr_val - base_val) / base_val) * 100
                drift_details.append({
                    "feature": feat,
                    "baseline": round(base_val, 2),
                    "current": round(curr_val, 2),
                    "deviation": f"{dev_pct:+.1f}%"
                })

        # 2. Extract Contextual Metrics
        twin_dev = pipeline_result.get('digital_twin_deviation', 0)
        future_risk = pipeline_result.get('future_risk', 0)
        age = pipeline_result.get('device_age')
        anomaly_score = pipeline_result.get('anomaly_score', 0)
        final_attack_score = pipeline_result.get('final_attack_score', 0)

        # 3. XAI Behavioral Indicators
        indicators = []
        sorted_fi = []
        
        # Add SHAP indicators if available
        fi = pipeline_result.get('feature_importance', {})
        if fi:
            sorted_fi = sorted(fi.items(), key=lambda x: abs(x[1]), reverse=True)[:3]
            for name, imp in sorted_fi:
                if abs(imp) > 0.05:
                    indicators.append(f"High {name.replace('_', ' ')} impact ({imp:+.2f})")
        
        # Add behavioral indicators from specific detectors
        if pipeline_result.get('c2_score', 0) > 40:
            indicators.append("High communication periodicity detected (Heartbeat)")
            indicators.append("Repeated access to single destination IP")
            
        if features.get('port_entropy', 0) > 0.8:
            indicators.append("Unusual port entropy (Scanning behavior)")
            
        if twin_dev > 50:
            indicators.append("Traffic volume exceeding digital twin prediction")
            
        if drift_score > 20:
            indicators.append("Significant baseline drift trend detected")
            
        if pipeline_result.get('policy_score', 0) > 0:
            indicators.append("Policy violation: Unauthorized port or destination")
            
        if pipeline_result.get('impersonation_score', 0) > 40:
            indicators.append("Conflict between MAC signature and traffic behavior")

        # 3. Device Context
        age = pipeline_result.get('device_age')
        age_remark = ""
        if age is not None:
            if age > 5 and pipeline_result.get('anomaly_score', 0) < 0.1:
                age_remark = "Low anomaly on legacy device (>5yr) suggests stable hardware."
            elif age < 3 and pipeline_result.get('final_attack_score', 0) > 50:
                age_remark = "High risk on new hardware (<3yr); prioritize cyber-attack over degradation."

        # 4. Digital Twin Context
        twin_dev = pipeline_result.get('digital_twin_deviation', 0)
        twin_remark = ""
        if twin_dev > 30:
            twin_remark = f"Behavior deviates {twin_dev:.0f}% from digital twin prediction."

        # 5. Future Prediction Context
        future_risk = pipeline_result.get('future_risk', 0)
        predicted_trust = pipeline_result.get('predicted_trust_2min', trust_score)
        future_remark = ""
        if future_risk > 30:
            future_remark = f"⚠ Trust projected to drop to {float(predicted_trust):.0f} within 2 minutes."

        # 6. Build XAI summary
        xai_parts = [
            f"The model detected {attack_type} primarily due to shifts in {', '.join([f[0] for f in sorted_fi])}."
        ]
        if twin_remark:
            xai_parts.append(twin_remark)
        if age_remark:
            xai_parts.append(age_remark)
        if future_remark:
            xai_parts.append(future_remark)

        # Determine threat_level based on trust_score
        threat_level = "Unknown"
        if trust_score < 30:
            threat_level = "Critical"
        elif trust_score < 60:
            threat_level = "High"
        elif trust_score < 90:
            threat_level = "Medium"
        else:
            threat_level = "Low"

        recommendations = ReportGenerator.generate_mitigation(
            attack_type, trust_score, indicators, pipeline_result
        )

        # 7. Build JSON output
        return {
            "device_id": device_id,
            "timestamp": pipeline_result.get('timestamp', ''),
            "trust_score": float(trust_score),
            "threat_level": threat_level,
            "attack_type": attack_type,
            "attack_probability": f"{pipeline_result.get('final_attack_score', 0):.1f}%",
            "drift_score": float(drift_score),
            "indicators": indicators,
            "most_likely_attack": attack_type.replace("_", " ").title(),
            "xai_explanation": {
                "top_features": sorted_fi,
                "summary": " ".join(xai_parts)
            },
            "recommendations": ReportGenerator.generate_mitigation(
                attack_type, trust_score, indicators, pipeline_result
            )
        }

        return report
