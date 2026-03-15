import { useMemo } from 'react';
import ReactFlow, { 
  Background, 
  Controls, 
  type Edge, 
  type Node, 
  ConnectionLineType,
  MarkerType
} from 'reactflow';
import 'reactflow/dist/style.css';
import BotnetNode from './BotnetNode';

interface NetworkGraphProps {
  nodes: Node[];
  edges: Edge[];
}

const nodeTypes = {
  camera:     BotnetNode,
  sensor:     BotnetNode,
  thermostat: BotnetNode,
  printer:    BotnetNode,
  gateway:    BotnetNode,
  cloud:      BotnetNode,
  botnet:     BotnetNode,
};

const NetworkGraph: React.FC<NetworkGraphProps> = ({ nodes, edges }) => {
  const styledEdges = useMemo(() => {
    return edges.map(edge => ({
      ...edge,
      type: ConnectionLineType.SmoothStep,
      animated: edge.animated || false,
      style: { 
        stroke: edge.className?.includes('suspicious') ? '#ef4444' : '#64748b', 
        strokeWidth: 3,
        strokeDasharray: edge.animated ? '12 6' : '0',
        transition: 'all 0.5s ease'
      },
      markerEnd: {
        type: MarkerType.ArrowClosed,
        color: edge.className?.includes('suspicious') ? '#ef4444' : '#64748b',
        width: 20,
        height: 20,
      }
    }));
  }, [edges]);

  return (
    <div className="flex-1 relative bg-cyber-dark">
      <ReactFlow
        nodes={nodes}
        edges={styledEdges}
        nodeTypes={nodeTypes}
        fitView
        snapToGrid
        snapGrid={[20, 20]}
      >
        <Background color="#1e293b" gap={20} />
        <Controls />
      </ReactFlow>
    </div>
  );
};

export default NetworkGraph;
