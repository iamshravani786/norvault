from __future__ import annotations
import networkx as nx
from typing import Any

class EvidenceGraphEngine:
    def __init__(self) -> None:
        self.graph = nx.DiGraph()
    
    def add_company(self, org_number: str, name: str, **data: Any) -> str:
        """Add a company node. Returns node_id."""
        node_id = f"company:{org_number}"
        self.graph.add_node(node_id, type="company", org_number=org_number, name=name, **data)
        return node_id
    
    def add_fact(self, fact_id: str, fact_type: str, value: str, **data: Any) -> str:
        """Add a fact node and link to company."""
        node_id = f"fact:{fact_id}"
        self.graph.add_node(node_id, type="fact", fact_type=fact_type, value=value, **data)
        return node_id
    
    def add_source(self, source_id: str, name: str, authority_level: int, **data: Any) -> str:
        """Add a source node."""
        node_id = f"source:{source_id}"
        self.graph.add_node(node_id, type="source", name=name, authority_level=authority_level, **data)
        return node_id
    
    def add_document(self, doc_id: str, url: str, content_hash: str | None = None, **data: Any) -> str:
        """Add a document node."""
        node_id = f"document:{doc_id}"
        self.graph.add_node(node_id, type="document", url=url, content_hash=content_hash, **data)
        return node_id
    
    def add_person(self, person_id: str, name: str, role: str | None = None, **data: Any) -> str:
        """Add a person node."""
        node_id = f"person:{person_id}"
        self.graph.add_node(node_id, type="person", name=name, role=role, **data)
        return node_id
    
    def link(self, from_id: str, to_id: str, edge_type: str, **data: Any) -> None:
        """Create an edge between two nodes."""
        self.graph.add_edge(from_id, to_id, type=edge_type, **data)
    
    def get_evidence_chain(self, fact_id: str) -> list[dict[str, Any]]:
        """Trace the full evidence chain for a fact: fact → evidence → document → source."""
        node_id = f"fact:{fact_id}"
        if node_id not in self.graph:
            return []
            
        chain = []
        visited = set()
        queue = [node_id]
        while queue:
            curr = queue.pop(0)
            if curr not in visited:
                visited.add(curr)
                node_data = self.graph.nodes[curr].copy()
                node_data['id'] = curr
                chain.append(node_data)
                for successor in self.graph.successors(curr):
                    queue.append(successor)
        return chain
    
    def get_company_subgraph(self, company_node_id: str) -> EvidenceGraphEngine:
        """Extract the subgraph for a specific company."""
        if company_node_id not in self.graph:
            return EvidenceGraphEngine()
            
        nodes = set([company_node_id])
        queue = [company_node_id]
        
        while queue:
            curr = queue.pop(0)
            for neighbor in self.graph.successors(curr):
                if neighbor not in nodes:
                    nodes.add(neighbor)
                    queue.append(neighbor)
            for neighbor in self.graph.predecessors(curr):
                if neighbor not in nodes:
                    nodes.add(neighbor)
                    queue.append(neighbor)
                    
        subgraph = self.graph.subgraph(nodes).copy()
        new_engine = EvidenceGraphEngine()
        new_engine.graph = subgraph
        return new_engine
    
    def to_serializable(self) -> dict[str, Any]:
        """Export graph as {nodes: [...], edges: [...]} for the frontend."""
        nodes = []
        for n in self.graph.nodes:
            data = dict(self.graph.nodes[n])
            node_type = data.pop('type', 'unknown')
            label = data.pop('name', data.get('value', str(n)))
            nodes.append({"id": n, "node_type": node_type, "label": str(label), "data": data})
            
        edges = []
        for u, v in self.graph.edges:
            data = dict(self.graph.edges[u, v])
            edge_type = data.pop('type', 'UNKNOWN')
            label = data.pop('label', '')
            edges.append({"source": u, "target": v, "edge_type": edge_type, "label": str(label)})
            
        return {"nodes": nodes, "edges": edges}
    
    def detect_contradictions(self) -> list[tuple[str, str]]:
        """Find nodes connected by CONTRADICTS edges."""
        contradictions = []
        for u, v, data in self.graph.edges(data=True):
            if data.get('type') == 'CONTRADICTS':
                contradictions.append((u, v))
        return contradictions
    
    def clear(self) -> None:
        """Reset the graph."""
        self.graph.clear()
