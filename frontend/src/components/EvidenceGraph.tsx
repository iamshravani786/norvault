import React, { useMemo } from 'react';
import { ProofPassport } from '../types';
import { ReactFlow, Controls, Background, MiniMap, Node, Edge, MarkerType } from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import dagre from 'dagre';

const nodeWidth = 220;
const nodeHeight = 80;

const getLayoutedElements = (nodes: Node[], edges: Edge[], direction = 'TB') => {
  const dagreGraph = new dagre.graphlib.Graph();
  dagreGraph.setDefaultEdgeLabel(() => ({}));
  dagreGraph.setGraph({ rankdir: direction });

  nodes.forEach((node) => {
    dagreGraph.setNode(node.id, { width: nodeWidth, height: nodeHeight });
  });

  edges.forEach((edge) => {
    dagreGraph.setEdge(edge.source, edge.target);
  });

  dagre.layout(dagreGraph);

  nodes.forEach((node) => {
    const nodeWithPosition = dagreGraph.node(node.id);
    node.targetPosition = direction === 'TB' ? 'top' : 'left' as any;
    node.sourcePosition = direction === 'TB' ? 'bottom' : 'right' as any;
    // Shift dagre node position (anchor=center) to React Flow (anchor=top-left)
    node.position = {
      x: nodeWithPosition.x - nodeWidth / 2,
      y: nodeWithPosition.y - nodeHeight / 2,
    };
    return node;
  });

  return { nodes, edges };
};

export function EvidenceGraph({ passport }: { passport: ProofPassport }) {
  const { initialNodes, initialEdges } = useMemo(() => {
    const rawNodes = passport.evidence_graph?.nodes || [];
    const rawEdges = passport.evidence_graph?.edges || [];

    const nodes: Node[] = rawNodes.map(n => {
      let bgColor = '#16161d';
      let borderColor = '#5a5a72';
      if (n.node_type === 'Company') borderColor = '#3b82f6';
      if (n.node_type === 'Fact') borderColor = '#22c55e';
      if (n.node_type === 'Source') borderColor = '#a855f7';
      if (n.node_type === 'Person') borderColor = '#f97316';

      return {
        id: n.id,
        position: { x: 0, y: 0 },
        data: { label: n.label || n.id },
        style: {
          background: bgColor,
          color: '#fff',
          border: `2px solid ${borderColor}`,
          borderRadius: '8px',
          padding: '10px',
          fontSize: '12px',
          width: nodeWidth,
          fontFamily: 'monospace',
          textAlign: 'center'
        }
      };
    });

    const edges: Edge[] = rawEdges.map((e, i) => ({
      id: `e-${i}-${e.source}-${e.target}`,
      source: e.source,
      target: e.target,
      label: e.label,
      labelStyle: { fill: '#b0b0c4', fontSize: 10, fontFamily: 'monospace' },
      labelBgStyle: { fill: '#0a0a0c', fillOpacity: 0.8 },
      style: { stroke: '#5a5a72', strokeWidth: 1.5 },
      markerEnd: { type: MarkerType.ArrowClosed, color: '#5a5a72' }
    }));

    return { initialNodes: nodes, initialEdges: edges };
  }, [passport.evidence_graph]);

  const { nodes: layoutedNodes, edges: layoutedEdges } = getLayoutedElements(initialNodes, initialEdges);

  if (!layoutedNodes.length) {
    return <div className="flex items-center justify-center h-[600px] text-[var(--color-graphite-400)] italic">No graph data available.</div>;
  }

  return (
    <div className="w-full h-[700px] bg-[var(--color-graphite-950)] border border-[var(--color-graphite-700)] rounded-xl overflow-hidden relative">
      <ReactFlow
        nodes={layoutedNodes}
        edges={layoutedEdges}
        fitView
        minZoom={0.2}
        maxZoom={2}
        attributionPosition="bottom-right"
      >
        <Background color="#2a2a38" gap={16} />
        <Controls className="bg-[var(--color-graphite-800)] fill-white border-[var(--color-graphite-600)]" />
      </ReactFlow>
    </div>
  );
}
