"""
Obsidian AI Brain - Phase 4: Link Suggestion Engine
Purpose: Suggest relevant links between notes
Author: RAze
Date: 2026-07-08
"""

import json
from pathlib import Path
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LinkSuggester:
    """Suggest connections between notes."""
    
    def __init__(self, enriched_notes_file='data/enriched_notes.json'):
        self.enriched_file = Path(enriched_notes_file)
        self.notes = []
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        self.suggestions = []
        self._load_notes()
        self._load_vector_store()
    
    def _load_notes(self):
        """Load enriched notes."""
        if not self.enriched_file.exists():
            logger.error(f"File not found: {self.enriched_file}")
            return
        
        with open(self.enriched_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Always extract as a list
        if isinstance(data, list):
            self.notes = data
        elif isinstance(data, dict) and 'notes' in data:
            notes_data = data['notes']
            self.notes = notes_data if isinstance(notes_data, list) else list(notes_data.values())
        elif isinstance(data, dict):
            self.notes = list(data.values())
        else:
            self.notes = data if isinstance(data, list) else []
        
        logger.info(f"✅ Loaded {len(self.notes)} notes")
    
    def _load_vector_store(self):
        """Load ChromaDB."""
        settings = Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory='vector_store',
            anonymized_telemetry=False
        )
        self.client = chromadb.PersistentClient(path="vector_store")
        self.collection = self.client.get_collection('obsidian_notes')
    
    def suggest_by_content_similarity(self, note, top_k=5):
        """Find similar notes by content."""
        try:
            query_embedding = self.embedder.encode(note['content'][:2000]).tolist()
            
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k + 1,  # +1 to exclude self
                include=['metadatas', 'distances']
            )
            
            # Filter out self and return
            suggestions = []
            for meta, dist in zip(results['metadatas'][0], results['distances'][0]):
                if meta['title'] != note['title']:
                    relevance = 1 - dist
                    suggestions.append({
                        'title': meta['title'],
                        'folder': meta['folder'],
                        'relevance': float(relevance),
                        'reason': 'Similar content'
                    })
                    if len(suggestions) >= top_k:
                        break
            
            return suggestions
        except Exception as e:
            logger.error(f"Error: {e}")
            return []
    
    def suggest_by_tags(self, note):
        """Find notes with shared tags."""
        if not note['tags']:
            return []
        
        suggestions = []
        for other_note in self.notes:
            if other_note['id'] == note['id']:
                continue
            
            shared_tags = set(note['tags']) & set(other_note['tags'])
            if shared_tags:
                suggestions.append({
                    'title': other_note['title'],
                    'folder': other_note['file_metadata']['folder'],
                    'shared_tags': list(shared_tags),
                    'reason': f'Shared tags: {", ".join(shared_tags)}'
                })
        
        return suggestions[:5]
    
    def suggest_by_concepts(self, note):
        """Find notes with shared important concepts."""
        if not note['important_concepts']:
            return []
        
        suggestions = []
        for other_note in self.notes:
            if other_note['id'] == note['id']:
                continue
            
            shared = set(note['important_concepts']) & set(other_note['important_concepts'])
            if shared:
                suggestions.append({
                    'title': other_note['title'],
                    'folder': other_note['file_metadata']['folder'],
                    'shared_concepts': list(shared)[:3],
                    'reason': f'Shares concepts: {", ".join(list(shared)[:2])}'
                })
        
        return suggestions[:5]
    
    def generate_all_suggestions(self):
        """Generate suggestions for all notes."""
        logger.info(f"\n🔗 GENERATING LINK SUGGESTIONS")
        logger.info("=" * 80)
        
        all_suggestions = {}
        
        for i, note in enumerate(self.notes, 1):
            if i % max(1, len(self.notes) // 5) == 0:
                logger.info(f"   Progress: {i}/{len(self.notes)}")
            
            suggestions = {
                'by_content': self.suggest_by_content_similarity(note, top_k=3),
                'by_tags': self.suggest_by_tags(note),
                'by_concepts': self.suggest_by_concepts(note)
            }
            
            # Remove duplicates
            all_titles = set()
            unique_suggestions = []
            
            for category in ['by_content', 'by_tags', 'by_concepts']:
                for sugg in suggestions[category]:
                    if sugg['title'] not in all_titles:
                        all_titles.add(sugg['title'])
                        unique_suggestions.append(sugg)
            
            all_suggestions[note['id']] = {
                'note_title': note['title'],
                'suggestions': unique_suggestions[:5],
                'suggestion_count': len(unique_suggestions)
            }
        
        self.suggestions = all_suggestions
        logger.info(f"   ✅ Generated suggestions for {len(all_suggestions)} notes")
        
        return all_suggestions
    
    def save_suggestions(self, output_path='data/link_suggestions.json'):
        """Save suggestions."""
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.suggestions, f, indent=2)
        
        logger.info(f"✅ Saved suggestions to {output_file}")


def main():
    """Generate link suggestions."""
    print("\n" + "="*80)
    print("🔗 OBSIDIAN AI BRAIN - LINK SUGGESTER")
    print("="*80)
    
    suggester = LinkSuggester()
    
    if not suggester.notes:
        print("⚠️  Run previous phases first")
        return
    
    # Generate
    suggester.generate_all_suggestions()
    
    # Print sample
    print(f"\n📊 Sample suggestions:")
    for note_id, data in list(suggester.suggestions.items())[:3]:
        print(f"\n   📝 {data['note_title']}")
        for sugg in data['suggestions'][:2]:
            print(f"      → {sugg['title']} ({sugg['reason']})")
    
    # Save
    suggester.save_suggestions()
    
    print("\n✅ LINK SUGGESTIONS COMPLETE!")
    print("   Next: Run: python obsidian_05_knowledge_graph.py")
    print("="*80)


if __name__ == "__main__":
    main()