import React from 'react';
import { ShieldAlert, Zap, Network, Play } from 'lucide-react';

interface BotnetSidebarProps {
  onInject: (type: string) => void;
  isLoading: boolean;
}

const BOTNET_TYPES = [
  {
    id: 'centralized',
    name: 'Centralized Botnet',
    description: 'All infected IoT devices communicate with a single central Command & Control (C2) server.',
    icon: <Cpu className="w-5 h-5" />
  },
  {
    id: 'p2p',
    name: 'Peer-to-Peer Botnet',
    description: 'Decentralized structure where infected devices act as both clients and servers to propagate commands.',
    icon: <Network className="w-5 h-5" />
  },
  {
    id: 'mirai',
    name: 'Mirai-Style IoT Botnet',
    description: 'Massive-scale botnet that scans for vulnerable IoT devices to launch large-scale DDoS attacks.',
    icon: <Zap className="w-5 h-5" />
  }
];

import { Cpu } from 'lucide-react';

export const BotnetSidebar: React.FC<BotnetSidebarProps> = ({ onInject, isLoading }) => {
  const [selected, setSelected] = React.useState<string | null>(null);

  return (
    <div className="w-80 h-full flex flex-col glass-panel border-r border-white/10 p-6 space-y-6">
      <div className="flex items-center space-x-3 mb-2">
        <ShieldAlert className="w-6 h-6 text-cyber-danger" />
        <h2 className="text-xl font-bold text-white">Botnet Simulator</h2>
      </div>

      <div className="space-y-4 flex-1 overflow-y-auto pr-2">
        {BOTNET_TYPES.map((type) => (
          <button
            key={type.id}
            onClick={() => setSelected(type.name)}
            className={`w-full text-left p-4 rounded-xl border transition-all duration-300 ${
              selected === type.name
                ? 'bg-cyber-danger/10 border-cyber-danger shadow-lg shadow-cyber-danger/20'
                : 'bg-white/5 border-white/5 hover:border-white/20 hover:bg-white/10'
            }`}
          >
            <div className={`flex items-center space-x-3 mb-2 ${selected === type.name ? 'text-cyber-danger' : 'text-slate-400'}`}>
              {type.icon}
              <span className="font-bold">{type.name}</span>
            </div>
            <p className="text-xs text-slate-500 leading-relaxed">
              {type.description}
            </p>
          </button>
        ))}
      </div>

      <button
        onClick={() => selected && onInject(selected)}
        disabled={!selected || isLoading}
        className={`w-full py-4 rounded-xl font-bold flex items-center justify-center space-x-3 transition-all duration-300 ${
          !selected || isLoading
            ? 'bg-slate-800 text-slate-500 cursor-not-allowed'
            : 'bg-gradient-to-r from-red-600 to-cyber-danger text-white shadow-lg shadow-cyber-danger/30 hover:scale-[1.02] active:scale-95'
        }`}
      >
        {isLoading ? (
          <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
        ) : (
          <>
            <Play className="w-5 h-5 fill-current" />
            <span>Inject Botnet Node</span>
          </>
        )}
      </button>
    </div>
  );
};
