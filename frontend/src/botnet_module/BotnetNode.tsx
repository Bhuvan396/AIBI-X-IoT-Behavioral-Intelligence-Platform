import { memo } from 'react';
import { Handle, Position } from 'reactflow';
import { Cpu, ShieldAlert, Monitor, Wifi, Thermometer, Printer } from 'lucide-react';

const NodeIcon = ({ type }: { type: string }) => {
  switch (type.toLowerCase()) {
    case 'camera': return <Wifi className="w-5 h-5" />;
    case 'sensor': return <Monitor className="w-5 h-5" />;
    case 'thermostat': return <Thermometer className="w-5 h-5" />;
    case 'printer': return <Printer className="w-5 h-5" />;
    case 'gateway': return <Cpu className="w-5 h-5 text-cyber-blue" />;
    case 'botnet': return <ShieldAlert className="w-6 h-6 text-cyber-danger" />;
    default: return <Cpu className="w-5 h-5" />;
  }
};

export const BotnetNode = memo(({ data }: any) => {
  const isBotnet = data.type === 'botnet';

  return (
    <div className={`px-4 py-3 shadow-xl rounded-xl border-2 bg-slate-900 flex flex-col items-center justify-center min-w-[120px] transition-all duration-500 ${
      isBotnet 
        ? 'border-cyber-danger shadow-cyber-danger/30 animate-pulse' 
        : 'border-white/10 hover:border-white/30'
    }`}>
      <Handle type="target" position={Position.Left} className="w-2 h-2 !bg-cyber-blue" />
      
      <div className={`p-2 rounded-lg mb-2 ${isBotnet ? 'bg-cyber-danger/20' : 'bg-white/5'}`}>
        <NodeIcon type={data.type} />
      </div>
      
      <div className="text-center">
        <div className="text-[10px] uppercase tracking-wider font-bold text-slate-500">{data.type}</div>
        <div className={`text-xs font-bold leading-tight ${isBotnet ? 'text-cyber-danger' : 'text-white'}`}>
          {data.label}
        </div>
        <div className="text-[8px] text-slate-600 mt-1 font-mono">{data.ip}</div>
      </div>

      <Handle type="source" position={Position.Right} className="w-2 h-2 !bg-cyber-blue" />
    </div>
  );
});
