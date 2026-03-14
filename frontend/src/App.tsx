import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import DeviceDetails from './pages/DeviceDetails';
import AttackControl from './pages/AttackControl';
import Reports from './pages/Reports';
import BotnetTopologyPage from './botnet_module/BotnetTopologyPage';
import { Activity, ShieldAlert, Cpu, FileText, Network } from 'lucide-react';

function App() {
  return (
    <BrowserRouter>
      <div className="flex h-screen overflow-hidden bg-cyber-dark text-slate-300">
        {/* Sidebar */}
        <aside className="w-64 flex-shrink-0 glass-panel border-l-0 border-y-0 border-r border-white/10 flex flex-col">
          <div className="p-6 border-b border-white/5 flex items-center justify-center space-x-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-cyber-blue to-cyber-cyan flex items-center justify-center shadow-lg shadow-cyber-blue/30">
              <ShieldAlert className="w-6 h-6 text-white" />
            </div>
            <h1 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-slate-400">
              AIBI<span className="text-cyber-cyan">-X</span>
            </h1>
          </div>
          <nav className="flex-1 p-4 space-y-2">
            <Link to="/" className="flex items-center space-x-3 px-4 py-3 rounded-lg hover:bg-white/5 transition-colors text-slate-400 hover:text-white group">
              <Activity className="w-5 h-5 group-hover:text-cyber-cyan transition-colors" />
              <span className="font-medium">Dashboard</span>
            </Link>
            <Link to="/devices" className="flex items-center space-x-3 px-4 py-3 rounded-lg hover:bg-white/5 transition-colors text-slate-400 hover:text-white group">
              <Cpu className="w-5 h-5 group-hover:text-cyber-blue transition-colors" />
              <span className="font-medium">Devices</span>
            </Link>
            <Link to="/attacks" className="flex items-center space-x-3 px-4 py-3 rounded-lg hover:bg-white/5 transition-colors text-slate-400 hover:text-white group">
              <ShieldAlert className="w-5 h-5 group-hover:text-cyber-danger transition-colors" />
              <span className="font-medium">Attack Control</span>
            </Link>
            <Link to="/reports" className="flex items-center space-x-3 px-4 py-3 rounded-lg hover:bg-white/5 transition-colors text-slate-400 hover:text-white group">
              <FileText className="w-5 h-5 group-hover:text-cyber-accent transition-colors" />
              <span className="font-medium">Reports</span>
            </Link>
            <Link to="/botnet-lab" className="flex items-center space-x-3 px-4 py-3 rounded-lg hover:bg-white/5 transition-colors text-slate-400 hover:text-white group border-t border-white/5 pt-4 mt-2">
              <Network className="w-5 h-5 group-hover:text-cyber-cyan transition-colors" />
              <span className="font-medium">Botnet Topology Lab</span>
            </Link>
          </nav>
          <div className="p-4 border-t border-white/5 text-xs text-center text-slate-600">
            AIBI-X Platform v1.0
          </div>
        </aside>

        {/* Main Content */}
        <main className="flex-1 overflow-y-auto relative bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-slate-900 via-cyber-dark to-black">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/devices" element={<DeviceDetails />} />
            <Route path="/attacks/:id?" element={<AttackControl />} />
            <Route path="/reports" element={<Reports />} />
            <Route path="/botnet-lab" element={<BotnetTopologyPage />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;
