import axios from 'axios';

const API_BASE = 'http://localhost:8888';

export interface Device {
  device_id: string;
  ip_address: string;
  device_type: string;
}

export interface DeviceStatus {
  device_id: string;
  trust_score: number;
  last_anomaly_score: number;
  predicted_attack_type: string;
  attack_probability: number;
  attack_breakdown: Record<string, number>;
  policy_score: number;
  drift_score: number;
}

export interface ExplainerReport {
  device_id: string;
  timestamp: string;
  trust_score: string;
  attack_probability: string;
  attack_breakdown: Record<string, number>;
  drift_analysis: {
    score: string;
    details: Array<{
      feature: string;
      baseline: number;
      current: number;
      deviation: string;
    }>;
  };
  policy_score: string;
  indicators: string[];
  most_likely_attack: string;
  xai_explanation: {
    top_features: Array<[string, number]>;
    summary: string;
  };
  recommendations: string[];
}

export const getDevices = async (): Promise<Device[]> => {
  const response = await axios.get(`${API_BASE}/devices`);
  return response.data;
};

export const getDeviceStatus = async (deviceId: string): Promise<DeviceStatus> => {
  const response = await axios.get(`${API_BASE}/device/${deviceId}/status`);
  return response.data;
};

export const getTrustHistory = async (deviceId: string) => {
  const response = await axios.get(`${API_BASE}/trust/history/${deviceId}`);
  return response.data;
};

export const getExplanation = async (deviceId: string): Promise<ExplainerReport> => {
  const response = await axios.get(`${API_BASE}/explain/${deviceId}`);
  return response.data;
};

export const analyzeNow = async (deviceId: string) => {
  const response = await axios.post(`${API_BASE}/analyze_now`, { device_id: deviceId });
  return response.data;
};

export const injectAttack = async (payload: { device_id: string, attack_type: string }) => {
  const response = await axios.post(`${API_BASE}/inject_attack`, payload);
  return response.data;
};
