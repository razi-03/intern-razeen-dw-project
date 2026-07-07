"""
RAG Project - Phase 3: Vector Database with ChromaDB
Purpose: Create embeddings and store in ChromaDB
Author: RAze
Date: 2026-07-07
Runtime: ~2-5 minutes (depends on document size)
"""

import json
from pathlib import Path
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class EmbeddingGenerator:
    """Generate embeddings for text chunks."""
    
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        """
        Initialize embedding model.
        
        all-MiniLM-L6-v2: Fast, accurate, 384 dimensions
        - Good for accuracy-first approach
        - ~80MB model size
        - ~5ms per chunk
        """
        logger.info(f"🔧 Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)
        self.dimension = self.model.get_sentence_embedding_dimension()
        logger.info(f"   ✅ Model loaded (dimension: {self.dimension})")
    
    def embed_text(self, text):
        """Generate embedding for a single text."""
        try:
            embedding = self.model.encode(text, convert_to_numpy=True)
            return embedding.tolist()
        except Exception as e:
            logger.error(f"   ❌ Error embedding text: {e}")
            return None
    
    def embed_batch(self, texts, batch_size=32):
        """Generate embeddings for multiple texts."""
        logger.info(f"🔄 Embedding {len(texts)} chunks...")
        embeddings = self.model.encode(texts, batch_size=batch_size, convert_to_numpy=True)
        return [emb.tolist() for emb in embeddings]


class ChromaVectorStore:
    """Manage ChromaDB vector storage."""
    
    def __init__(self, persist_directory='vector_store', collection_name='research_papers'):
        """Initialize ChromaDB."""
        logger.info(f"🗄️  Initializing ChromaDB...")
        
        # Create settings for persistence
        settings = Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=persist_directory,
            anonymized_telemetry=False
        )
        
        # Initialize client
        self.client = chromadb.Client(settings)
        
        # Create or get collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={'hnsw:space': 'cosine'}  # Cosine similarity for accuracy
        )
        
        self.persist_directory = persist_directory
        logger.info(f"   ✅ ChromaDB initialized")
    
    def add_documents(self, chunks, embeddings):
        """Add documents and embeddings to ChromaDB."""
        logger.info(f"\n📥 Adding {len(chunks)} documents to ChromaDB...")
        
        ids = []
        documents = []
        metadatas = []
        vectors = []
        
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            chunk_id = f"{chunk['source']}_{chunk['chunk_index']}"
            ids.append(chunk_id)
            documents.append(chunk['text'])
            metadatas.append({
                'source': chunk['source'],
                'chunk_index': str(chunk['chunk_index']),
                'title': chunk['metadata'].get('title', 'Unknown'),
                'pages': str(chunk['metadata'].get('pages', 'Unknown'))
            })
            vectors.append(embedding)
            
            # Progress indicator
            if (i + 1) % 100 == 0:
                logger.info(f"   Processed {i + 1}/{len(chunks)} documents")
        
        # Add to collection
        try:
            self.collection.add(
                ids=ids,
                documents=documents,
                embeddings=vectors,
                metadatas=metadatas
            )
            logger.info(f"   ✅ Successfully added {len(chunks)} documents")
            return True
        except Exception as e:
            logger.error(f"   ❌ Error adding documents: {e}")
            return False
    
    def persist(self):
        """Persist the database to disk."""
        logger.info(f"\n💾 Persisting ChromaDB to {self.persist_directory}...")
        try:
            self.client.persist()
            logger.info(f"   ✅ Database persisted")
            return True
        except Exception as e:
            logger.error(f"   ❌ Error persisting: {e}")
            return False
    
    def get_collection_stats(self):
        """Get statistics about the collection."""
        count = self.collection.count()
        return {
            'total_documents': count,
            'collection_name': self.collection.name
        }


class VectorDBValidator:
    """Validate the vector database."""
    
    @staticmethod
    def validate_storage(vector_store):
        """Validate vector storage."""
        logger.info("\n🔍 Validating Vector Database...")
        
        stats = vector_store.get_collection_stats()
        
        print(f"\n   📊 Collection Statistics:")
        print(f"      Collection: {stats['collection_name']}")
        print(f"      Documents: {stats['total_documents']}")
        
        if stats['total_documents'] == 0:
            logger.warning("   ⚠️  No documents in database!")
            return False
        
        logger.info("   ✅ Vector database valid!")
        return True
    
    @staticmethod
    def test_retrieval(vector_store, embedding_model, query_text="research methodology"):
        """Test basic retrieval."""
        logger.info(f"\n🧪 Testing retrieval with query: '{query_text}'")
        
        # Embed query
        query_embedding = embedding_model.embed_text(query_text)
        
        if query_embedding is None:
            logger.error("   ❌ Failed to embed query")
            return False
        
        # Query the collection
        try:
            results = vector_store.collection.query(
                query_embeddings=[query_embedding],
                n_results=3
            )
            
            if results['documents'] and len(results['documents'][0]) > 0:
                logger.info(f"   ✅ Retrieval works!")
                logger.info(f"      Found {len(results['documents'][0])} results")
                
                # Show top result
                print(f"\n   Top result:")
                print(f"      Distance: {results['distances'][0][0]:.4f}")
                print(f"      Text: {results['documents'][0][0][:100]}...")
                
                return True
            else:
                logger.warning("   ⚠️  No results returned")
                return False
        
        except Exception as e:
            logger.error(f"   ❌ Error during retrieval: {e}")
            return False


def main():
    """Setup vector database."""
    print("\n" + "="*80)
    print("🗄️  VECTOR DATABASE SETUP")
    print("="*80)
    
    # Load chunks from Phase 2
    chunks_file = Path('data/metadata/chunks.json')
    if not chunks_file.exists():
        print(f"\n❌ Chunks file not found: {chunks_file}")
        print("   Run Phase 2 first: python rag_02_data_loader.py")
        return
    
    logger.info(f"📂 Loading chunks from {chunks_file}")
    with open(chunks_file, 'r') as f:
        chunks = json.load(f)
    
    print(f"\n   ✅ Loaded {len(chunks)} chunks")
    
    # Initialize embedding model
    embedding_gen = EmbeddingGenerator('all-MiniLM-L6-v2')
    
    # Generate embeddings
    print(f"\n" + "="*80)
    print("🔤 GENERATING EMBEDDINGS")
    print("="*80)
    texts = [chunk['text'] for chunk in chunks]
    embeddings = embedding_gen.embed_batch(texts)
    
    if not embeddings:
        print("\n❌ Failed to generate embeddings")
        return
    
    print(f"   ✅ Generated {len(embeddings)} embeddings")
    
    # Initialize ChromaDB
    print(f"\n" + "="*80)
    print("🗄️  INITIALIZING CHROMADB")
    print("="*80)
    vector_store = ChromaVectorStore()
    
    # Add documents
    if not vector_store.add_documents(chunks, embeddings):
        print("\n❌ Failed to add documents to ChromaDB")
        return
    
    # Persist
    vector_store.persist()
    
    # Validate
    print(f"\n" + "="*80)
    print("✅ VALIDATION")
    print("="*80)
    validator = VectorDBValidator()
    validator.validate_storage(vector_store)
    validator.test_retrieval(vector_store, embedding_gen)
    
    # Summary
    print("\n" + "="*80)
    print("✅ VECTOR DATABASE READY!")
    print("="*80)
    print(f"""
✅ Completed:
   • Generated embeddings for {len(chunks)} chunks
   • Stored in ChromaDB (chromadb.ai)
   • Persistent storage enabled
   • Validated and tested retrieval

📊 Database Info:
   • Location: vector_store/
   • Collection: research_papers
   • Total chunks: {len(chunks)}
   • Embedding model: all-MiniLM-L6-v2
   • Distance metric: cosine (for accuracy)

🔄 Next step:
   Run: python rag_04_rag_pipeline.py
""")
    print("="*80)


if __name__ == "__main__":
    main()
