"""
Obsidian AI Brain - Phase 3: Embeddings & Vector Store
Purpose: Create embeddings and store in ChromaDB
Author: RAze
Date: 2026-07-08
"""

import json
from pathlib import Path
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EmbeddingGenerator:
    """Generate embeddings for note content."""
    
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        logger.info(f"🔧 Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)
        self.dimension = self.model.get_sentence_embedding_dimension()
        logger.info(f"   ✅ Model loaded (dimension: {self.dimension})")
    
    def embed_text(self, text):
        """Embed single text."""
        try:
            embedding = self.model.encode(text, convert_to_numpy=True)
            return embedding.tolist()
        except Exception as e:
            logger.error(f"Error embedding: {e}")
            return None
    
    def embed_batch(self, texts, batch_size=32):
        """Embed multiple texts."""
        logger.info(f"🔄 Embedding {len(texts)} notes...")
        embeddings = self.model.encode(texts, batch_size=batch_size, convert_to_numpy=True)
        return [emb.tolist() for emb in embeddings]


class VectorStoreManager:
    """Manage ChromaDB vector store."""
    
    def __init__(self, persist_directory='vector_store', collection_name='obsidian_notes'):
        logger.info(f"🗄️  Initializing ChromaDB...")
        
        settings = Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=persist_directory,
            anonymized_telemetry=False
        )
        
        self.client = chromadb.PersistentClient(path="vector_store")
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={'hnsw:space': 'cosine'}
        )
        
        self.persist_directory = persist_directory
        logger.info(f"   ✅ ChromaDB initialized")
    
    def add_notes(self, notes, embeddings):
        """Add notes and embeddings to store."""
        logger.info(f"\n📥 Adding {len(notes)} notes to ChromaDB...")
        
        ids = []
        documents = []
        metadatas = []
        
        for note, embedding in zip(notes, embeddings):
            ids.append(note['id'])
            documents.append(note['content'][:5000])  # Limit content
            metadatas.append({
                'title': note['title'],
                'folder': note['file_metadata']['folder'],
                'tags': ','.join(note['tags']) if note['tags'] else '',
                'links': ','.join(note['links']) if note['links'] else '',
                'word_count': str(note['readability']['total_words']),
                'modified': note['file_metadata']['modified']
            })
        
        try:
            self.collection.add(
                ids=ids,
                documents=documents,
                embeddings=[e for e in embeddings],
                metadatas=metadatas
            )
            logger.info(f"   ✅ Added {len(notes)} notes")
            return True
        except Exception as e:
            logger.error(f"   ❌ Error: {e}")
            return False
    
    def persist(self):
        """Persist database."""
        logger.info(f"\n💾 Persisting database...")
        try:
            self.client.persist()
            logger.info(f"   ✅ Database persisted")
            return True
        except Exception as e:
            logger.error(f"   ❌ Error: {e}")
            return False
    
    def get_stats(self):
        """Get collection stats."""
        return {'total_notes': self.collection.count()}


def main():
    """Generate embeddings and create vector store."""
    print("\n" + "="*80)
    print("🔤 OBSIDIAN AI BRAIN - EMBEDDINGS & VECTOR STORE")
    print("="*80)
    
    # Load enriched notes
    enriched_file = Path('data/enriched_notes.json')
    if not enriched_file.exists():
        print("⚠️  Run obsidian_02_note_parser.py first")
        return
    
    with open(enriched_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    notes = data['notes']
    print(f"\n   ✅ Loaded {len(notes)} enriched notes")
    
    # Generate embeddings
    embedder = EmbeddingGenerator('all-MiniLM-L6-v2')
    texts = [note['content'][:2000] for note in notes]  # Use first 2000 chars
    embeddings = embedder.embed_batch(texts)
    
    if not embeddings:
        print("❌ Failed to generate embeddings")
        return
    
    print(f"   ✅ Generated {len(embeddings)} embeddings")
    
    # Create vector store
    store = VectorStoreManager()
    if not store.add_notes(notes, embeddings):
        print("❌ Failed to add notes to store")
        return
    
    # Persist
    store.persist()
    
    # Summary
    stats = store.get_stats()
    print("\n" + "="*80)
    print("✅ EMBEDDINGS & VECTOR STORE READY!")
    print("="*80)
    print(f"   Total notes stored: {stats['total_notes']}")
    print(f"   Next: Run: python obsidian_04_link_suggester.py")
    print("="*80)


if __name__ == "__main__":
    main()
