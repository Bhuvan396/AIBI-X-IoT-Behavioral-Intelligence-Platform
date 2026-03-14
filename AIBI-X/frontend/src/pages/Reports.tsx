import React, { useState, useEffect } from 'react';
import type { Device, ExplainerReport } from '../services/api';
import { getDevices, getExplanation } from '../services/api';
import { FileText, ShieldAlert, CheckCircle, ArrowRight, ShieldCheck } from 'lucide-react';

const Reports: React.FC = () => {
  const [devices, setDevices] = useState<Device[]>([]);
  const [selectedId, setSelectedId] = useState('');
  const [report, setReport] = useState<ExplainerReport | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    getDevices().then(setDevices);
  }, []);

  const handleGenerate = async () => {
    if (!selectedId) return;
    setLoading(true);
    try {
      const res = await getExplanation(selectedId);
      setReport(res);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-8 pb-32">
      <h1 className="text-3xl font-extrabold text-white mb-8">Security Intel Reports</h1>
      
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
        <div className="lg:col-span-1 space-y-6">
          <div className="glass-panel p-6">
            <label className="block text-xs font-bold text-slate-500 uppercase tracking-widest mb-4">Select Target</label>
            <select 
              value={selectedId}
              onChange={(e) => setSelectedId(e.target.value)}
              className="w-full bg-cyber-dark border border-white/10 rounded-lg p-3 text-white focus:outline-none focus:border-cyber-cyan mb-6"
            >
              <option value="">Choose Device...</option>
              {devices.map(d => (
                <option key={d.device_id} value={d.device_id}>{d.device_id}</option>
              ))}
            </select>
            
            <button 
              onClick={handleGenerate}
              disabled={!selectedId || loading}
              className="w-full btn-primary disabled:opacity-50"
            >
              Generate Analysis
            </button>
          </div>
        </div>

        <div className="lg:col-span-3">
          {report ? (
            <div className="space-y-6 animate-fade-in">
              {/* Header Box */}
              <div className="glass-panel p-8 border-t-4 border-t-cyber-blue">
                <div className="flex justify-between items-start mb-8">
                  <div>
                    <h2 className="text-2xl font-bold text-white mb-1">Incident Report: {report.device_id}</h2>
                    <p className="text-slate-500 font-mono text-sm">{report.timestamp}</p>
                  </div>
                  <div className="text-right">
                    <p className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-1">Attack Probability</p>
                    <p className="text-3xl font-black text-cyber-danger">{report.attack_probability}</p>
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 p-6 bg-white/5 rounded-xl">
                  <div>
                    <p className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-2">Primary Diagnosis</p>
                    <p className="text-xl font-bold text-white flex items-center">
                      <ShieldAlert className="w-5 h-5 text-cyber-danger mr-2" />
                      {report.most_likely_attack}
                    </p>
                  </div>
                  <div>
                    <p className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-2">Trust Integrity</p>
                    <p className="text-xl font-bold text-white flex items-center">
                      <ShieldCheck className="w-5 h-5 text-emerald-500 mr-2" />
                      {report.trust_score}/100.0
                    </p>
                  </div>
                </div>
              </div>

              {/* Indicators */}
              <div className="glass-panel p-8">
                <h3 className="text-lg font-bold text-white mb-6 flex items-center">
                  <FileText className="w-5 h-5 mr-3 text-cyber-cyan" />
                  XAI Behavioral Indicators
                </h3>
                <div className="space-y-4">
                  {report.indicators.map((ind, i) => (
                    <div key={i} className="flex items-center space-x-4 p-4 bg-white/5 rounded-lg border border-white/5">
                      <div className="w-2 h-2 rounded-full bg-cyber-cyan" />
                      <span className="text-slate-300">{ind}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Mitigations */}
              <div className="glass-panel p-8 border-l-4 border-l-emerald-500">
                <h3 className="text-lg font-bold text-white mb-6 flex items-center">
                  <CheckCircle className="w-5 h-5 mr-3 text-emerald-500" />
                  Recommended Mitigation Actions
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {report.recommendations.map((rec, i) => (
                    <div key={i} className="flex items-start space-x-3 p-4 bg-emerald-500/10 rounded-lg group hover:bg-emerald-500/20 transition-colors">
                      <ArrowRight className="w-4 h-4 text-emerald-500 mt-1" />
                      <span className="text-emerald-50 font-medium">{rec}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          ) : (
            <div className="glass-panel p-20 flex flex-col items-center justify-center text-center">
               <div className="w-16 h-16 rounded-full bg-white/5 flex items-center justify-center mb-6">
                 <FileText className="w-8 h-8 text-slate-600" />
               </div>
               <h3 className="text-xl font-bold text-slate-400">No Analysis Selected</h3>
               <p className="text-slate-500 mt-2 max-w-sm">Select a device from the left panel to generate a comprehensive machine learning security audit report.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Reports;
