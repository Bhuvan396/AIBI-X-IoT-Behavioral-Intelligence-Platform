import { 
  X, AlertTriangle, ShieldCheck, Activity, 
  Target, Server, TrendingDown, ChevronRight 
} from 'lucide-react';

interface AnalysisPopupProps {
  data: any;
  onClose: () => void;
}

const AnalysisPopup: React.FC<AnalysisPopupProps> = ({ data, onClose }) => {
  const { analysis, alert } = data;
  
  return (
    <div className="fixed inset-0 z-[100] flex items-center justify-center p-6 bg-cyber-dark/95 backdrop-blur-md">
      <div className="w-full max-w-4xl max-h-[90vh] bg-slate-900 border border-white/10 rounded-3xl shadow-[0_0_100px_rgba(0,0,0,0.8)] overflow-hidden flex flex-col">
        
        {/* Header */}
        <div className={`p-8 border-b flex items-center justify-between ${
          alert ? 'bg-red-500/10 border-red-500/20' : 'bg-emerald-500/10 border-emerald-500/20'
        }`}>
          <div className="flex items-center space-x-4">
            <div className={`p-4 rounded-2xl shadow-lg ${
              alert ? 'bg-red-500 text-white' : 'bg-emerald-500 text-white'
            }`}>
              {alert ? <AlertTriangle className="w-10 h-10" /> : <ShieldCheck className="w-10 h-10" />}
            </div>
            <div>
              <h2 className="text-3xl font-black tracking-tight text-white uppercase italic">
                {alert ? 'Attack Analysis' : 'Safety Report'}
              </h2>
              <div className="flex items-center space-x-3 mt-1">
                <span className={`px-3 py-1 rounded-full text-[10px] font-black uppercase tracking-widest ${
                  alert ? 'bg-red-500/20 text-red-400' : 'bg-emerald-500/20 text-emerald-400'
                }`}>
                  {analysis.type}
                </span>
                <span className="text-slate-500 font-bold">•</span>
                <span className="text-xs font-bold text-slate-400">Confidence: <span className="text-white font-mono">{analysis.confidence}</span></span>
              </div>
            </div>
          </div>
          <button onClick={onClose} className="p-3 hover:bg-white/5 rounded-full transition-colors text-slate-500">
            <X className="w-6 h-6" />
          </button>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto p-10 grid grid-cols-5 gap-10">
          {/* Left Column: Forensic Metrics */}
          <div className="col-span-2 space-y-8">
            <div>
              <h3 className="text-xs font-black text-slate-500 uppercase tracking-[0.2em] mb-6 flex items-center">
                <Activity className="w-4 h-4 mr-2 text-cyber-cyan" />
                Forensic Indicators
              </h3>
              <div className="space-y-4">
                {analysis.irregularities.map((item: string, i: number) => (
                  <div key={i} className="flex space-x-3 p-4 rounded-xl bg-red-500/5 border border-red-500/10 text-xs font-semibold text-red-300 leading-relaxed italic">
                    <TrendingDown className="w-4 h-4 flex-shrink-0" />
                    <span>{item}</span>
                  </div>
                ))}
                {analysis.irregularities.length === 0 && (
                  <div className="flex items-center space-x-3 p-4 rounded-xl bg-emerald-500/5 border border-emerald-500/10 text-xs font-semibold text-emerald-400 italic">
                    <ShieldCheck className="w-4 h-4" />
                    <span>Behavioral metrics correlate with captured baseline.</span>
                  </div>
                )}
              </div>
            </div>

            <div>
              <h3 className="text-[10px] font-black text-slate-600 uppercase tracking-widest mb-4 italic underline decoration-cyber-cyan/30 underline-offset-4">Affected Assets</h3>
              <div className="grid grid-cols-2 gap-2">
                {analysis.affected_devices.map((id: string) => (
                  <div key={id} className="px-3 py-2 rounded-lg bg-black/20 border border-white/5 text-[10px] font-mono text-slate-400">
                    {id}
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Right Column: AI Rationale & Explanation */}
          <div className="col-span-3 space-y-8 bg-white/5 p-8 rounded-3xl border border-white/5 backdrop-blur-sm self-start">
            <div>
              <h3 className="text-xs font-black text-slate-400 uppercase tracking-[0.2em] mb-6 flex items-center">
                <Target className="w-4 h-4 mr-2 text-red-500" />
                AI Analysis & Rationale
              </h3>
              <div className="space-y-6">
                <div className="p-5 rounded-2xl bg-black/30 border-l-4 border-red-500">
                  <p className="text-sm font-bold text-white mb-2 italic">Class Summary</p>
                  <p className="text-xs text-slate-400 leading-relaxed font-semibold italic opacity-80">{analysis.description}</p>
                </div>
                
                <div className="space-y-3">
                  <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest pl-2">Rationale (Explainable AI)</p>
                  {analysis.rationale.map((line: string, i: number) => (
                    <div key={i} className="flex items-start space-x-3 p-3 rounded-xl hover:bg-white/5 transition-colors">
                      <ChevronRight className="w-4 h-4 text-cyber-cyan mt-0.5" />
                      <p className="text-xs text-slate-300 font-medium italic">{line}</p>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            <div className="pt-6 border-t border-white/10">
              <h3 className="text-[10px] font-black text-slate-600 uppercase tracking-widest mb-4 italic">Security Impact</h3>
              <div className="flex items-start space-x-3">
                <div className="p-2 rounded-lg bg-red-500/20 text-red-500">
                  <Server className="w-4 h-4" />
                </div>
                <p className="text-[11px] font-bold text-red-400 leading-relaxed italic opacity-90">{analysis.impact}</p>
              </div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="p-8 border-t border-white/5 bg-black/30 flex justify-end">
          <button 
            onClick={onClose}
            className="px-10 py-3 rounded-xl bg-white text-black font-black uppercase text-xs tracking-widest hover:bg-cyber-cyan hover:scale-105 active:scale-95 transition-all shadow-xl shadow-cyan-500/10"
          >
            DISMISS REPORT
          </button>
        </div>
      </div>
    </div>
  );
};

export default AnalysisPopup;
