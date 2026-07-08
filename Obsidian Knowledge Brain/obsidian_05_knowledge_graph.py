"""
Obsidian AI Brain - Phase 5: Knowledge Graph Builder
Purpose: Build and visualize knowledge graph of notes
Author: RAze
Date: 2026-07-08
"""

import json
from pathlib import Path
import networkx as nx
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class KnowledgeGraphBuilder:
    """Build knowledge graph from notes."""
    
    def __init__(self):
        self.graph = nx.DiGraph()
        self.nodes_data = {}
        self.edges_data = []
    
    def load_data(self, enriched_file='data/enriched_notes.json', suggestions_file='data/link_suggestions.json'):
        """Load notes and suggestions."""
        with open(enriched_file, 'r') as f:
            self.notes = json.load(f)['notes']
        
        with open(suggestions_file, 'r') as f:
            self.suggestions = json.load(f)
        
        logger.info(f"✅ Loaded {len(self.notes)} notes")
    
    def build_graph(self):
        """Build the knowledge graph."""
        logger.info(f"\n🕸️  BUILDING KNOWLEDGE GRAPH")
        logger.info("=" * 80)
        
        # Add nodes (notes)
        for note in self.notes:
            self.graph.add_node(
                note['id'],
                title=note['title'],
                folder=note['file_metadata']['folder'],
                word_count=note['readability']['total_words'],
                tags=note['tags'],
                concepts=note['important_concepts']
            )
            
            self.nodes_data[note['id']] = {
                'title': note['title'],
                'folder': note['file_metadata']['folder'],
                'word_count': note['readability']['total_words'],
                'tag_count': len(note['tags']),
                'concept_count': len(note['important_concepts'])
            }
        
        logger.info(f"   ✅ Added {len(self.notes)} nodes")
        
        # Add edges (connections)
        for note_id, sugg_data in self.suggestions.items():
            for suggestion in sugg_data['suggestions']:
                # Find target note ID by title
                target_id = None
                for note in self.notes:
                    if note['title'] == suggestion['title']:
                        target_id = note['id']
                        break
                
                if target_id and target_id != note_id:
                    self.graph.add_edge(
                        note_id,
                        target_id,
                        weight=1.0,
                        reason=suggestion['reason']
                    )
                    
                    self.edges_data.append({
                        'source': note_id,
                        'target': target_id,
                        'reason': suggestion['reason']
                    })
        
        logger.info(f"   ✅ Added {len(self.edges_data)} edges")
    
    def calculate_metrics(self):
        """Calculate graph metrics."""
        logger.info(f"\n📊 CALCULATING METRICS")
        
        metrics = {
            'total_nodes': self.graph.number_of_nodes(),
            'total_edges': self.graph.number_of_edges(),
            'density': nx.density(self.graph),
            'connected_components': nx.number_weakly_connected_components(self.graph)
        }
        
        # Node centrality
        centrality = nx.betweenness_centrality(self.graph)
        top_central = sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:5]
        
        print(f"\n📈 Graph Metrics:")
        print(f"   Nodes: {metrics['total_nodes']}")
        print(f"   Edges: {metrics['total_edges']}")
        print(f"   Density: {metrics['density']:.3f}")
        
        print(f"\n🎯 Most Connected Notes:")
        for node_id, centrality_val in top_central:
            node_title = self.nodes_data[node_id]['title']
            print(f"   • {node_title} (centrality: {centrality_val:.3f})")
        
        return metrics, top_central
    
    def get_node_neighborhood(self, node_id, depth=2):
        """Get neighbors of a node."""
        neighbors = set()
        current_level = {node_id}
        
        for _ in range(depth):
            next_level = set()
            for node in current_level:
                next_level.update(self.graph.successors(node))
                next_level.update(self.graph.predecessors(node))
            neighbors.update(next_level)
            current_level = next_level
        
        return neighbors
    
    def export_for_visualization(self, output_path='data/graph_data.json'):
        """Export graph data for visualization."""
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Prepare nodes
        nodes = []
        for node_id, attrs in self.graph.nodes(data=True):
            nodes.append({
                'id': node_id,
                'label': attrs.get('title', node_id),
                'folder': attrs.get('folder', 'unknown'),
                'word_count': attrs.get('word_count', 0),
                'tags': attrs.get('tags', []),
                'concepts': attrs.get('concepts', [])
            })
        
        # Prepare edges
        edges = []
        for source, target, attrs in self.graph.edges(data=True):
            edges.append({
                'source': source,
                'target': target,
                'reason': attrs.get('reason', 'related')
            })
        
        data = {
            'nodes': nodes,
            'edges': edges,
            'stats': {
                'total_nodes': len(nodes),
                'total_edges': len(edges)
            }
        }
        
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        logger.info(f"✅ Exported graph data to {output_file}")
    
    def save_graph(self, output_path='data/knowledge_graph.json'):
        """Save graph structure."""
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        data = {
            'nodes': list(self.nodes_data.values()),
            'edges': self.edges_data,
            'metadata': {
                'total_nodes': self.graph.number_of_nodes(),
                'total_edges': self.graph.number_of_edges()
            }
        }
        
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        logger.info(f"✅ Saved graph to {output_file}")


def main():
    """Build knowledge graph."""
    print("\n" + "="*80)
    print("🕸️  OBSIDIAN AI BRAIN - KNOWLEDGE GRAPH")
    print("="*80)
    
    builder = KnowledgeGraphBuilder()
    
    try:
        builder.load_data()
    except FileNotFoundError as e:
        print(f"⚠️  {e}")
        print("   Run previous phases first")
        return
    
    # Build
    builder.build_graph()
    
    # Calculate metrics
    metrics, top_nodes = builder.calculate_metrics()
    
    # Export
    builder.export_for_visualization()
    builder.save_graph()
    
    print("\n✅ KNOWLEDGE GRAPH COMPLETE!")
    print("   Next: Run: python obsidian_06_insights_generator.py")
    print("="*80)


if __name__ == "__main__":
    main()
