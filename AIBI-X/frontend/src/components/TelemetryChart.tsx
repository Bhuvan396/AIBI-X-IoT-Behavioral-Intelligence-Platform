import React from 'react';
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, Legend } from 'recharts';

interface ChartProps {
  data: any[];
  title: string;
}

const TelemetryChart: React.FC<ChartProps> = ({ data, title }) => {
  return (
    <div className="glass-panel p-6 h-[400px] flex flex-col relative overflow-hidden">
      <div className="absolute top-0 right-0 w-64 h-64 bg-cyber-blue/5 rounded-full blur-3xl -mr-32 -mt-32 pointer-events-none" />
      <div className="flex items-center justify-between mb-6 z-10">
        <h2 className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-slate-400">
          {title || "Behavioral Analysis Trend"}
        </h2>
        <div className="flex items-center space-x-2">
          <span className="w-2 h-2 rounded-full bg-cyber-cyan animate-pulse" />
          <span className="text-xs text-cyber-cyan font-mono uppercase tracking-widest">Live Sync</span>
        </div>
      </div>
      
      <div className="flex-1 min-h-0 w-full z-10">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={data} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
            <defs>
              <linearGradient id="colorTrust" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#06b6d4" stopOpacity={0.3}/>
                <stop offset="95%" stopColor="#06b6d4" stopOpacity={0}/>
              </linearGradient>
              <linearGradient id="colorDrift" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#f59e0b" stopOpacity={0.3}/>
                <stop offset="95%" stopColor="#f59e0b" stopOpacity={0}/>
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#ffffff10" vertical={false} />
            <XAxis 
              dataKey="time" 
              stroke="#ffffff40" 
              tick={{ fill: '#ffffff60', fontSize: 10 }} 
              minTickGap={30}
            />
            <YAxis stroke="#ffffff40" tick={{ fill: '#ffffff60', fontSize: 10 }} domain={[0, 100]} />
            <Tooltip 
              contentStyle={{ 
                backgroundColor: 'rgba(21, 23, 34, 0.95)', 
                borderColor: 'rgba(255, 255, 255, 0.1)',
                backdropFilter: 'blur(8px)',
                borderRadius: '8px',
                color: '#fff',
                fontSize: '12px'
              }} 
            />
            <Legend verticalAlign="top" height={36}/>
            
            <Area 
              type="monotone" 
              name="Trust Score"
              dataKey="trust" 
              stroke="#06b6d4" 
              strokeWidth={3} 
              fillOpacity={1} 
              fill="url(#colorTrust)" 
              animationDuration={1500}
            />
            
            <Area 
              type="monotone" 
              name="Drift Level"
              dataKey="drift" 
              stroke="#f59e0b" 
              strokeWidth={2} 
              fillOpacity={1} 
              fill="url(#colorDrift)" 
              strokeDasharray="5 5"
              animationDuration={1500}
            />

            <Area 
              type="monotone" 
              name="Slow Poison"
              dataKey="poison" 
              stroke="#ef4444" 
              strokeWidth={2} 
              fillOpacity={0} 
              strokeDasharray="3 3"
              animationDuration={1500}
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default TelemetryChart;
