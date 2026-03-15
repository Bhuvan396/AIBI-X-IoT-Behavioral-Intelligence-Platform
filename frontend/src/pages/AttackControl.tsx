import React, { useState } from 'react';
import AttackSelector from '../components/AttackSelector';
import { ShieldAlert } from 'lucide-react';

const AttackControl: React.FC = () => {
  const [deviceId, setDeviceId] = useState('');

  return (
    <div className="p-8">
      <h1 className="flex items-center text-3xl font-extrabold bg-clip-text text-transparent bg-gradient-to-r from-red-500 to-rose-400 mb-8">
        <ShieldAlert className="w-8 h-8 text-red-500 mr-4" />
        Attack Control Center
      </h1>
      <div className="max-w-xl mx-auto space-y-8">
        <div className="glass-panel p-6 border-l-4 border-l-cyber-danger">
          <label className="block text-sm font-bold text-slate-300 uppercase tracking-widest mb-2">Target Device ID</label>
          <input 
            type="text" 
            value={deviceId}
            onChange={(e) => setDeviceId(e.target.value)}
            className="w-full bg-black/50 border border-white/10 rounded-lg p-3 text-white focus:outline-none focus:border-cyber-danger focus:ring-1 focus:ring-cyber-danger transition-all focus:bg-cyber-danger/5"
            placeholder="e.g., camera_01"
          />
        </div>
        
        {deviceId && <AttackSelector deviceId={deviceId} />}
      </div>
    </div>
  );
};

export default AttackControl;
