#!/usr/bin/env python3
"""
RAG Web Interface - Streamlit UI (Improved)
Beautiful web interface for Research Paper Question Answering
"""

import streamlit as st
import logging
from pathlib import Path
from typing import List, Dict
import json
from datetime import datetime

# Configure page FIRST
st.set_page_config(
    page_title="📚 Research Paper RAG",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
VECTOR_STORE_PATH = "./vector_store"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
OLLAMA_HOST = "http://localhost:11434"
RESULTS_PATH = "./outputs/results"

# Custom CSS
st.markdown("""
<style>
    .main { padding: 0rem 1rem; }
    .stButton>button { width: 100%; padding: 10px; border-radius: 5px; }
    .source-box { 
        background-color: #f0f2f6; 
        padding: 15px; 
        border-radius: 5px; 
        margin: 10px 0; 
        border-left: 4px solid #0066cc; 
    }
    .answer-box { 
        background-color: #f8f9fa; 
        padding: 20px; 
        border-radius: 5px; 
        margin: 20px 0;
        color: #000000;
        font-size: 16px;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def initialize_rag():
    """Initialize RAG pipeline with error handling"""
    try:
        from sentence_transformers import SentenceTransformer
        import chromadb
        from ollama import Client as OllamaClient
        
        errors = []
        
        # Check vector database
        if not Path(VECTOR_STORE_PATH).exists():
            errors.append("Vector database not found. Run: python rag_03_vector_database.py")
        
        # Initialize Ollama
        try:
            ollama = OllamaClient(base_url=OLLAMA_HOST)
            # Test connection
            ollama.list()
        except Exception as e:
            errors.append(f"Ollama not responding: {e}")
        
        # Initialize embeddings
        try:
            embedder = SentenceTransformer(EMBEDDING_MODEL)
        except Exception as e:
            errors.append(f"Embedding model error: {e}")
        
        # Initialize ChromaDB
        try:
            Path(VECTOR_STORE_PATH).mkdir(parents=True, exist_ok=True)
            chroma_client = chromadb.PersistentClient(path=VECTOR_STORE_PATH)
            collection = chroma_client.get_or_create_collection(
                name="research_papers",
                metadata={"hnsw:space": "cosine"}
            )
            doc_count = collection.count()
            if doc_count == 0:
                errors.append("Vector database is empty")
        except Exception as e:
            errors.append(f"ChromaDB error: {e}")
        
        if errors:
            return {'status': 'error', 'errors': errors}
        
        return {
            'status': 'success',
            'ollama': ollama,
            'embedder': embedder,
            'collection': collection,
            'chroma_client': chroma_client,
            'doc_count': doc_count
        }
    except Exception as e:
        return {'status': 'error', 'errors': [f"Initialization error: {str(e)}"]}

def retrieve_documents(query: str, collection, embedder, n_results: int = 5) -> List[Dict]:
    """Retrieve relevant documents"""
    try:
        query_embedding = embedder.encode(query).tolist()
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=min(n_results, 10)
        )
        
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
        
        return formatted
    except Exception as e:
        logger.error(f"Retrieval error: {e}")
        return []

def generate_answer(query: str, context: List[Dict], ollama, model: str) -> str:
    """Generate answer using LLM"""
    try:
        context_text = "\n\n".join([
            f"Source: {doc['source']} (Page {doc['page']})\n{doc['content']}"
            for doc in context
        ])
        
        prompt = f"""Based on the following research paper excerpts, answer the question.

CONTEXT:
{context_text}

QUESTION: {query}

ANSWER:"""
        
        response = ollama.generate(model=model, prompt=prompt)
        
        if isinstance(response, dict) and 'response' in response:
            return response['response'].strip()
        else:
            return str(response).strip()
    except Exception as e:
        return f"Error: {str(e)}"

def save_to_history(query: str, answer: str, sources: List[Dict], model: str):
    """Save query to history"""
    try:
        Path(RESULTS_PATH).mkdir(parents=True, exist_ok=True)
        history_file = Path(RESULTS_PATH) / "web_history.json"
        
        entry = {
            'timestamp': datetime.now().isoformat(),
            'query': query,
            'answer': answer[:500],
            'sources': [{'source': s['source'], 'page': s['page']} for s in sources],
            'model': model
        }
        
        history = []
        if history_file.exists():
            try:
                with open(history_file, 'r') as f:
                    history = json.load(f)
            except:
                history = []
        
        history.append(entry)
        
        with open(history_file, 'w') as f:
            json.dump(history, f, indent=2)
    except Exception as e:
        logger.error(f"Error saving history: {e}")

# Initialize session state
if 'rag' not in st.session_state:
    st.session_state.rag = initialize_rag()
    st.session_state.model = "mistral:7b"
    st.session_state.history = []

# Header
st.markdown("# 📚 Research Paper RAG System")
st.markdown("Ask questions about your research papers using AI-powered search.")

# Check initialization status
rag_status = st.session_state.rag

if rag_status['status'] == 'error':
    st.error("❌ Failed to initialize RAG system.")
    st.warning("**Troubleshooting:**")
    for error in rag_status['errors']:
        st.warning(f"• {error}")
    st.info("""
    **Fix:**
    1. Make sure 'ollama serve' is running in another terminal
    2. Run: `python rag_03_vector_database.py` if vector DB is missing
    3. Refresh this page (F5)
    """)
else:
    # Sidebar
    with st.sidebar:
        st.markdown("## ⚙️ Settings")
        
        model = st.selectbox(
            "🤖 Select Model",
            ["mistral:7b", "neural-chat:latest"],
            index=0,
        )
        st.session_state.model = model
        
        n_results = st.slider("📊 Sources", 1, 10, 5)
        
        st.markdown("---")
        st.markdown("## 📈 Status")
        st.metric("Documents", rag_status.get('doc_count', 0))
        st.metric("Model", st.session_state.model)
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("## ❓ Ask a Question")
        query = st.text_area(
            "Enter your question:",
            placeholder="e.g., What is the methodology?",
            height=80,
            label_visibility="collapsed"
        )
        
        col_ask, col_clear = st.columns(2)
        with col_ask:
            ask_button = st.button("🔍 Search & Answer", use_container_width=True)
        with col_clear:
            clear_button = st.button("🗑️ Clear", use_container_width=True)
        
        if clear_button:
            st.rerun()
    
    with col2:
        st.markdown("## 💡 Examples")
        examples = ["What is the main topic?", "Explain methodology", "Key findings?"]
        for example in examples:
            if st.button(example, use_container_width=True):
                query = example
                ask_button = True
    
    # Process query
    if ask_button and query:
        with st.spinner("⏳ Retrieving documents..."):
            context = retrieve_documents(
                query,
                rag_status['collection'],
                rag_status['embedder'],
                n_results
            )
        
        if not context:
            st.warning("No relevant documents found.")
        else:
            with st.spinner("🤖 Generating answer..."):
                answer = generate_answer(
                    query,
                    context,
                    rag_status['ollama'],
                    st.session_state.model
                )
            
            save_to_history(query, answer, context, st.session_state.model)
            
            st.markdown("---")
            st.markdown("## 📝 Answer")
            st.markdown(f'<div class="answer-box">{answer}</div>', unsafe_allow_html=True)
            
            st.markdown("## 📚 Sources")
            for i, source in enumerate(context, 1):
                icon = "🟢" if source['relevance'] > 0.7 else "🟡"
                with st.expander(f"{icon} {source['source']} (Relevance: {source['relevance']:.0%})"):
                    st.write(source['content'][:300] + "...")

st.markdown("---")
st.markdown("<div style='text-align: center; color: gray; font-size: 12px;'>Research Paper RAG | Keep Ollama running</div>", unsafe_allow_html=True)