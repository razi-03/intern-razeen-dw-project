#!/usr/bin/env python3
"""
RAG Pipeline - Test the Retrieval-Augmented Generation system
Demonstrates how to retrieve documents and generate answers
"""

import logging
from pathlib import Path
from typing import List, Dict
from sentence_transformers import SentenceTransformer
import chromadb
from ollama import Client as OllamaClient

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
VECTOR_STORE_PATH = "./vector_store"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
OLLAMA_HOST = "http://localhost:11434"
DEFAULT_MODEL = "mistral:7b"

class RAGPipeline:
    """Retrieval-Augmented Generation Pipeline"""
    
    def __init__(self, model: str = DEFAULT_MODEL):
        """Initialize RAG pipeline"""
        logger.info("🚀 Initializing RAG Pipeline...\n")
        
        # Initialize Ollama
        logger.info(f"🤖 Initializing Ollama models...")
        logger.info(f"🤖 Initializing {model}...")
        try:
            self.ollama = OllamaClient(base_url=OLLAMA_HOST)
        except:
            # Fallback for older ollama versions
            self.ollama = OllamaClient()
        self.current_model = model
        logger.info(f"   ✅ {model} ready\n")
        
        # Initialize embeddings
        logger.info(f"📦 Loading embedding model: {EMBEDDING_MODEL}...")
        self.embedder = SentenceTransformer(EMBEDDING_MODEL)
        logger.info("   ✅ Embedding model loaded\n")
        
        # Initialize vector store
        logger.info("📂 Initializing RAG pipeline...")
        logger.info("📂 Loading ChromaDB...")
        try:
            Path(VECTOR_STORE_PATH).mkdir(parents=True, exist_ok=True)
            
            # NEW ChromaDB API - Use PersistentClient
            self.chroma_client = chromadb.PersistentClient(path=VECTOR_STORE_PATH)
            self.collection = self.chroma_client.get_or_create_collection(
                name="research_papers",
                metadata={"hnsw:space": "cosine"}
            )
            
            count = self.collection.count()
            logger.info(f"   ✅ ChromaDB loaded ({count} documents)\n")
        except Exception as e:
            logger.error(f"❌ Error loading ChromaDB: {e}")
            raise
    
    def retrieve(self, query: str, n_results: int = 5) -> List[Dict]:
        """Retrieve relevant documents from vector store"""
        logger.info(f"🔍 Retrieving documents for: '{query}'")
        
        try:
            # Get query embedding
            query_embedding = self.embedder.encode(query).tolist()
            
            # Search vector store
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results
            )
            
            # Format results
            formatted = []
            if results['documents']:
                for i, doc in enumerate(results['documents'][0]):
                    relevance = 1 - results['distances'][0][i]
                    formatted.append({
                        'content': doc,
                        'source': results['metadatas'][0][i].get('source', 'unknown'),
                        'page': results['metadatas'][0][i].get('page', 'N/A'),
                        'relevance': relevance
                    })
                    logger.info(f"   📄 {formatted[-1]['source']} (relevance: {relevance:.1%})")
            
            logger.info(f"   ✅ Retrieved {len(formatted)} documents\n")
            return formatted
        except Exception as e:
            logger.error(f"❌ Retrieval error: {e}")
            return []
    
    def generate(self, query: str, context: List[Dict]) -> str:
        """Generate answer using LLM with retrieved context"""
        logger.info(f"📝 Generating answer with {self.current_model}...")
        
        # Build context string
        context_text = "\n\n".join([
            f"[Source: {doc['source']}, Page {doc['page']}]\n{doc['content']}"
            for doc in context
        ])
        
        # Create prompt
        prompt = f"""Based on the following research paper excerpts, answer the question comprehensively.

RESEARCH PAPER CONTEXT:
{context_text}

QUESTION: {query}

ANSWER: Please provide a detailed answer based on the above context."""
        
        try:
            response = self.ollama.generate(
                model=self.current_model,
                prompt=prompt
            )
            # Handle response format
            if isinstance(response, dict) and 'response' in response:
                answer = response['response'].strip()
            else:
                answer = str(response).strip()
            logger.info(f"   ✅ Answer generated\n")
            return answer
        except Exception as e:
            logger.error(f"❌ Generation error: {e}")
            return f"Error: Could not generate response - {e}"
    
    def run(self, query: str) -> Dict:
        """Run complete RAG pipeline"""
        logger.info("="*80)
        logger.info("🚀 RAG PIPELINE EXECUTION")
        logger.info("="*80 + "\n")
        
        logger.info(f"❓ QUESTION: {query}\n")
        
        # Step 1: Retrieve
        context = self.retrieve(query)
        
        if not context:
            return {
                'query': query,
                'answer': "No relevant documents found in the vector store.",
                'context': [],
                'model': self.current_model
            }
        
        # Step 2: Generate
        answer = self.generate(query, context)
        
        return {
            'query': query,
            'answer': answer,
            'context': context,
            'model': self.current_model
        }

def print_result(result: Dict):
    """Pretty print RAG result"""
    print("\n" + "="*80)
    print("📋 RAG PIPELINE RESULT")
    print("="*80 + "\n")
    
    print(f"❓ Question: {result['query']}")
    print(f"🤖 Model: {result['model']}\n")
    
    print("-"*80)
    print("📝 ANSWER:")
    print("-"*80)
    print(f"\n{result['answer']}\n")
    
    if result['context']:
        print("-"*80)
        print("📚 SOURCES USED:")
        print("-"*80)
        for i, doc in enumerate(result['context'], 1):
            print(f"\n{i}. {doc['source']} (Page {doc['page']})")
            print(f"   Relevance: {doc['relevance']:.1%}")
            print(f"   Content: {doc['content'][:100]}...")
    
    print("\n" + "="*80 + "\n")

def main():
    """Main execution"""
    print("\n" + "="*80)
    print("🚀 RESEARCH PAPER RAG - PIPELINE TEST")
    print("="*80 + "\n")
    
    # Initialize RAG pipeline
    try:
        rag = RAGPipeline()
    except Exception as e:
        logger.error(f"❌ Failed to initialize: {e}")
        return
    
    # Test queries
    test_queries = [
        "What is the main focus of these research papers?",
        "What methodologies are used in these papers?",
        "What are the key findings or contributions?"
    ]
    
    print("="*80)
    print("🧪 TESTING RAG PIPELINE WITH SAMPLE QUERIES")
    print("="*80 + "\n")
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{'='*80}")
        print(f"TEST {i}/{len(test_queries)}")
        print(f"{'='*80}\n")
        
        try:
            result = rag.run(query)
            print_result(result)
            
            # Pause for readability
            if i < len(test_queries):
                input("Press Enter to continue to next test...")
        except Exception as e:
            logger.error(f"❌ Test failed: {e}")
    
    print("\n" + "="*80)
    print("✅ PIPELINE TEST COMPLETE!")
    print("="*80)
    print("\n✅ Next step: Run interactive CLI")
    print("   python rag_05_cli_interface.py\n")

if __name__ == "__main__":
    main()