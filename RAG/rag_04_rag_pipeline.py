"""
RAG Project - Phase 4: RAG Pipeline
Purpose: Retrieval + Generation with Mistral/Neural Chat switching
Author: RAze
Date: 2026-07-07
Runtime: ~10 seconds per query
"""

import json
from pathlib import Path
import chromadb
from chromadb.config import Settings
import logging
from datetime import datetime
from langchain.llms.ollama import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from sentence_transformers import SentenceTransformer

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class OllamaModelManager:
    """Manage switching between Ollama models."""
    
    def __init__(self):
        self.available_models = {
            'mistral': {
                'name': 'mistral:7b-instruct-q4_K_M',
                'description': 'Mistral - Accurate, good for detailed QA',
                'temperature': 0.3,  # Lower for accuracy
                'max_tokens': 2048
            },
            'neural-chat': {
                'name': 'neural-chat:7b-v3-q4_K_M',
                'description': 'Neural Chat - Fast and accurate',
                'temperature': 0.3,
                'max_tokens': 2048
            }
        }
        self.active_model = 'mistral'
        self.llm = None
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize the active model."""
        logger.info(f"🤖 Initializing {self.active_model}...")
        
        model_config = self.available_models[self.active_model]
        
        try:
            self.llm = Ollama(
                model=model_config['name'],
                temperature=model_config['temperature'],
                top_k=10,  # Focus on top predictions for accuracy
                top_p=0.9
            )
            logger.info(f"   ✅ {self.active_model} ready")
        except Exception as e:
            logger.error(f"   ❌ Failed to initialize {self.active_model}: {e}")
            logger.info("   Make sure 'ollama serve' is running!")
            raise
    
    def switch_model(self, model_name):
        """Switch to a different model."""
        if model_name not in self.available_models:
            logger.warning(f"⚠️  Model {model_name} not available")
            return False
        
        logger.info(f"\n🔄 Switching to {model_name}...")
        self.active_model = model_name
        self._initialize_model()
        return True
    
    def get_available_models(self):
        """Get list of available models."""
        return {
            name: config['description']
            for name, config in self.available_models.items()
        }
    
    def get_active_model(self):
        """Get the active model name."""
        return self.active_model


class RAGPipeline:
    """Retrieval-Augmented Generation pipeline."""
    
    def __init__(self, model_manager, persist_directory='vector_store'):
        self.model_manager = model_manager
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Initialize ChromaDB
        logger.info("📂 Loading ChromaDB...")
        settings = Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=persist_directory,
            anonymized_telemetry=False
        )
        client = chromadb.Client(settings)
        self.collection = client.get_collection(name='research_papers')
        logger.info(f"   ✅ ChromaDB loaded ({self.collection.count()} documents)")
        
        # Setup RAG prompt
        self.qa_prompt = PromptTemplate(
            input_variables=['context', 'question'],
            template="""You are an expert research paper analyst. 
Use the following research paper excerpts to answer the question accurately and thoroughly.

RESEARCH CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
- Be precise and cite specific findings from the papers
- If information is not in the provided context, say so clearly
- Structure your answer logically with key points
- Use academic language appropriate for research"""
        )
        
        # Setup retrieval-focused prompt
        self.summary_prompt = PromptTemplate(
            input_variables=['context'],
            template="""You are a research paper summarizer.
Analyze the following research paper excerpt and provide a clear, accurate summary.

RESEARCH CONTEXT:
{context}

SUMMARY:
- Key findings
- Methodology used
- Limitations or future work mentioned
- Significance to the field

Keep the summary concise but comprehensive."""
        )
    
    def retrieve_documents(self, query, top_k=5):
        """
        Retrieve relevant documents from ChromaDB.
        
        Returns top_k most relevant chunks with high similarity scores.
        """
        logger.info(f"🔍 Retrieving relevant documents...")
        
        # Embed the query
        query_embedding = self.embedding_model.encode(query).tolist()
        
        # Query ChromaDB with cosine similarity
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=['documents', 'metadatas', 'distances']
        )
        
        if not results['documents'] or len(results['documents'][0]) == 0:
            logger.warning("   ⚠️  No relevant documents found")
            return [], []
        
        documents = results['documents'][0]
        distances = results['distances'][0]
        metadatas = results['metadatas'][0]
        
        logger.info(f"   ✅ Found {len(documents)} relevant chunks")
        
        # Log relevance scores
        for i, (doc, dist, meta) in enumerate(zip(documents, distances, metadatas), 1):
            relevance = 1 - dist  # Convert distance to similarity
            logger.info(f"      [{i}] {meta['title']} (relevance: {relevance:.3f})")
        
        return documents, metadatas
    
    def answer_question(self, question):
        """
        Answer a question using RAG pipeline.
        
        1. Retrieve relevant documents
        2. Create context
        3. Use LLM to generate answer
        """
        print(f"\n" + "="*80)
        print(f"❓ QUESTION: {question}")
        print("="*80)
        
        # Step 1: Retrieve
        documents, metadatas = self.retrieve_documents(question, top_k=5)
        
        if not documents:
            print("\n⚠️  Unable to find relevant documents. Try a different question.")
            return None
        
        # Step 2: Create context
        context = "\n\n---\n\n".join(documents)
        context = context[:3000]  # Limit context size for efficiency
        
        # Step 3: Generate answer
        logger.info(f"\n💭 Generating answer with {self.model_manager.get_active_model()}...")
        
        try:
            chain = LLMChain(
                llm=self.model_manager.llm,
                prompt=self.qa_prompt
            )
            
            answer = chain.run(context=context, question=question)
            
            print(f"\n📄 ANSWER:")
            print("-" * 80)
            print(answer)
            print("-" * 80)
            
            # Log sources
            print(f"\n📚 Sources:")
            for i, meta in enumerate(metadatas, 1):
                print(f"   [{i}] {meta['title']} (Page {meta['pages']})")
            
            return {
                'question': question,
                'answer': answer,
                'sources': metadatas,
                'model': self.model_manager.get_active_model(),
                'timestamp': datetime.now().isoformat()
            }
        
        except Exception as e:
            logger.error(f"   ❌ Error generating answer: {e}")
            return None
    
    def summarize_papers(self, top_k=5):
        """Summarize loaded research papers."""
        print(f"\n" + "="*80)
        print(f"📄 SUMMARIZING RESEARCH PAPERS")
        print("="*80)
        
        logger.info(f"Loading top {top_k} paper chunks...")
        
        results = self.collection.query(
            query_embeddings=[self.embedding_model.encode("research").tolist()],
            n_results=top_k,
            include=['documents', 'metadatas']
        )
        
        for i, (doc, meta) in enumerate(zip(
            results['documents'][0], 
            results['metadatas'][0]
        ), 1):
            print(f"\n📚 [{i}] {meta['title']}")
            print("-" * 80)
            
            try:
                chain = LLMChain(
                    llm=self.model_manager.llm,
                    prompt=self.summary_prompt
                )
                
                summary = chain.run(context=doc[:2000])
                print(summary)
            
            except Exception as e:
                logger.error(f"Error summarizing: {e}")


def main():
    """Run RAG pipeline demo."""
    print("\n" + "="*80)
    print("🔬 RESEARCH PAPER RAG PIPELINE")
    print("="*80)
    
    # Initialize model manager
    try:
        model_manager = OllamaModelManager()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n⚠️  Make sure:")
        print("   1. Ollama is running: ollama serve")
        print("   2. Models are downloaded: ollama pull mistral:7b-instruct-q4_K_M")
        return
    
    # Initialize RAG pipeline
    try:
        rag = RAGPipeline(model_manager)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n⚠️  Vector database not found. Run Phase 3 first:")
        print("   python rag_03_vector_database.py")
        return
    
    # Available models
    print("\n🤖 Available Models:")
    for model, desc in model_manager.get_available_models().items():
        print(f"   • {model}: {desc}")
    
    # Demo questions
    demo_questions = [
        "What are the main findings of this research?",
        "What methodology was used in this paper?",
        "What are the key limitations mentioned?",
    ]
    
    # Run demo
    print("\n📌 Running demo queries...")
    print("(Add your own papers to data/papers/ for real results)\n")
    
    for question in demo_questions:
        result = rag.answer_question(question)
        
        if result:
            # Save result
            output_dir = Path('outputs/results')
            output_dir.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = output_dir / f"result_{timestamp}.json"
            
            with open(output_file, 'w') as f:
                json.dump(result, f, indent=2)
    
    # Model switching demo
    print("\n" + "="*80)
    print("🔄 MODEL SWITCHING DEMO")
    print("="*80)
    
    print("\n💬 Switching to Neural Chat...")
    model_manager.switch_model('neural-chat')
    
    if demo_questions:
        result = rag.answer_question(demo_questions[0])
    
    print("\n" + "="*80)
    print("✅ RAG PIPELINE DEMO COMPLETE!")
    print("="*80)
    print("""
✅ What was demonstrated:
   • Document retrieval (semantic search)
   • Context creation from relevant papers
   • Answer generation with LLM
   • Model switching (Mistral ↔ Neural Chat)
   • Result saving

🔄 Next step:
   Run: python rag_05_cli_interface.py
   (For interactive querying)
""")


if __name__ == "__main__":
    main()
