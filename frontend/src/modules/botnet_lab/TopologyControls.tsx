import React from 'react';
import { ShieldAlert, Play, RotateCcw, Ban, Unlock } from 'lucide-react';

interface TopologyControlsProps {
  onAnalyze: () => void;
  onReset: () => void;
  onToggleIntake: () => void;
  isIntakeBlocked: boolean;
  isAnalyzing: boolean;
}

const TopologyControls: React.FC<TopologyControlsProps> = ({
  onAnalyze,
  onReset,
  onToggleIntake,
  isIntakeBlocked,
  isAnalyzing,
}) => {
  return (
    <div className="absolute top-6 left-6 z-10 flex flex-col space-y-3">
      {/* Run Analysis Button */}
      <button
        onClick={onAnalyze}
        disabled={isAnalyzing}
        className={`flex items-center space-x-3 px-6 py-4 rounded-xl font-bold transition-all duration-300 shadow-2xl ${
          isAnalyzing
            ? 'bg-slate-800 text-slate-500 cursor-not-allowed border border-white/5'
            : 'bg-white text-black hover:bg-cyber-cyan hover:scale-105 active:scale-95'
        }`}
      >
        <Play className={`w-5 h-5 ${isAnalyzing ? '' : 'fill-current'}`} />
        <span>{isAnalyzing ? 'RUNNING ANALYSIS...' : 'RUN FORENSIC ANALYSIS'}</span>
      </button>

      <div className="flex space-x-3">
        {/* Block Intake Toggle */}
        <button
          onClick={onToggleIntake}
          className={`flex items-center space-x-2 px-4 py-2.5 rounded-lg text-xs font-bold border transition-all duration-300 ${
            isIntakeBlocked
              ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400 hover:bg-emerald-500/20'
              : 'bg-red-500/10 border-red-500/30 text-red-400 hover:bg-red-500/20'
          }`}
        >
          {isIntakeBlocked ? <Unlock className="w-4 h-4" /> : <Ban className="w-4 h-4" />}
          <span>{isIntakeBlocked ? 'UNBLOCK INTAKE' : 'BLOCK INTAKE'}</span>
        </button>

        {/* Reset Button */}
        <button
          onClick={onReset}
          className="flex items-center space-x-2 px-4 py-2.5 rounded-lg text-xs font-bold bg-slate-800 border border-white/5 text-slate-400 hover:bg-slate-700 hover:text-white transition-all duration-300"
        >
          <RotateCcw className="w-4 h-4" />
          <span>RESET TO BASELINE</span>
        </button>
      </div>

      {/* Intake Status Badge */}
      {isIntakeBlocked && (
        <div className="flex items-center space-x-2 px-3 py-1.5 rounded-full bg-red-500 text-white text-[10px] font-black uppercase tracking-widest animate-pulse w-fit">
          <ShieldAlert className="w-3 h-3" />
          <span>Intake Blocked</span>
        </div>
      )}
    </div>
  );
};

export default TopologyControls;
