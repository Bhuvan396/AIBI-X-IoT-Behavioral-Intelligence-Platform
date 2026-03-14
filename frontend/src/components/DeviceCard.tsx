import React from 'react';
import { Shield, ShieldAlert, Cpu } from 'lucide-react';

interface Device {
  id: string;
  type: string;
  ip: string;
  status: 'Normal' | 'Compromised' | 'Unknown';
  trust_score?: number;
}

const DeviceCard: React.FC<{ device: Device; onClick?: () => void }> = ({ device, onClick }) => {
  const isCompromised = device.status === 'Compromised';
  
  return (
    <div 
      onClick={onClick}
      className={`glass-panel p-5 cursor-pointer hover:-translate-y-1 transition-transform duration-300 group
        ${isCompromised ? 'border-cyber-danger/50 shadow-cyber-danger/20' : 'hover:border-cyber-blue/50'}
      `}
    >
      <div className="flex justify-between items-start mb-4">
        <div className={`p-3 rounded-lg flex items-center justify-center
          ${isCompromised ? 'bg-cyber-danger/10 text-cyber-danger' : 'bg-cyber-blue/10 text-cyber-blue'}
        `}>
          <Cpu className="w-6 h-6" />
        </div>
        <div className={`px-2 py-1 rounded-full text-xs font-semibold flex items-center space-x-1
          ${isCompromised ? 'bg-cyber-danger/20 text-red-400' : 'bg-emerald-500/20 text-emerald-400'}
        `}>
          {isCompromised ? <ShieldAlert className="w-3 h-3" /> : <Shield className="w-3 h-3" />}
          <span>{device.status}</span>
        </div>
      </div>
      
      <h3 className="font-bold text-lg text-white mb-1 group-hover:text-cyber-cyan transition-colors">{device.id}</h3>
      <p className="text-sm text-slate-400 font-mono mb-3">{device.ip}</p>
      
      <div className="flex items-center justify-between text-xs">
        <span className="text-slate-500 uppercase tracking-widest font-semibold text-[10px]">{device.type}</span>
        {device.trust_score !== undefined && (
          <div className="flex items-center space-x-1">
            <span className="text-slate-500">Trust:</span>
            <span className={`font-bold ${device.trust_score < 70 ? 'text-cyber-danger' : 'text-emerald-500'}`}>
              {Math.round(device.trust_score)}%
            </span>
          </div>
        )}
      </div>
    </div>
  );
};

export default DeviceCard;
