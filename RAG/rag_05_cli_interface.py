#!/usr/bin/env python3
"""
RAG CLI Interface - Interactive Question Answering
Ask questions about your research papers
"""

import logging
from pathlib import Path
from typing import List, Dict
import json
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
RESULTS_PATH = "./outputs/results"

class RAGPipeline:
    """RAG Pipeline - Retrieve documents and generate answers"""
    
    def __init__(self, model: str = DEFAULT_MODEL):
        """Initialize RAG pipeline"""
        logger.info("📂 Initializing RAG pipeline...")
        
        # Initialize Ollama
        logger.info(f"🤖 Initializing Ollama with model: {model}...")
        try:
            self.ollama = OllamaClient(base_url=OLLAMA_HOST)
        except:
            # Fallback for older ollama versions
            self.ollama = OllamaClient()
        self.current_model = model
        logger.info(f"   ✅ {model} ready")
        
        # Initialize embeddings
        logger.info(f"📦 Loading embedding model: {EMBEDDING_MODEL}...")
        self.embedder = SentenceTransformer(EMBEDDING_MODEL)
        logger.info("   ✅ Embedding model loaded")
        
        # Initialize vector store
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
            if count == 0:
                logger.error("⚠️  Vector database is empty!")
                logger.error("   Run: python rag_03_vector_database.py")
                raise RuntimeError("Vector database empty")
            
            logger.info(f"   ✅ ChromaDB loaded ({count} documents)")
        except Exception as e:
            logger.error(f"❌ Error loading ChromaDB: {e}")
            raise
        
        # Initialize results directory
        Path(RESULTS_PATH).mkdir(parents=True, exist_ok=True)
        self.query_history = []
        
    def retrieve(self, query: str, n_results: int = 5) -> List[Dict]:
        """Retrieve relevant documents"""
        try:
            # Get query embedding
            query_embedding = self.embedder.encode(query).tolist()
            
            # Search
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results
            )
            
            # Format results
            formatted = []
            if results['documents']:
                for i, doc in enumerate(results['documents'][0]):
                    formatted.append({
                        'content': doc,
                        'source': results['metadatas'][0][i].get('source', 'unknown'),
                        'page': results['metadatas'][0][i].get('page', 'N/A'),
                        'relevance': 1 - results['distances'][0][i]
                    })
            
            return formatted
        except Exception as e:
            logger.error(f"❌ Retrieval error: {e}")
            return []
    
    def generate(self, query: str, context: List[Dict]) -> str:
        """Generate answer using LLM"""
        # Build context
        context_text = "\n\n".join([
            f"Source: {doc['source']} (Page {doc['page']})\n{doc['content']}"
            for doc in context
        ])
        
        # Create prompt
        prompt = f"""Based on the following research paper excerpts, answer the question.

CONTEXT:
{context_text}

QUESTION: {query}

ANSWER:"""
        
        try:
            logger.info(f"🤖 Generating answer with {self.current_model}...")
            response = self.ollama.generate(
                model=self.current_model,
                prompt=prompt
            )
            # Handle response format
            if isinstance(response, dict) and 'response' in response:
                return response['response'].strip()
            else:
                return str(response).strip()
        except Exception as e:
            logger.error(f"❌ Generation error: {e}")
            return f"Error generating response: {e}"
    
    def answer(self, query: str) -> Dict:
        """Full RAG pipeline: retrieve + generate"""
        # Retrieve
        context = self.retrieve(query)
        
        if not context:
            return {
                'query': query,
                'answer': "No relevant documents found.",
                'sources': []
            }
        
        # Generate
        answer = self.generate(query, context)
        
        # Format response
        response = {
            'query': query,
            'answer': answer,
            'sources': [
                f"{doc['source']} (Page {doc['page']}, {doc['relevance']:.1%} relevant)"
                for doc in context
            ]
        }
        
        # Store in history
        self.query_history.append(response)
        
        return response
    
    def switch_model(self, model: str) -> bool:
        """Switch to different model"""
        try:
            # Test if model exists with simple call
            self.ollama.generate(model=model, prompt="test")
            self.current_model = model
            logger.info(f"✅ Switched to model: {model}")
            return True
        except Exception as e:
            logger.error(f"❌ Model not available: {model}")
            return False
    
    def save_history(self):
        """Save query history"""
        try:
            history_file = Path(RESULTS_PATH) / "query_history.json"
            with open(history_file, 'w') as f:
                json.dump(self.query_history, f, indent=2)
            logger.info(f"✅ History saved to {history_file}")
        except Exception as e:
            logger.error(f"❌ Error saving history: {e}")

def print_header():
    """Print application header"""
    print("\n" + "="*80)
    print("🤖 RESEARCH PAPER RAG - INTERACTIVE Q&A")
    print("="*80 + "\n")

def print_help():
    """Print help menu"""
    print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                           COMMAND REFERENCE                                ║
╠════════════════════════════════════════════════════════════════════════════╣
║ ask <question>          Ask a question about the papers                    ║
║ model <name>            Switch models (mistral, neural-chat, etc.)         ║
║ history                 Show query history                                 ║
║ save                    Save query history to file                         ║
║ help                    Show this help menu                                ║
║ exit / quit             Exit the application                               ║
╚════════════════════════════════════════════════════════════════════════════╝
""")

def main():
    """Main CLI loop"""
    print_header()
    
    # Initialize RAG
    try:
        rag = RAGPipeline()
    except Exception as e:
        logger.error(f"❌ Failed to initialize RAG pipeline: {e}")
        return
    
    print(f"✅ RAG System Ready!")
    print(f"📚 Vector Store: {VECTOR_STORE_PATH}")
    print(f"🤖 Model: {rag.current_model}")
    print(f"\nType 'help' for commands or ask a question directly:\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            # Parse commands
            if user_input.lower() == "exit" or user_input.lower() == "quit":
                print("\n✅ Saving history...")
                rag.save_history()
                print("👋 Goodbye!")
                break
            
            elif user_input.lower() == "help":
                print_help()
            
            elif user_input.lower() == "history":
                print("\n📋 QUERY HISTORY:")
                print("="*80)
                for i, item in enumerate(rag.query_history, 1):
                    print(f"\n{i}. Q: {item['query']}")
                    print(f"   A: {item['answer'][:100]}...")
                print()
            
            elif user_input.lower() == "save":
                rag.save_history()
                print("✅ History saved!\n")
            
            elif user_input.lower().startswith("model "):
                model_name = user_input[6:].strip()
                if rag.switch_model(model_name):
                    print(f"✅ Using {model_name} now\n")
                else:
                    print(f"❌ Model '{model_name}' not available\n")
            
            elif user_input.lower().startswith("ask "):
                query = user_input[4:].strip()
                print("\n⏳ Thinking...\n")
                response = rag.answer(query)
                
                print("="*80)
                print(f"Answer:\n{response['answer']}")
                print("\n" + "-"*80)
                print("Sources:")
                for source in response['sources']:
                    print(f"  • {source}")
                print("="*80 + "\n")
            
            else:
                # Direct question
                print("\n⏳ Thinking...\n")
                response = rag.answer(user_input)
                
                print("="*80)
                print(f"Answer:\n{response['answer']}")
                print("\n" + "-"*80)
                print("Sources:")
                for source in response['sources']:
                    print(f"  • {source}")
                print("="*80 + "\n")
        
        except KeyboardInterrupt:
            print("\n\n✅ Saving history...")
            rag.save_history()
            print("👋 Goodbye!")
            break
        except Exception as e:
            logger.error(f"❌ Error: {e}")
            print(f"Error: {e}\n")

if __name__ == "__main__":
    main()