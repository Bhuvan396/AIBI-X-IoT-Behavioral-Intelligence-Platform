import React from 'react';
import { ShieldAlert, Zap, Globe, Target } from 'lucide-react';

interface BotnetSidebarProps {
  onInject: (type: string) => void;
  activeBotnet: string | null;
}

const botnetTypes = [
  {
    id: "Centralized Botnet",
    name: "Centralized Botnet",
    icon: Target,
    color: "from-blue-500 to-blue-700",
    description: "Classic hub-and-spoke model. All bots report to a single C2 server for instructions.",
    indicators: ["High node degree", "Periodic beaconing", "Known C2 IPs"]
  },
  {
    id: "Peer-to-Peer Botnet",
    name: "P2P Botnet (Storm/Gameover)",
    icon: Globe,
    color: "from-purple-500 to-purple-700",
    description: "Decentralized mesh network. Commands propagate through the network without a single point of failure.",
    indicators: ["Distributed mesh graph", "High flow entropy", "Multi-point coordination"]
  },
  {
    id: "Mirai-Style IoT Botnet",
    name: "Mirai IoT Swarm",
    icon: Zap,
    color: "from-red-500 to-orange-700",
    description: "Specialized in bandwidth exhaustion. Uses Telnet/SSH scanning to compromise IoT devices.",
    indicators: ["Explosive traffic volume", "High fan-out ratio", "Targeting port 23/2323"]
  }
];

const BotnetSidebar: React.FC<BotnetSidebarProps> = ({ onInject, activeBotnet }) => {
  return (
    <aside className="w-80 flex-shrink-0 bg-slate-900 border-l border-white/5 flex flex-col p-6 overflow-y-auto">
      <div className="flex items-center space-x-3 mb-8">
        <div className="p-2 rounded-lg bg-red-500/20 text-red-500 shadow-lg shadow-red-500/10">
          <ShieldAlert className="w-6 h-6" />
        </div>
        <div>
          <h2 className="text-xl font-bold text-white tracking-tight">Simulator</h2>
          <p className="text-[10px] text-slate-500 uppercase tracking-widest font-bold">Botnet Lab v1.2</p>
        </div>
      </div>

      <div className="space-y-6">
        {botnetTypes.map((type) => {
          const Icon = type.icon;
          const isActive = activeBotnet === type.id;

          return (
            <div 
              key={type.id}
              className={`p-5 rounded-2xl border transition-all duration-300 relative overflow-hidden group ${
                isActive 
                  ? 'bg-slate-800 border-red-500/50 shadow-xl shadow-red-500/5 scale-[1.02]' 
                  : 'bg-white/5 border-white/5 hover:border-white/20'
              }`}
            >
              {/* Active Indicator */}
              {isActive && (
                <div className="absolute top-0 right-0 w-2 h-full bg-red-500 active-glow" />
              )}

              <div className={`w-10 h-10 rounded-xl bg-gradient-to-br ${type.color} flex items-center justify-center mb-4 shadow-lg`}>
                <Icon className="w-6 h-6 text-white" />
              </div>

              <h3 className="text-lg font-bold text-white mb-2">{type.name}</h3>
              <p className="text-xs text-slate-400 mb-4 leading-relaxed line-clamp-2">
                {type.description}
              </p>

              <div className="space-y-1.5 mb-6">
                {type.indicators.map((ind, i) => (
                  <div key={i} className="flex items-center space-x-2 text-[10px] font-bold text-slate-500 uppercase tracking-wide">
                    <div className="w-1 h-1 rounded-full bg-slate-600" />
                    <span>{ind}</span>
                  </div>
                ))}
              </div>

              <button
                onClick={() => onInject(type.id)}
                disabled={isActive}
                className={`w-full py-3 rounded-xl text-xs font-black uppercase tracking-widest transition-all duration-300 ${
                  isActive
                    ? 'bg-red-500/10 text-red-400 cursor-not-allowed border border-red-500/20'
                    : 'bg-white text-black hover:bg-cyber-cyan hover:scale-[1.03] active:scale-95 shadow-lg'
                }`}
              >
                {isActive ? 'BOTNET INJECTED' : 'INJECT BOTNET'}
              </button>
            </div>
          );
        })}
      </div>

      <div className="mt-auto pt-8 border-t border-white/5">
        <div className="p-4 rounded-xl bg-black/40 border border-white/5">
          <h4 className="text-[10px] font-black text-slate-500 uppercase tracking-widest mb-2">Network Health</h4>
          <div className="flex justify-between items-end">
            <span className={`text-2xl font-mono font-bold ${activeBotnet ? 'text-red-400' : 'text-emerald-400'}`}>
              {activeBotnet ? 'CRITICAL' : 'OPTIMAL'}
            </span>
            <span className="text-[10px] text-slate-600 mb-1">Topology Verified</span>
          </div>
        </div>
      </div>
    </aside>
  );
};

export default BotnetSidebar;
