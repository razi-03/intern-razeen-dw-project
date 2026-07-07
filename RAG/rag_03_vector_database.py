#!/usr/bin/env python3
"""
RAG Vector Database - ChromaDB Vector Store
Loads chunked documents and creates embeddings
"""

import os
import json
import logging
from pathlib import Path
from typing import List, Dict
from sentence_transformers import SentenceTransformer
import chromadb

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
VECTOR_STORE_PATH = "./vector_store"
METADATA_PATH = "./data/metadata"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # Fast & efficient embeddings

class ChromaVectorStore:
    """ChromaDB Vector Store - Store embeddings and retrieve similar documents"""
    
    def __init__(self):
        """Initialize ChromaDB with new API"""
        logger.info("🗄️  Initializing ChromaDB...")
        
        # Create vector store directory if it doesn't exist
        Path(VECTOR_STORE_PATH).mkdir(parents=True, exist_ok=True)
        
        # NEW ChromaDB API - Use PersistentClient instead of deprecated Client
        self.client = chromadb.PersistentClient(path=VECTOR_STORE_PATH)
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name="research_papers",
            metadata={"hnsw:space": "cosine"}
        )
        
        # Load embedding model
        logger.info(f"📦 Loading embedding model: {EMBEDDING_MODEL}...")
        self.model = SentenceTransformer(EMBEDDING_MODEL)
        logger.info("✅ Embedding model loaded")
        
    def add_documents(self, documents: List[Dict]):
        """Add documents with embeddings to ChromaDB"""
        if not documents:
            logger.warning("⚠️  No documents to add")
            return
            
        logger.info(f"📝 Adding {len(documents)} documents to vector store...")
        
        ids = []
        embeddings = []
        documents_list = []
        metadatas = []
        
        for i, doc in enumerate(documents):
            # Generate ID
            doc_id = f"doc_{doc.get('paper_id', 'unknown')}_{i}"
            ids.append(doc_id)
            
            # Get embedding
            text = doc.get('text', '')
            if not text:
                logger.warning(f"⚠️  Document {i} has no text, skipping")
                continue
                
            embedding = self.model.encode(text).tolist()
            embeddings.append(embedding)
            
            # Store document
            documents_list.append(text)
            
            # Store metadata
            metadata = {
                'paper_id': doc.get('paper_id', 'unknown'),
                'chunk_index': str(doc.get('chunk_index', 0)),
                'source': doc.get('source', 'unknown'),
                'page': str(doc.get('page', 0))
            }
            metadatas.append(metadata)
            
            if (i + 1) % 20 == 0:
                logger.info(f"   📊 Processed {i + 1}/{len(documents)} documents")
        
        # Add to collection
        if not ids:
            logger.error("❌ No valid documents to add")
            return
            
        try:
            self.collection.add(
                ids=ids,
                embeddings=embeddings,
                documents=documents_list,
                metadatas=metadatas
            )
            logger.info(f"✅ Successfully added {len(documents_list)} documents to ChromaDB")
        except Exception as e:
            logger.error(f"❌ Error adding documents: {e}")
            raise
    
    def search(self, query: str, n_results: int = 5) -> List[Dict]:
        """Search for similar documents"""
        logger.info(f"🔍 Searching for: {query}")
        
        # Get embedding for query
        query_embedding = self.model.encode(query).tolist()
        
        # Search
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        
        # Format results
        formatted_results = []
        if results['documents']:
            for i, doc in enumerate(results['documents'][0]):
                formatted_results.append({
                    'id': results['ids'][0][i],
                    'document': doc,
                    'metadata': results['metadatas'][0][i],
                    'distance': results['distances'][0][i]
                })
        
        return formatted_results
    
    def get_stats(self) -> Dict:
        """Get vector store statistics"""
        count = self.collection.count()
        return {
            'total_documents': count,
            'collection_name': self.collection.name
        }

def load_chunks():
    """Load chunks from JSON file created by rag_02_data_loader.py"""
    logger.info("📂 Loading document chunks...")
    
    chunks_file = Path(METADATA_PATH) / "chunks.json"
    
    if not chunks_file.exists():
        logger.error(f"❌ Chunks file not found at {chunks_file}")
        logger.error("   Run rag_02_data_loader.py first to create chunks")
        return []
    
    try:
        with open(chunks_file, 'r', encoding='utf-8') as f:
            chunks = json.load(f)
        logger.info(f"✅ Loaded {len(chunks)} chunks from {chunks_file.name}")
        return chunks
    except Exception as e:
        logger.error(f"❌ Error loading chunks: {e}")
        return []

def main():
    """Main execution"""
    print("\n" + "="*80)
    print("🗄️  INITIALIZING CHROMADB")
    print("="*80 + "\n")
    
    # Initialize vector store
    vector_store = ChromaVectorStore()
    
    # Load chunks
    chunks = load_chunks()
    
    if not chunks:
        logger.error("❌ No chunks found! Please run rag_02_data_loader.py first")
        return
    
    # Add to vector store
    vector_store.add_documents(chunks)
    
    # Get statistics
    stats = vector_store.get_stats()
    
    print("\n" + "="*80)
    print("✅ VECTOR DATABASE CREATED SUCCESSFULLY!")
    print("="*80)
    print(f"📊 Total documents: {stats['total_documents']}")
    print(f"📍 Location: {VECTOR_STORE_PATH}/")
    print(f"🔍 Collection: {stats['collection_name']}")
    print("\n✅ Next step: python rag_04_rag_pipeline.py (optional demo)")
    print("✅ Or start Q&A: python rag_05_cli_interface.py\n")
    
    # Test search
    print("="*80)
    print("🧪 TESTING VECTOR SEARCH")
    print("="*80 + "\n")
    
    test_queries = ["learning", "model", "data"]
    
    for test_query in test_queries:
        results = vector_store.search(test_query, n_results=2)
        
        if results:
            print(f"✅ Search for '{test_query}': Found {len(results)} results")
            for i, result in enumerate(results[:1], 1):
                preview = result['document'][:80].replace('\n', ' ')
                print(f"   📝 {preview}...\n")
        else:
            print(f"⚠️  No results for '{test_query}'\n")
    
    print("="*80)
    print("🚀 READY FOR RAG QUERIES!")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()