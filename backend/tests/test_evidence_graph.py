from __future__ import annotations
import pytest
from app.core.evidence_graph import EvidenceGraph, Node, Edge

def test_add_node():
    graph = EvidenceGraph()
    graph.add_node(Node(id="1", label="Company"))
    assert len(graph.nodes) == 1

def test_add_edge():
    graph = EvidenceGraph()
    graph.add_edge(Edge(source="1", target="2", type="owns"))
    assert len(graph.edges) == 1

def test_evidence_chain():
    graph = EvidenceGraph()
    graph.add_edge(Edge(source="1", target="2", type="owns"))
    graph.add_edge(Edge(source="2", target="3", type="owns"))
    chain = graph.get_chain("1", "3")
    assert len(chain) == 2

def test_serialization():
    graph = EvidenceGraph()
    graph.add_node(Node(id="1", label="Company"))
    data = graph.to_json()
    assert "Company" in data

def test_subgraph_extraction():
    graph = EvidenceGraph()
    graph.add_node(Node(id="1", label="A"))
    graph.add_node(Node(id="2", label="B"))
    graph.add_edge(Edge(source="1", target="2", type="rel"))
    sub = graph.extract_subgraph("1")
    assert len(sub.nodes) == 2

def test_contradiction_detection():
    graph = EvidenceGraph()
    graph.add_edge(Edge(source="source1", target="fact", type="claims", value="A"))
    graph.add_edge(Edge(source="source2", target="fact", type="claims", value="B"))
    contradictions = graph.find_contradictions("fact")
    assert len(contradictions) > 0
