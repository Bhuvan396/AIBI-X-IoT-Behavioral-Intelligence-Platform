import React from 'react';
import ReactFlow, { 
  Background, 
  Controls, 
  MiniMap,
  useNodesState,
  useEdgesState,
} from 'reactflow';
import type { Node, Edge } from 'reactflow';
import 'reactflow/dist/style.css';
import { BotnetNode } from './BotnetNode';

const nodeTypes = {
  camera: BotnetNode,
  sensor: BotnetNode,
  thermostat: BotnetNode,
  printer: BotnetNode,
  gateway: BotnetNode,
  cloud: BotnetNode,
  botnet: BotnetNode,
};

interface NetworkGraphProps {
  nodes: Node[];
  edges: Edge[];
}

export const NetworkGraph: React.FC<NetworkGraphProps> = ({ nodes: initialNodes, edges: initialEdges }) => {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);

  React.useEffect(() => {
    setNodes(initialNodes);
    setEdges(initialEdges);
  }, [initialNodes, initialEdges, setNodes, setEdges]);

  return (
    <div className="w-full h-full bg-slate-950/50 rounded-2xl overflow-hidden border border-white/5 relative">
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        nodeTypes={nodeTypes}
        fitView
        className="botnet-flow"
      >
        <Background color="#1e293b" gap={20} />
        <Controls className="!bg-slate-900 !border-white/10" />
        <MiniMap 
          className="!bg-slate-900 !border-white/10"
          maskColor="rgba(0,0,0,0.5)"
          nodeColor={(n) => {
            if (n.type === 'botnet') return '#ff3e3e';
            if (n.type === 'gateway') return '#00d1ff';
            return '#1e293b';
          }}
        />
      </ReactFlow>
      
      {/* Legend */}
      <div className="absolute top-4 right-4 p-4 glass-panel border border-white/10 rounded-xl space-y-2 text-[10px] z-10">
        <div className="flex items-center space-x-2">
          <div className="w-3 h-3 rounded bg-cyber-blue" />
          <span className="text-slate-400">Gateway / Security Stack</span>
        </div>
        <div className="flex items-center space-x-2">
          <div className="w-3 h-3 rounded bg-cyber-danger animate-pulse" />
          <span className="text-slate-400">Botnet Node (Malicious)</span>
        </div>
        <div className="flex items-center space-x-2">
          <div className="w-3 h-3 rounded bg-slate-700" />
          <span className="text-slate-400">IoT Peripheral Device</span>
        </div>
      </div>
    </div>
  );
};
