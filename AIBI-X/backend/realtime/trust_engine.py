"""
Unified Trust Engine — Section 14 formula:

RiskScore = 0.20 * AttackProbability
          + 0.15 * DigitalTwinDeviation
          + 0.10 * TemporalDeviation
          + 0.10 * AdversarialScore
          + 0.10 * PolicyScore
          + 0.10 * PredictionTrend
          + 0.10 * FutureRisk
          + 0.10 * SlowPoisonScore
          + 0.05 * AgeFactor

TrustScore = 100 - RiskScore
"""
import pandas as pd
import os

TRUST_CSV = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/trust_scores.csv'))


class UnifiedTrustEngine:
    def compute_policy_score(self, device_id: str, features: dict, device_type: str) -> float:
        """Behavioral policy violation check against policies.csv."""
        POLICY_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/policies.csv'))
        if not os.path.exists(POLICY_PATH):
            return 0.0
            
        try:
            policies_df = pd.read_csv(POLICY_PATH)
            # Ensure no whitespace in column or data
            policies_df['device_type'] = policies_df['device_type'].astype(str).str.strip()
            
            target_type = str(device_type).strip()
            policy = policies_df[policies_df['device_type'] == target_type]
            
            if policy.empty:
                # Try generic match
                policy = policies_df[policies_df['device_type'] == '*']
                if policy.empty:
                    return 0.0
                
            row = policy.iloc[0]
            allowed_ports = [p.strip() for p in str(row['allowed_ports']).split(',')]
            allowed_dests = [d.strip() for d in str(row['allowed_destinations']).split(',')]
            
            score = 0.0
            curr_port = str(features.get('most_freq_port', '')).strip()
            curr_dest = str(features.get('most_freq_ip', '')).strip()
            
            if '*' not in allowed_ports and curr_port not in allowed_ports:
                score += 50
            if '*' not in allowed_dests and curr_dest not in allowed_dests:
                score += 50
                
            return float(min(100.0, score))
        except Exception as e:
            print(f"Policy check error: {e}")
            return 0.0

    def compute_trust(
        self,
        device_id: str,
        attack_probability: float,
        digital_twin_deviation: float,
        temporal_deviation: float,
        adversarial_score: float,
        policy_score: float,
        prediction_trend: float,
        future_risk: float,
        slow_poison_score: float,
        age_factor: float
    ) -> dict:
        """
        Compute unified risk and trust scores.
        All inputs are 0-100 scale.
        """
        risk_score = (
            0.20 * min(100, attack_probability) +
            0.15 * min(100, digital_twin_deviation) +
            0.10 * min(100, temporal_deviation) +
            0.10 * min(100, adversarial_score) +
            0.10 * min(100, prediction_trend) +
            0.10 * min(100, future_risk) +
            0.10 * min(100, slow_poison_score) +
            0.05 * min(100, age_factor)
        )
        
        risk_score = min(100.0, max(0.0, risk_score))
        trust_score = max(0.0, 100.0 - risk_score)

        # Log trust score
        self._log_trust(device_id, trust_score, risk_score)

        return {
            'trust_score': trust_score,
            'risk_score': risk_score,
            'policy_score': policy_score
        }

    def _log_trust(self, device_id, trust_score, risk_score):
        try:
            if not os.path.exists(TRUST_CSV):
                pd.DataFrame(columns=['timestamp', 'device_id', 'trust_score', 'risk_score']).to_csv(TRUST_CSV, index=False)
            row = pd.DataFrame([{
                'timestamp': pd.Timestamp.now(tz='UTC').isoformat(),
                'device_id': device_id,
                'trust_score': trust_score,
                'risk_score': risk_score
            }])
            row.to_csv(TRUST_CSV, mode='a', header=False, index=False)
        except Exception:
            pass
