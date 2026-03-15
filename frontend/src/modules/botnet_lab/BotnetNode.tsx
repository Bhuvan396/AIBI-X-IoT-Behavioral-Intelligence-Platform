import { memo } from 'react';
import { Handle, Position } from 'reactflow';
import { Camera, Cpu, Thermometer, HardDrive, ShieldAlert, Cloud } from 'lucide-react';

const icons: Record<string, typeof Camera> = {
  camera:     Camera,
  sensor:     Cpu,
  thermostat: Thermometer,
  printer:    HardDrive,
  gateway:    ShieldAlert,
  cloud:      Cloud,
  botnet:     ShieldAlert,
};

const BotnetNode = ({ data, type }: any) => {
  const Icon = icons[type] || Cpu;
  const isMalicious = type === 'botnet';

  return (
    <div className={`px-4 py-3 rounded-xl border-2 shadow-xl min-w-[140px] transition-all duration-300 ${
      isMalicious 
        ? 'bg-red-950/40 border-red-500 shadow-red-500/20' 
        : 'bg-slate-900 border-white/10 shadow-black/40'
    }`}>
      <div className="flex items-center space-x-3">
        <div className={`p-2 rounded-lg ${
          isMalicious ? 'bg-red-500/20 text-red-400' : 'bg-white/5 text-slate-400'
        }`}>
          <Icon className="w-5 h-5" />
        </div>
        <div>
          <div className="text-[10px] font-bold tracking-wider text-slate-500 uppercase">
            {type}
          </div>
          <div className={`text-sm font-semibold ${isMalicious ? 'text-red-400' : 'text-slate-200'}`}>
            {data.label}
          </div>
        </div>
      </div>
      
      {data.ip && (
        <div className="mt-2 text-[10px] font-mono text-slate-500 bg-black/30 px-2 py-1 rounded">
          {data.ip}
        </div>
      )}

      {/* Handles */}
      <Handle type="target" position={Position.Top} className="w-2 h-2 !bg-slate-600 border-none" />
      <Handle type="source" position={Position.Bottom} className="w-2 h-2 !bg-slate-600 border-none" />
    </div>
  );
};

export default memo(BotnetNode);
