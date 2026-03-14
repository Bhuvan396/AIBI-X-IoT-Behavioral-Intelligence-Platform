import React, { useState, useEffect } from 'react';
import { Activity, ShieldCheck, ShieldAlert, FileSearch, Zap, Network, SearchCode } from 'lucide-react';
import type { Device, DeviceStatus, ExplainerReport } from '../services/api';
import { getDevices, getDeviceStatus, getTrustHistory, analyzeNow, getExplanation } from '../services/api';
import DeviceCard from '../components/DeviceCard';
import TelemetryChart from '../components/TelemetryChart';
import AttackSelector from '../components/AttackSelector';

const Dashboard: React.FC = () => {
  const [devices, setDevices] = useState<Device[]>([]);
  const [statuses, setStatuses] = useState<Record<string, DeviceStatus>>({});
  const [selectedDeviceId, setSelectedDeviceId] = useState<string | null>(null);
  const [chartData, setChartData] = useState<any[]>([]);
  const [report, setReport] = useState<ExplainerReport | null>(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [analysisSuccess, setAnalysisSuccess] = useState<boolean | null>(null);
  const [showAttackScore, setShowAttackScore] = useState(false);

  const fetchOverviewData = async () => {
    try {
      const deviceList = await getDevices();
      setDevices(deviceList);
      
      const statusMap: Record<string, DeviceStatus> = {};
      for (const dev of deviceList) {
        const s = await getDeviceStatus(dev.device_id);
        statusMap[dev.device_id] = s;
      }
      setStatuses(statusMap);
      
      const targetId = selectedDeviceId || deviceList[0]?.device_id;
      if (targetId) {
        if (!selectedDeviceId) setSelectedDeviceId(targetId);
        
        // 1. Fetch History for the Chart
        try {
          const history = await getTrustHistory(targetId);
          setChartData(history.map((h: any) => ({
            time: new Date(h.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' }),
            value: (h.trust_score || 0)
          })));
        } catch (e) {
          setChartData([]);
        }

        // 2. Fetch detailed report, ignore 404 if no telemetry yet
        try {
          const exp = await getExplanation(targetId);
          setReport(exp);
        } catch (e) {
          setReport(null);
        }
      }
    } catch (err) {
      console.error(err);
    }
  };

  const handleAnalyzeNow = async () => {
    if (!selectedDeviceId) return;
    setAnalyzing(true);
    setAnalysisSuccess(null);
    try {
      await analyzeNow(selectedDeviceId);
      await fetchOverviewData();
      setAnalysisSuccess(true);
      setTimeout(() => setAnalysisSuccess(null), 3000);
    } catch (err) {
      console.error("Analysis failed", err);
      setAnalysisSuccess(false);
      setTimeout(() => setAnalysisSuccess(null), 3000);
    } finally {
      setAnalyzing(false);
    }
  };

  useEffect(() => {
    fetchOverviewData();
    const interval = setInterval(fetchOverviewData, 10000); // Poll every 10s (Upgrade 12)
    return () => clearInterval(interval);
  }, [selectedDeviceId]);

  const selectedStatus = selectedDeviceId ? statuses[selectedDeviceId] : null;

  return (
    <div className="p-8 pb-32 min-h-screen">
      <header className="flex flex-col md:flex-row justify-between items-start md:items-center space-y-4 md:space-y-0 mb-8">
        <div>
          <h1 className="text-3xl font-extrabold bg-clip-text text-transparent bg-gradient-to-r from-white to-slate-400">
            AIBI-X Command Center
          </h1>
          <p className="text-slate-500 mt-2 flex items-center">
            <span className="w-2 h-2 rounded-full bg-cyber-blue mr-2 animate-pulse" />
            Active Real-Time Monitoring: <span className="text-cyber-blue ml-1 font-mono">{devices.length} Nodes</span>
          </p>
        </div>
        <div className="flex flex-wrap gap-4">
          <button 
            onClick={handleAnalyzeNow}
            disabled={analyzing}
            className={`btn-primary flex items-center space-x-2 ${analyzing ? 'opacity-50' : ''} ${analysisSuccess === true ? 'bg-emerald-500' : analysisSuccess === false ? 'bg-cyber-danger' : ''}`}
          >
            <Zap className={`w-4 h-4 ${analyzing ? 'animate-spin' : ''}`} />
            <span>
              {analyzing ? 'Ingesting...' : analysisSuccess === true ? 'Ready' : analysisSuccess === false ? 'Failed' : 'Analyze Now'}
            </span>
          </button>
          <button 
            onClick={() => setShowAttackScore(!showAttackScore)}
            className="btn-outline border-cyber-blue/30 text-cyber-blue flex items-center space-x-2"
          >
            <ShieldAlert className="w-4 h-4" />
            <span>Check Attack Score</span>
          </button>
        </div>
      </header>

      {/* Modern Dashboard Layout */}
      <div className="grid grid-cols-1 xl:grid-cols-4 gap-6">
        
        {/* Left Column: Device Grid */}
        <div className="xl:col-span-1 space-y-6">
          <div className="glass-panel p-6 h-full border-l-4 border-cyber-blue">
            <h2 className="text-lg font-bold text-white mb-4 flex items-center">
              <Network className="w-5 h-5 mr-3 text-cyber-blue" />
              Infrastructure
            </h2>
            <div className="space-y-3 max-h-[600px] overflow-y-auto pr-2 custom-scrollbar">
              {devices.map((device) => (
                <DeviceCard
                  key={device.device_id}
                  device={{
                    id: device.device_id,
                    type: device.device_type,
                    ip: device.ip_address,
                    status: statuses[device.device_id]?.trust_score < 60 ? 'Critical' : 'Operational',
                    trust_score: statuses[device.device_id]?.trust_score
                  } as any}
                  onClick={() => setSelectedDeviceId(device.device_id)}
                />
              ))}
            </div>
          </div>
        </div>

        {/* Center/Right Column: Multi-Panel Analysis (Upgrade 12) */}
        <div className="xl:col-span-3 space-y-6">
          
          {selectedDeviceId && selectedStatus ? (
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              
              {/* Trust & History */}
              <div className="lg:col-span-2 space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                   <div className="glass-panel p-6 flex flex-col items-center justify-center relative overflow-hidden">
                      <div className="absolute top-0 right-0 p-2 opacity-10"><Activity className="w-12 h-12" /></div>
                      <p className="text-sm text-slate-400 mb-2">Trust Score</p>
                      <h3 className={`text-5xl font-black mb-2 ${selectedStatus.trust_score < 70 ? 'text-cyber-danger' : 'text-emerald-500'}`}>
                        {selectedStatus.trust_score?.toFixed(0) || '0'}
                      </h3>
                      <div className="w-full bg-white/5 h-1.5 rounded-full mt-2">
                        <div className={`h-full rounded-full transition-all duration-1000 ${selectedStatus.trust_score < 70 ? 'bg-cyber-danger' : 'bg-emerald-500'}`} style={{ width: `${selectedStatus.trust_score || 0}%` }} />
                      </div>
                   </div>
                   <div className="glass-panel p-6">
                      <p className="text-sm text-slate-400 mb-2">Drift Level</p>
                      <h3 className="text-3xl font-bold text-cyber-blue">{(selectedStatus.drift_score || 0).toFixed(1)}%</h3>
                      <p className="text-xs text-slate-500 mt-2">Variation from baseline</p>
                   </div>
                   <div className="glass-panel p-6">
                      <p className="text-sm text-slate-400 mb-2">Policy Risk</p>
                      <h3 className={`text-3xl font-bold ${selectedStatus.policy_score > 30 ? 'text-cyber-warning' : 'text-white'}`}>
                        {(selectedStatus.policy_score || 0).toFixed(1)}%
                      </h3>
                      <p className="text-xs text-slate-500 mt-2">Violation probability</p>
                   </div>
                </div>

                <div className="glass-panel p-6">
                   <h2 className="text-xl font-bold text-white mb-6">Behavioral Trend</h2>
                   <div className="h-[300px]">
                      <TelemetryChart title="" data={chartData} />
                   </div>
                </div>

                {/* Recommendations Panel */}
                <div className="glass-panel p-6 border-t-4 border-emerald-500/50">
                  <h2 className="text-lg font-bold text-white mb-4 flex items-center">
                    <ShieldCheck className="w-5 h-5 mr-3 text-emerald-500" />
                    Security Recommendations
                  </h2>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    {report?.recommendations.map((rec, i) => (
                      <div key={i} className="flex items-start space-x-3 p-3 rounded-lg bg-emerald-500/5 border border-emerald-500/10">
                        <div className="w-1.5 h-1.5 rounded-full bg-emerald-500 mt-2 flex-shrink-0" />
                        <span className="text-emerald-50/80 text-sm leading-relaxed">{rec}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              {/* Sidebar: Explainable AI & Breakdown */}
              <div className="space-y-6">
                
                {/* Attack Probability Breakdown */}
                <div className="glass-panel p-6">
                  <h2 className="text-lg font-bold text-white mb-4">Attack Breakdown</h2>
                  <div className="space-y-3">
                    {Object.entries(selectedStatus.attack_breakdown || {}).sort((a,b)=>b[1]-a[1]).map(([type, prob]) => (
                      <div key={type} className="space-y-1">
                        <div className="flex justify-between text-xs">
                          <span className="text-slate-400 uppercase tracking-wider">{type.replace('_', ' ')}</span>
                          <span className="text-white font-mono">{prob.toFixed(1)}%</span>
                        </div>
                        <div className="w-full h-1 bg-white/5 rounded-full">
                          <div 
                            className={`h-full rounded-full ${prob > 50 ? 'bg-cyber-danger' : 'bg-cyber-blue/40'}`} 
                            style={{ width: `${prob}%` }} 
                          />
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* XAI Panel (Upgrade 7) */}
                <div className="glass-panel p-6 bg-cyber-blue/5 border border-cyber-blue/10">
                  <h2 className="text-lg font-bold text-white mb-4 flex items-center">
                    <SearchCode className="w-5 h-5 mr-3 text-cyber-blue" />
                    Explainable AI
                  </h2>
                  <p className="text-sm text-slate-300 italic mb-4">"{report?.xai_explanation.summary}"</p>
                  <div className="space-y-2">
                    <p className="text-xs font-bold text-cyber-blue uppercase mb-2">Top Drivers</p>
                    {report?.xai_explanation.top_features.map(([feat, imp]) => (
                      <div key={feat} className="flex justify-between items-center text-xs py-1">
                        <span className="text-slate-400">{feat.replace('_', ' ')}</span>
                        <span className={`px-2 py-0.5 rounded font-mono ${imp > 0 ? 'bg-cyber-danger/20 text-cyber-danger' : 'bg-emerald-500/20 text-emerald-500'}`}>
                          {imp > 0 ? '+' : ''}{imp.toFixed(3)}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="glass-panel p-6">
                   <h2 className="text-lg font-bold text-white mb-4">Attack Control</h2>
                   <AttackSelector deviceId={selectedDeviceId} />
                </div>
              </div>

            </div>
          ) : (
            <div className="h-full flex items-center justify-center glass-panel opacity-50 p-20 text-center">
              <div>
                <Activity className="w-16 h-16 mx-auto mb-6 animate-pulse text-cyber-blue" />
                <h2 className="text-2xl font-bold text-white mb-2">Initializing Uplink</h2>
                <p className="text-slate-400">Negotiating telemetry channels with IoT infrastructure...</p>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Attack Analysis Overlay (Upgrade 8) */}
      {showAttackScore && selectedStatus && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-6 bg-black/80 backdrop-blur-sm">
          <div className="glass-panel w-full max-w-4xl p-8 border-cyber-danger/30 shadow-2xl shadow-cyber-danger/10">
             <div className="flex justify-between items-center mb-8">
                <div className="flex items-center space-x-4">
                  <div className="p-3 bg-cyber-danger/10 rounded-xl"><ShieldAlert className="text-cyber-danger w-8 h-8" /></div>
                  <div>
                    <h2 className="text-3xl font-black text-white italic tracking-tighter uppercase">Deep Threat Analysis</h2>
                    <p className="text-cyber-blue/70 font-mono text-sm underline">Source Node: {selectedDeviceId}</p>
                  </div>
                </div>
                <button onClick={() => setShowAttackScore(false)} className="text-slate-400 hover:text-white">&times; Close Analysis</button>
             </div>

             <div className="grid grid-cols-1 md:grid-cols-2 gap-10">
                <div className="space-y-8">
                   <div>
                      <h3 className="text-cyber-danger text-sm font-bold uppercase mb-4 tracking-[0.2em]">Primary Risk Probability</h3>
                      <div className="flex items-end space-x-4">
                         <span className="text-7xl font-black text-white">{selectedStatus.attack_probability.toFixed(1)}</span>
                         <span className="text-2xl font-bold text-cyber-danger pb-2">%</span>
                      </div>
                   </div>
                   
                   <div className="space-y-4">
                      {Object.entries(selectedStatus.attack_breakdown || {}).sort((a,b)=>b[1]-a[1]).map(([type, prob]) => (
                        <div key={type} className="flex justify-between border-b border-white/5 pb-2">
                           <span className="text-slate-300 font-medium">{type.replace('_', ' ').toUpperCase()}</span>
                           <span className="text-cyber-blue font-mono">{prob.toFixed(2)}%</span>
                        </div>
                      ))}
                   </div>
                </div>

                <div className="bg-cyber-blue/5 p-6 rounded-2xl border border-cyber-blue/10">
                   <h3 className="text-white text-lg font-bold mb-6 flex items-center">
                     <FileSearch className="w-5 h-5 mr-3 text-cyber-blue" />
                     Inference Forensics
                   </h3>
                   <div className="space-y-6">
                      <div className="p-4 bg-black/40 rounded-xl border-l-4 border-cyber-danger">
                         <p className="text-xs text-cyber-danger uppercase font-bold mb-2">Automated Conclusion</p>
                         <p className="text-sm text-slate-300 leading-relaxed italic">
                           "The neural classifier suggests a <strong>{selectedStatus.predicted_attack_type}</strong> intrusion with high confidence. 
                           Behavioral drift of {selectedStatus.drift_score.toFixed(1)}% confirms active evasion attempts."
                         </p>
                      </div>
                      <div className="space-y-3">
                         <p className="text-xs text-slate-500 uppercase font-bold">Contributor Importance (SHAP)</p>
                         {report?.xai_explanation.top_features.map(([feat, imp]) => (
                           <div key={feat} className="flex items-center space-x-4">
                              <span className="w-24 text-[10px] text-slate-400 truncate uppercase">{feat.replace('_', ' ')}</span>
                              <div className="flex-1 h-3 bg-white/5 rounded-full overflow-hidden flex">
                                 {imp > 0 ? (
                                   <div className="bg-cyber-danger h-full ml-1/2" style={{ marginLeft: '50%', width: `${Math.min(50, imp * 100)}%` }} />
                                 ) : (
                                   <div className="bg-emerald-500 h-full" style={{ width: `${Math.min(50, Math.abs(imp * 100))}%`, marginLeft: `${50 - Math.min(50, Math.abs(imp * 100))}%` }} />
                                 )}
                              </div>
                           </div>
                         ))}
                      </div>
                   </div>
                </div>
             </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;
