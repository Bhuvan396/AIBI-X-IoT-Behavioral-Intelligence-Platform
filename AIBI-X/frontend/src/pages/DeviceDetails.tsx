import React, { useState, useEffect } from 'react';
import { getDevices, getDeviceStatus } from '../services/api';
import type { Device } from '../services/api';
import { Cpu, Globe, BadgeCheck } from 'lucide-react';

const DeviceDetails: React.FC = () => {
  const [devices, setDevices] = useState<Device[]>([]);
  const [statuses, setStatuses] = useState<Record<string, any>>({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const list = await getDevices();
        setDevices(list);
        const statusMap: Record<string, any> = {};
        for (const d of list) {
          const s = await getDeviceStatus(d.device_id);
          statusMap[d.device_id] = s;
        }
        setStatuses(statusMap);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  return (
    <div className="p-8 pb-32">
      <header className="mb-8">
        <h1 className="text-3xl font-extrabold text-white mb-2">Device Registry</h1>
        <p className="text-slate-500">Inventory and real-time health status of all connected IoT infrastructure.</p>
      </header>

      {loading ? (
        <div className="flex flex-col items-center justify-center p-20 opacity-30">
          <Cpu className="w-12 h-12 animate-spin mb-4" />
          <p>Scanning Network...</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
          {devices.map((device) => {
            const status = statuses[device.device_id];
            const isUnhealthy = status && status.trust_score < 70;

            return (
              <div key={device.device_id} className={`glass-panel p-6 border-t-4 ${isUnhealthy ? 'border-cyber-danger' : 'border-cyber-blue'}`}>
                <div className="flex justify-between items-start mb-6">
                  <div className="p-3 bg-white/5 rounded-xl text-cyber-blue">
                    <Cpu className="w-6 h-6" />
                  </div>
                  <div className={`px-3 py-1 rounded-full text-[10px] font-bold uppercase tracking-widest ${isUnhealthy ? 'bg-cyber-danger/10 text-cyber-danger' : 'bg-emerald-500/10 text-emerald-500'}`}>
                    {isUnhealthy ? 'Risk Detected' : 'Healthy'}
                  </div>
                </div>

                <div className="space-y-4">
                  <div>
                    <h3 className="text-xl font-bold text-white">{device.device_id}</h3>
                    <p className="text-xs text-slate-500 uppercase font-mono">{device.device_type}</p>
                  </div>

                  <div className="grid grid-cols-2 gap-4 pt-4 border-t border-white/5 text-sm">
                    <div className="flex items-center space-x-2 text-slate-400">
                      <Globe className="w-4 h-4" />
                      <span>{device.ip_address}</span>
                    </div>
                    <div className="flex items-center space-x-2 text-slate-400">
                      <BadgeCheck className="w-4 h-4" />
                      <span>{(status?.trust_score ?? 100).toFixed(1)}% Link</span>
                    </div>
                  </div>

                  <div className="pt-2">
                    <div className="flex justify-between text-xs mb-1">
                      <span className="text-slate-500">Security Score</span>
                      <span className={isUnhealthy ? 'text-cyber-danger' : 'text-emerald-500'}>
                        {(status?.trust_score ?? 100).toFixed(0)}/100
                      </span>
                    </div>
                    <div className="w-full bg-white/5 h-1 rounded-full overflow-hidden">
                      <div 
                        className={`h-full transition-all duration-1000 ${isUnhealthy ? 'bg-cyber-danger' : 'bg-cyber-blue'}`}
                        style={{ width: `${status?.trust_score || 0}%` }}
                      />
                    </div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};

export default DeviceDetails;
