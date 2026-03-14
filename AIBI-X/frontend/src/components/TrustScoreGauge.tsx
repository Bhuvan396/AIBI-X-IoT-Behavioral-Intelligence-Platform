import React from 'react';

interface GaugeProps {
  score: number;
}

const TrustScoreGauge: React.FC<GaugeProps> = ({ score }) => {
  const percentage = Math.max(0, Math.min(100, score));
  let colorClass = 'text-emerald-500';
  let strokeColor = '#10b981';
  let blurClass = 'bg-emerald-500/20';

  if (percentage < 50) {
    colorClass = 'text-cyber-danger';
    strokeColor = '#ef4444';
    blurClass = 'bg-cyber-danger/20';
  } else if (percentage < 80) {
    colorClass = 'text-amber-500';
    strokeColor = '#f59e0b';
    blurClass = 'bg-amber-500/20';
  }

  const radius = 60;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (percentage / 100) * circumference;

  return (
    <div className="glass-panel p-6 flex flex-col items-center justify-center relative overflow-hidden h-[300px]">
      <div className={`absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-48 h-48 rounded-full blur-[64px] ${blurClass} pointer-events-none`} />
      
      <h2 className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-slate-400 self-start w-full">
        Trust Score
      </h2>
      
      <div className="relative mt-8 group">
        <svg fill="transparent" width="160" height="160" viewBox="0 0 160 160" className="transform -rotate-90">
          <circle cx="80" cy="80" r={radius} stroke="#ffffff10" strokeWidth="12" />
          <circle 
            cx="80" 
            cy="80" 
            r={radius} 
            stroke={strokeColor} 
            strokeWidth="12" 
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            className="transition-all duration-1000 ease-out drop-shadow-lg"
          />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className={`text-4xl font-extrabold ${colorClass} drop-shadow-md`}>
            {percentage}
          </span>
          <span className="text-xs font-medium text-slate-400 uppercase tracking-widest mt-1">/100</span>
        </div>
      </div>
    </div>
  );
};

export default TrustScoreGauge;
