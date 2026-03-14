import React, { useState } from 'react';
import { injectAttack } from '../services/api';
import { ShieldAlert, Activity, ChevronDown, CheckCircle2 } from 'lucide-react';

interface Props {
  deviceId: string;
}

const ATTACK_TYPES = [
  { id: 'recon', name: 'Reconnaissance', desc: 'Simulate port scanning and enumeration', color: 'text-amber-400', bg: 'bg-amber-400/10' },
  { id: 'exfiltration', name: 'Data Exfiltration', desc: 'Simulate large outbound data transfer', color: 'text-red-500', bg: 'bg-red-500/10' },
  { id: 'c2_beaconing', name: 'C2 Beaconing', desc: 'Simulate periodic command & control', color: 'text-purple-500', bg: 'bg-purple-500/10' },
  { id: 'policy_violation', name: 'Policy Violation', desc: 'Simulate unauthorized service access', color: 'text-orange-500', bg: 'bg-orange-500/10' },
  { id: 'slow_poison', name: 'Slow Poisoning', desc: 'Simulate gradual anomaly injection', color: 'text-emerald-500', bg: 'bg-emerald-500/10' },
];

const AttackSelector: React.FC<Props> = ({ deviceId }) => {
  const [selectedAttack, setSelectedAttack] = useState(ATTACK_TYPES[0]);
  const [isOpen, setIsOpen] = useState(false);
  const [status, setStatus] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleInject = async () => {
    setLoading(true);
    setStatus(null);
    try {
      await injectAttack({ device_id: deviceId, attack_type: selectedAttack.id });
      setStatus(`Success: Injected ${selectedAttack.name}`);
    } catch (error) {
      setStatus(`Error: Failed to inject attack`);
    } finally {
      setLoading(false);
      setTimeout(() => setStatus(null), 3000);
    }
  };

  return (
    <div className="glass-panel p-6">
      <div className="flex items-center space-x-3 mb-6">
        <div className="w-10 h-10 rounded-xl bg-cyber-danger/10 flex items-center justify-center flex-shrink-0">
          <ShieldAlert className="w-5 h-5 text-cyber-danger" />
        </div>
        <div>
          <h2 className="text-xl font-bold text-white">Targeted Injection</h2>
          <p className="text-sm text-slate-400 flex items-center">Target: <span className="font-mono text-cyber-cyan ml-2 px-2 py-0.5 rounded bg-cyber-cyan/10">{deviceId}</span></p>
        </div>
      </div>

      <div className="relative mb-6">
        <div 
          className="w-full glass-panel cursor-pointer flex items-center justify-between p-4 hover:border-cyber-cyan/50 transition-colors group"
          onClick={() => setIsOpen(!isOpen)}
        >
          <div className="flex items-center space-x-3">
            <div className={`p-2 rounded-lg ${selectedAttack.bg}`}>
              <Activity className={`w-5 h-5 ${selectedAttack.color}`} />
            </div>
            <div className="flex flex-col">
              <span className="font-bold text-white">{selectedAttack.name}</span>
              <span className="text-xs text-slate-400">{selectedAttack.desc}</span>
            </div>
          </div>
          <ChevronDown className={`w-5 h-5 text-slate-400 transition-transform ${isOpen ? 'rotate-180' : ''}`} />
        </div>
        
        {isOpen && (
          <div className="absolute top-full left-0 right-0 mt-2 glass-panel z-50 py-2 shadow-2xl overflow-hidden max-h-64 overflow-y-auto">
            {ATTACK_TYPES.map((attack) => (
              <div
                key={attack.id}
                className="px-4 py-3 hover:bg-white/5 cursor-pointer flex items-center space-x-3 transition-colors"
                onClick={() => {
                  setSelectedAttack(attack);
                  setIsOpen(false);
                }}
              >
                <div className={`p-2 rounded-lg ${attack.bg}`}>
                  <Activity className={`w-4 h-4 ${attack.color}`} />
                </div>
                <div className="flex flex-col">
                  <span className="font-semibold text-white">{attack.name}</span>
                  <span className="text-xs text-slate-500">{attack.desc}</span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      <button
        onClick={handleInject}
        disabled={loading || !deviceId}
        className={`w-full relative overflow-hidden group btn-danger ${loading || !deviceId ? 'opacity-50 cursor-not-allowed' : ''}`}
      >
        <div className="absolute inset-0 bg-white/20 translate-y-full group-hover:translate-y-0 transition-transform duration-300" />
        <span className="relative z-10 font-bold uppercase tracking-widest flex items-center justify-center space-x-2">
          {loading ? <Activity className="w-4 h-4 animate-spin" /> : <ShieldAlert className="w-4 h-4" />}
          <span>{loading ? 'Injecting...' : 'Force Demo Attack'}</span>
        </span>
      </button>

      {status && (
        <div className={`mt-4 p-3 rounded-lg text-sm flex items-center space-x-2 font-medium ${status.includes('Error') ? 'bg-red-500/20 text-red-400 border border-red-500/30' : 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'}`}>
          <CheckCircle2 className="w-4 h-4 flex-shrink-0" />
          <span>{status}</span>
        </div>
      )}
    </div>
  );
};

export default AttackSelector;
