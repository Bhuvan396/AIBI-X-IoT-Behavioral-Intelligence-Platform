import React, { useState, useEffect } from 'react';
import NetworkGraph from './NetworkGraph';
import BotnetSidebar from './BotnetSidebar';
import TopologyControls from './TopologyControls';
import AnalysisPopup from './AnalysisPopup';
import axios from 'axios';

const API_BASE = 'http://localhost:8888/botnet-lab';

const BotnetTopologyPage: React.FC = () => {
  const [nodes, setNodes] = useState([]);
  const [edges, setEdges] = useState([]);
  const [activeBotnet, setActiveBotnet] = useState<string | null>(null);
  const [isIntakeBlocked, setIsIntakeBlocked] = useState(false);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState(null);

  // Load topology
  const fetchTopology = async () => {
    try {
      const res = await axios.get(`${API_BASE}/topology`);
      setNodes(res.data.nodes);
      setEdges(res.data.edges);
    } catch (err) {
      console.error('Failed to fetch topology:', err);
    }
  };

  // Load intake status
  const fetchIntakeStatus = async () => {
    try {
      const res = await axios.get(`${API_BASE}/intake-status`);
      setIsIntakeBlocked(res.data.blocked);
    } catch (err) {
      console.error('Failed to fetch intake status:', err);
    }
  };

  useEffect(() => {
    fetchTopology();
    fetchIntakeStatus();
    const interval = setInterval(fetchIntakeStatus, 3000);
    return () => clearInterval(interval);
  }, []);

  const handleInject = async (type: string) => {
    try {
      const res = await axios.post(`${API_BASE}/inject`, { botnet_type: type });
      setNodes(res.data.nodes);
      setEdges(res.data.edges);
      setActiveBotnet(type);
    } catch (err) {
      console.error('Injection failed:', err);
    }
  };

  const handleReset = async () => {
    try {
      const res = await axios.post(`${API_BASE}/reset`);
      setNodes(res.data.nodes);
      setEdges(res.data.edges);
      setActiveBotnet(null);
      setAnalysisResult(null);
    } catch (err) {
      console.error('Reset failed:', err);
    }
  };

  const handleAnalyze = async () => {
    setIsAnalyzing(true);
    try {
      // Simulate delay for dramatic effect
      await new Promise(r => setTimeout(r, 2000));
      const res = await axios.get(`${API_BASE}/analyze`);
      setAnalysisResult(res.data);
    } catch (err) {
      console.error('Analysis failed:', err);
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleToggleIntake = async () => {
    try {
      const endpoint = isIntakeBlocked ? 'unblock-intake' : 'block-intake';
      await axios.post(`${API_BASE}/${endpoint}`);
      setIsIntakeBlocked(!isIntakeBlocked);
    } catch (err) {
      console.error('Intake toggle failed:', err);
    }
  };

  return (
    <div className="flex h-full w-full overflow-hidden bg-black">
      {/* Main Graph Area */}
      <div className="flex-1 relative flex flex-col h-full overflow-hidden">
        <TypographyHeader activeBotnet={activeBotnet} />
        
        <div className="flex-1 relative">
          <NetworkGraph nodes={nodes} edges={edges} />
          
          <TopologyControls 
            onAnalyze={handleAnalyze}
            onReset={handleReset}
            onToggleIntake={handleToggleIntake}
            isIntakeBlocked={isIntakeBlocked}
            isAnalyzing={isAnalyzing}
          />
        </div>
      </div>

      {/* Sidebar */}
      <BotnetSidebar 
        onInject={handleInject}
        activeBotnet={activeBotnet}
      />

      {/* Popups */}
      {analysisResult && (
        <AnalysisPopup 
          data={analysisResult} 
          onClose={() => setAnalysisResult(null)} 
        />
      )}
    </div>
  );
};

const TypographyHeader = ({ activeBotnet }: { activeBotnet: string | null }) => (
  <div className="px-8 py-6 bg-slate-900 border-b border-white/5 flex items-center justify-between">
    <div className="flex items-center space-x-4">
      <div className="p-3 rounded-xl bg-cyber-blue/10 text-cyber-blue shadow-lg shadow-cyber-blue/5 border border-cyber-blue/20">
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 20l-5.447-2.724A2 2 0 013 15.382V6.618a2 2 0 011.09-1.789L9 2m0 18l6-3m-6 3V7m6 10l4.553 2.276A2 2 0 0021 17.382V8.618a2 2 0 00-1.09-1.789L15 4m0 13V4m0 0L9 7" />
        </svg>
      </div>
      <div>
        <h1 className="text-2xl font-black italic tracking-tighter text-white uppercase italic">
          BOTNET <span className="text-cyber-cyan">TOPOLOGY</span> LAB
        </h1>
        <p className="text-[10px] font-bold text-slate-500 tracking-[0.3em] uppercase">
          Structural Behavioral Analysis Engine
        </p>
      </div>
    </div>

    {activeBotnet && (
      <div className="flex items-center space-x-4 animate-in fade-in slide-in-from-right duration-700">
        <div className="text-right">
          <p className="text-[10px] font-black text-red-500 uppercase tracking-widest">Active Incident</p>
          <p className="text-sm font-black italic text-white uppercase">{activeBotnet}</p>
        </div>
        <div className="w-12 h-12 rounded-full border-4 border-red-500 border-t-transparent animate-spin flex items-center justify-center">
          <div className="w-2 h-2 rounded-full bg-red-500 animate-pulse" />
        </div>
      </div>
    )}
  </div>
);

export default BotnetTopologyPage;
