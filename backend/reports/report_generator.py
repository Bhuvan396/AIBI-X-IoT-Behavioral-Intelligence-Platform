class ReportGenerator:
    @staticmethod
    def generate_mitigation(attack_type, trust_score, indicators):
        if trust_score > 90 and not indicators:
            return ["No immediate action required", "Continue routine monitoring"]
        
        mitigations = {
            "recon": [
                "Isolate device segment immediately", 
                "Deploy honeypot on adjacent IPs", 
                "Enable deep packet inspection for port 22/23/445"
            ],
            "exfiltration": [
                "Revoke outbound certificates", 
                "Apply strict rate-limiting to destination IPs", 
                "Implement 24h data lockdown for this node"
            ],
            "c2_beaconing": [
                "Kill suspicious processes on device", 
                "Block external C2 domain via DNS sinkhole", 
                "Forced firmware re-flash recommended"
            ],
            "policy_violation": [
                "Disable unauthorized ports/services", 
                "Audit device session logs for privilege escalation", 
                "Re-enroll device in NAC system"
            ],
            "slow_poison": [
                "Reset ML baseline training points", 
                "Sanitize incoming data streams", 
                "Quarantine device for forensic analysis"
            ],
            "normal": [
                "Regular maintenance cycle", 
                "Update security signatures"
            ]
        }
        
        base_mitigation = mitigations.get(attack_type, ["Manual forensic audit required", "Isolate node"])
        
        if any("High periodicity" in ind for ind in indicators):
            base_mitigation.append("Monitor for Heartbeat patterns")
        
        return base_mitigation

    @staticmethod
    def create_report(pipeline_result):
        device_id = pipeline_result['device_id']
        attack_type = pipeline_result['attack_type']
        trust_score = pipeline_result['trust_score']
        drift_score = pipeline_result['drift_score']
        
        # 1. Detailed Drift Analysis (Upgrade 5)
        drift_details = []
        features = pipeline_result['features']
        baseline = pipeline_result['baseline']
        
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

        # 2. Indicators & SHAP (Upgrade 7)
        indicators = []
        fi = pipeline_result.get('feature_importance', {})
        sorted_fi = sorted(fi.items(), key=lambda x: abs(x[1]), reverse=True)[:3]
        
        for name, imp in sorted_fi:
            if abs(imp) > 0.05:
                indicators.append(f"High {name.replace('_', ' ')} impact ({imp:+.2f})")

        # 3. Device Context (Upgrade 9)
        age = pipeline_result.get('device_age')
        age_remark = ""
        if age is not None:
            if age > 5 and pipeline_result['anomaly_score'] < 0.1:
                age_remark = "Low anomaly score on legacy device (>5yr) suggests stable hardware integrity."
            elif age < 3 and pipeline_result['final_attack_score'] > 50:
                age_remark = "High risk detected on relatively new hardware (<3yr); prioritize cyber-attack over hardware failure."

        # 4. Assembly
        report = {
            "device_id": device_id,
            "timestamp": pipeline_result['timestamp'],
            "trust_score": f"{trust_score:.1f}",
            "attack_probability": f"{pipeline_result['final_attack_score']:.1f}%",
            "attack_breakdown": pipeline_result['attack_breakdown'],
            "drift_analysis": {
                "score": f"{drift_score:.1f}%",
                "details": drift_details
            },
            "policy_score": f"{pipeline_result['policy_score']:.1f}%",
            "indicators": indicators,
            "most_likely_attack": attack_type.replace("_", " ").title(),
            "xai_explanation": {
                "top_features": sorted_fi,
                "summary": f"The model detected {attack_type} primarily due to shifts in {', '.join([f[0] for f in sorted_fi])}. {age_remark}"
            },
            "recommendations": ReportGenerator.generate_mitigation(attack_type, trust_score, indicators)
        }
            
        return report
