import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { BotnetSidebar } from './BotnetSidebar';
import { NetworkGraph } from './NetworkGraph';
import { AnalysisPopup } from './AnalysisPopup';
import { RefreshCw, Play, ShieldCheck, Bug, ShieldOff, ShieldAlert } from 'lucide-react';

const API_BASE = 'http://localhost:8888/botnet';

const BotnetTopologyPage: React.FC = () => {
  const [topology, setTopology] = useState<{ nodes: any[]; edges: any[] }>({ nodes: [], edges: [] });
  const [isAnalysisOpen, setIsAnalysisOpen] = useState(false);
  const [analysisData, setAnalysisData] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [intakeBlocked, setIntakeBlocked] = useState(false);
  const [intakeToggling, setIntakeToggling] = useState(false);

  const fetchTopology = async () => {
    try {
      const res = await axios.get(`${API_BASE}/topology`);
      setTopology(res.data);
    } catch (err) {
      console.error('Error fetching topology:', err);
    }
  };

  const fetchIntakeStatus = async () => {
    try {
      const res = await axios.get(`${API_BASE}/intake-status`);
      setIntakeBlocked(res.data.blocked);
    } catch (err) {
      console.error('Error fetching intake status:', err);
    }
  };

  useEffect(() => {
    fetchTopology();
    fetchIntakeStatus();
  }, []);

  const handleInject = async (type: string) => {
    setIsLoading(true);
    try {
      await axios.post(`${API_BASE}/inject`, { botnet_type: type });
      await fetchTopology();
    } catch (err) {
      console.error('Error injecting botnet:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = async () => {
    try {
      await axios.post(`${API_BASE}/reset`);
      await fetchTopology();
      setAnalysisData(null);
    } catch (err) {
      console.error('Error resetting topology:', err);
    }
  };

  const runAnalysis = async () => {
    setIsAnalyzing(true);
    try {
      const res = await axios.get(`${API_BASE}/analysis`);
      setAnalysisData(res.data);
      setIsAnalysisOpen(true);
    } catch (err) {
      console.error('Error running analysis:', err);
    } finally {
      setIsAnalyzing(false);
    }
  };

  const toggleIntake = async () => {
    setIntakeToggling(true);
    try {
      const endpoint = intakeBlocked ? '/unblock-intake' : '/block-intake';
      const res = await axios.post(`${API_BASE}${endpoint}`);
      setIntakeBlocked(res.data.blocked);
    } catch (err) {
      console.error('Error toggling intake:', err);
    } finally {
      setIntakeToggling(false);
    }
  };

  return (
    <div className="flex h-full w-full overflow-hidden">
      {/* Sidebar */}
      <BotnetSidebar onInject={handleInject} isLoading={isLoading} />

      {/* Main Area */}
      <div className="flex-1 flex flex-col p-8 relative">
        {/* Header Controls */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold text-white mb-2">Botnet Topology Lab</h1>
            <p className="text-slate-400">Simulate and detect malicious IoT network reconfigurations.</p>
          </div>
          <div className="flex items-center space-x-4">
            {/* Block Intake Button */}
            <button
              onClick={toggleIntake}
              disabled={intakeToggling}
              className={`flex items-center space-x-2 px-6 py-3 rounded-xl border font-bold transition-all
                ${intakeBlocked
                  ? 'bg-cyber-danger/20 border-cyber-danger/50 text-cyber-danger hover:bg-cyber-danger/30 shadow-lg shadow-cyber-danger/20'
                  : 'bg-white/5 border-white/10 text-slate-300 hover:bg-white/10'
                }`}
            >
              {intakeToggling ? (
                <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
              ) : intakeBlocked ? (
                <ShieldOff className="w-4 h-4" />
              ) : (
                <ShieldAlert className="w-4 h-4" />
              )}
              <span>{intakeBlocked ? 'Unblock Intake' : 'Block Intake'}</span>
            </button>

            <button
              onClick={handleReset}
              className="flex items-center space-x-2 px-6 py-3 bg-white/5 border border-white/10 rounded-xl hover:bg-white/10 transition-all text-slate-300 font-bold"
            >
              <RefreshCw className="w-4 h-4" />
              <span>Reset Topology</span>
            </button>
            <button
              onClick={runAnalysis}
              disabled={isAnalyzing}
              className="flex items-center space-x-2 px-8 py-3 bg-gradient-to-r from-cyber-blue to-cyber-cyan rounded-xl shadow-lg shadow-cyber-blue/30 hover:scale-105 active:scale-95 transition-all text-white font-bold"
            >
              {isAnalyzing ? (
                <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
              ) : (
                <>
                  <Play className="w-5 h-5 fill-current" />
                  <span>Run Analysis</span>
                </>
              )}
            </button>
          </div>
        </div>

        {/* Graph Display */}
        <div className="flex-1 min-h-0">
          <NetworkGraph nodes={topology.nodes} edges={topology.edges} />
        </div>

        {/* Mini Alerts */}
        {analysisData?.is_anomaly && (
          <div className="absolute bottom-12 right-12 p-6 glass-panel border border-cyber-danger/30 bg-cyber-danger/5 rounded-2xl shadow-2xl animate-bounce">
            <div className="flex items-center space-x-4">
              <div className="w-12 h-12 rounded-xl bg-cyber-danger flex items-center justify-center shadow-lg shadow-cyber-danger/50">
                <Bug className="w-7 h-7 text-white" />
              </div>
              <div>
                <div className="text-xs font-bold text-cyber-danger uppercase tracking-widest">Topology Alert</div>
                <div className="text-lg font-bold text-white leading-tight">Botnet Infiltration Detected</div>
              </div>
            </div>
          </div>
        )}

        {/* Analysis Result Summary Overlay */}
        {analysisData && !isAnalysisOpen && (
          <div className="absolute top-32 left-1/2 -translate-x-1/2 flex items-center space-x-2 px-6 py-2 bg-slate-900/90 backdrop-blur-md rounded-full border border-white/10 shadow-2xl z-20">
            <ShieldCheck className="w-4 h-4 text-cyber-success" />
            <span className="text-sm font-bold text-white">Latest Analysis:</span>
            <span className="text-sm text-slate-300 font-medium">
              {analysisData.analysis.type} ({analysisData.analysis.confidence})
            </span>
            <button onClick={() => setIsAnalysisOpen(true)} className="text-xs text-cyber-blue font-bold hover:underline ml-2">
              View Detailed Report
            </button>
          </div>
        )}

        {/* Intake Blocked Persistent Badge */}
        {intakeBlocked && (
          <div className="absolute top-6 left-1/2 -translate-x-1/2 flex items-center space-x-3 px-5 py-2.5 bg-cyber-danger/20 backdrop-blur-md rounded-full border border-cyber-danger/50 shadow-2xl shadow-cyber-danger/20 z-30 animate-pulse">
            <ShieldOff className="w-4 h-4 text-cyber-danger" />
            <span className="text-sm font-bold text-cyber-danger tracking-wide">⛔ TELEMETRY INTAKE BLOCKED — Devices cannot send data</span>
          </div>
        )}
      </div>

      {/* Analysis Popup */}
      <AnalysisPopup 
        isOpen={isAnalysisOpen} 
        onClose={() => setIsAnalysisOpen(false)} 
        data={analysisData} 
      />
    </div>
  );
};

export default BotnetTopologyPage;
