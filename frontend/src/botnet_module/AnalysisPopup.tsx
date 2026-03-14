import React from 'react';
import { X, AlertTriangle, ShieldCheck, Activity, Info, Fingerprint, Search } from 'lucide-react';

interface AnalysisPopupProps {
  isOpen: boolean;
  onClose: () => void;
  data: {
    is_anomaly: boolean;
    analysis: {
      type: string;
      confidence: string;
      description: string;
      indicators: string[];
      impact: string;
      affected_devices: string[];
      irregularities: string[];
      rationale: string[];
      forensics: {
        current: Record<string, number>;
        baseline: Record<string, number>;
      };
    };
  } | null;
}

export const AnalysisPopup: React.FC<AnalysisPopupProps> = ({ isOpen, onClose, data }) => {
  if (!isOpen || !data) return null;

  const { is_anomaly, analysis } = data;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm">
      <div className="w-full max-w-2xl bg-cyber-dark glass-panel border border-white/10 rounded-2xl shadow-2xl overflow-hidden animate-in fade-in zoom-in duration-300">
        <div className={`p-6 border-b border-white/10 flex items-center justify-between ${is_anomaly ? 'bg-cyber-danger/10' : 'bg-cyber-success/10'}`}>
          <div className="flex items-center space-x-3">
            {is_anomaly ? (
              <AlertTriangle className="w-8 h-8 text-cyber-danger" />
            ) : (
              <ShieldCheck className="w-8 h-8 text-cyber-success" />
            )}
            <div>
              <h2 className="text-2xl font-bold text-white">
                {is_anomaly ? 'Malicious Topology Detected' : 'Network Health Scan'}
              </h2>
              <p className="text-sm text-slate-400">Security Analysis AI Engine v2.0</p>
            </div>
          </div>
          <button onClick={onClose} className="p-2 rounded-lg hover:bg-white/10 transition-colors">
            <X className="w-6 h-6 text-slate-400" />
          </button>
        </div>

        <div className="p-8 space-y-8 overflow-y-auto max-h-[70vh]">
          {/* Classification Stats */}
          <div className="grid grid-cols-2 gap-6">
            <div className="p-4 rounded-xl bg-white/5 border border-white/5">
              <span className="text-xs font-bold text-slate-500 uppercase tracking-widest block mb-1">Botnet Type</span>
              <span className="text-xl font-bold text-cyber-cyan">{analysis.type}</span>
            </div>
            <div className="p-4 rounded-xl bg-white/5 border border-white/5">
              <span className="text-xs font-bold text-slate-500 uppercase tracking-widest block mb-1">AI Confidence</span>
              <span className="text-xl font-bold text-cyber-blue">{analysis.confidence}</span>
            </div>
          </div>
          {/* Description */}
          <div className="p-4 rounded-xl bg-cyber-blue/5 border border-cyber-blue/20">
             <p className="text-sm text-slate-300 leading-relaxed italic">
               "{analysis.description}"
             </p>
          </div>

          {/* Forensic Evidence - Proof for Judges */}
          <div className="space-y-4">
            <h3 className="flex items-center space-x-2 text-lg font-bold text-white">
              <Fingerprint className="w-5 h-5 text-cyber-cyan" />
              <span>Forensic Evidence (Baseline Comparison)</span>
            </h3>
            <div className="overflow-hidden rounded-xl border border-white/5 bg-white/5">
              <table className="w-full text-left text-xs">
                <thead>
                  <tr className="bg-white/10 text-slate-400">
                    <th className="px-4 py-2 font-bold uppercase tracking-wider">Metric Pattern</th>
                    <th className="px-4 py-2 font-bold uppercase tracking-wider">Baseline</th>
                    <th className="px-4 py-2 font-bold uppercase tracking-wider text-cyber-blue">Captured</th>
                    <th className="px-4 py-2 font-bold uppercase tracking-wider">Deviation</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-white/5">
                  {Object.keys(analysis.forensics.current).map((key) => {
                    const current = analysis.forensics.current[key];
                    const baseline = analysis.forensics.baseline[key];
                    const diff = ((current - baseline) / (baseline || 1)) * 100;
                    return (
                      <tr key={key} className="hover:bg-white/5 transition-colors">
                        <td className="px-4 py-3 text-slate-300 font-medium capitalize">{key.replace(/_/g, ' ')}</td>
                        <td className="px-4 py-3 text-slate-500 font-mono">{baseline}</td>
                        <td className="px-4 py-3 text-white font-bold font-mono">{current}</td>
                        <td className={`px-4 py-3 font-mono font-bold ${Math.abs(diff) > 10 ? 'text-cyber-danger' : 'text-cyber-success'}`}>
                          {diff > 0 ? '+' : ''}{diff.toFixed(1)}%
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
            
            {analysis.irregularities?.length > 0 && (
              <div className="p-4 rounded-xl bg-cyber-danger/5 border border-cyber-danger/20">
                <p className="text-xs font-bold text-cyber-danger uppercase mb-3 tracking-widest">Analysis Proof Checklist</p>
                <div className="space-y-2">
                  {analysis.irregularities.map((irr, i) => (
                    <div key={i} className="flex items-center space-x-2 text-xs text-slate-300">
                      <AlertTriangle className="w-3 h-3 text-cyber-danger" />
                      <span>{irr}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* AI Logic & Rationale - XAI Phase */}
          <div className="space-y-4">
            <h3 className="flex items-center space-x-2 text-lg font-bold text-white">
              <Search className="w-5 h-5 text-cyber-cyan" />
              <span>AI Logic & Rationale: "Why this result?"</span>
            </h3>
            <div className="p-4 rounded-xl bg-cyber-blue/5 border border-cyber-blue/20">
               <div className="space-y-3">
                 {analysis.rationale && analysis.rationale.length > 0 ? (
                   analysis.rationale.map((reason, i) => (
                     <div key={i} className="flex items-start space-x-3">
                       <span className="w-1.5 h-1.5 rounded-full bg-cyber-cyan mt-1.5 flex-shrink-0" />
                       <p className="text-sm text-slate-300 leading-relaxed font-medium">
                         {reason}
                       </p>
                     </div>
                   ))
                 ) : (
                   <p className="text-sm text-slate-400 italic">No significant deviations detected for logic generation.</p>
                 )}
               </div>
            </div>
          </div>

          {/* Indicators */}
          <div className="space-y-4">
            <h3 className="flex items-center space-x-2 text-lg font-bold text-white">
              <Activity className="w-5 h-5 text-cyber-blue" />
              <span>Suspicious Indicators</span>
            </h3>
            <div className="space-y-3">
              {analysis.indicators.map((indicator, idx) => (
                <div key={idx} className="flex items-start space-x-3 p-3 rounded-lg bg-white/5 border-l-2 border-cyber-blue">
                  <div className="w-1.5 h-1.5 rounded-full bg-cyber-blue mt-2" />
                  <span className="text-sm text-slate-300">{indicator}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Impact & Devices */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div className="space-y-4">
              <h3 className="flex items-center space-x-2 text-lg font-bold text-white">
                <Info className="w-5 h-5 text-cyber-danger" />
                <span>Impact Assessment</span>
              </h3>
              <p className="text-sm text-slate-400 italic">
                {analysis.impact}
              </p>
            </div>
            <div className="space-y-4">
              <h3 className="flex items-center space-x-2 text-lg font-bold text-white">
                <Network className="w-5 h-5 text-cyber-accent" />
                <span>Affected Devices</span>
              </h3>
              <div className="flex flex-wrap gap-2">
                {analysis.affected_devices.map((device) => (
                  <span key={device} className="px-3 py-1 bg-white/5 border border-white/10 rounded-full text-xs text-slate-300">
                    {device}
                  </span>
                ))}
              </div>
            </div>
          </div>
        </div>

        <div className="p-6 border-t border-white/10 flex justify-end">
          <button 
            onClick={onClose}
            className="px-8 py-3 bg-white/10 hover:bg-white/20 text-white font-bold rounded-xl transition-all"
          >
            Close Analysis
          </button>
        </div>
      </div>
    </div>
  );
};

import { Network } from 'lucide-react';
