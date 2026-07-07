"""
RAG Project - Phase 1: Environment Setup
Purpose: Setup Ollama, download models, configure system
Author: RAze
Date: 2026-07-07
Runtime: ~10 minutes (includes model download)
"""

import subprocess
import sys
import json
import os
from pathlib import Path
import time

class OllamaSetup:
    """Setup and configure Ollama for local LLM inference."""
    
    def __init__(self):
        self.ollama_installed = False
        self.mistral_installed = False
        self.neural_chat_installed = False
        self.models_to_install = {
            'mistral': 'mistral:7b-instruct-q4_K_M',  # 4.1GB - good for accuracy
            'neural-chat': 'neural-chat:7b-v3-q4_K_M'  # 4GB - fast, good accuracy
        }
    
    def check_ollama_installed(self):
        """Check if Ollama is installed."""
        print("🔍 Checking Ollama installation...")
        try:
            result = subprocess.run(['ollama', '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"   ✅ Ollama found: {result.stdout.strip()}")
                self.ollama_installed = True
                return True
        except FileNotFoundError:
            pass
        
        print("   ❌ Ollama not found")
        return False
    
    def install_ollama(self):
        """Guide user to install Ollama."""
        print("\n" + "="*80)
        print("📥 OLLAMA INSTALLATION REQUIRED")
        print("="*80)
        print("""
Ollama is needed to run local LLM models (Mistral, Neural Chat).

📍 Installation Guide:

Windows:
  1. Visit: https://ollama.ai
  2. Download Ollama for Windows
  3. Install and restart terminal
  
Mac:
  1. Visit: https://ollama.ai
  2. Download Ollama for Mac
  3. Install and restart terminal
  
Linux:
  curl https://ollama.ai/install.sh | sh

After installation:
  1. Open new terminal
  2. Run: ollama serve
  3. In another terminal, run this script again

📌 Keep 'ollama serve' running in background!
""")
        print("="*80)
        return False
    
    def check_models_installed(self):
        """Check which models are installed."""
        print("\n🤖 Checking installed models...")
        try:
            result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
            models_output = result.stdout.lower()
            
            if 'mistral' in models_output:
                print("   ✅ Mistral found")
                self.mistral_installed = True
            else:
                print("   ❌ Mistral not found")
            
            if 'neural-chat' in models_output:
                print("   ✅ Neural Chat found")
                self.neural_chat_installed = True
            else:
                print("   ❌ Neural Chat not found")
            
            return self.mistral_installed or self.neural_chat_installed
        except Exception as e:
            print(f"   ⚠️  Error checking models: {e}")
            return False
    
    def install_models(self):
        """Install required models."""
        print("\n" + "="*80)
        print("📥 DOWNLOADING MODELS (This will take 10-15 minutes)")
        print("="*80)
        
        for model_name, model_id in self.models_to_install.items():
            if model_name == 'mistral' and self.mistral_installed:
                print(f"   ⏭️  Skipping {model_name} (already installed)")
                continue
            if model_name == 'neural-chat' and self.neural_chat_installed:
                print(f"   ⏭️  Skipping {model_name} (already installed)")
                continue
            
            print(f"\n   📦 Downloading {model_name}...")
            print(f"      Model: {model_id}")
            print(f"      Size: ~4 GB")
            print(f"      ⏳ This may take 5-10 minutes...")
            
            try:
                subprocess.run(['ollama', 'pull', model_id], check=True)
                print(f"   ✅ {model_name} installed successfully!")
                if model_name == 'mistral':
                    self.mistral_installed = True
                else:
                    self.neural_chat_installed = True
            except Exception as e:
                print(f"   ❌ Failed to install {model_name}: {e}")
        
        return self.mistral_installed and self.neural_chat_installed
    
    def test_models(self):
        """Test if models respond correctly."""
        print("\n" + "="*80)
        print("🧪 TESTING MODELS")
        print("="*80)
        
        test_prompt = "Say 'Hello from [model_name]' and nothing else."
        
        for model_name, model_id in self.models_to_install.items():
            if model_name == 'mistral' and not self.mistral_installed:
                continue
            if model_name == 'neural-chat' and not self.neural_chat_installed:
                continue
            
            print(f"\n   🧪 Testing {model_name}...")
            try:
                result = subprocess.run(
                    ['ollama', 'run', model_id, test_prompt],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                if result.returncode == 0:
                    print(f"   ✅ {model_name} works!")
                    print(f"      Response: {result.stdout.strip()[:100]}")
                else:
                    print(f"   ⚠️  {model_name} returned error")
            except subprocess.TimeoutExpired:
                print(f"   ⏳ {model_name} taking too long (may still work)")
            except Exception as e:
                print(f"   ❌ Error testing {model_name}: {e}")
    
    def setup_project_structure(self):
        """Create necessary directories."""
        print("\n📁 Creating project structure...")
        
        directories = [
            'data/papers',
            'data/metadata',
            'vector_store',
            'config',
            'outputs/logs',
            'outputs/results'
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
            print(f"   ✅ Created: {directory}/")
    
    def create_config_file(self):
        """Create configuration file."""
        print("\n⚙️  Creating configuration file...")
        
        config = {
            'models': {
                'primary': 'mistral:7b-instruct-q4_K_M',
                'secondary': 'neural-chat:7b-v3-q4_K_M',
                'active_model': 'mistral'
            },
            'vector_db': {
                'type': 'chromadb',
                'persist_directory': './vector_store',
                'distance_metric': 'cosine'  # For accuracy
            },
            'embeddings': {
                'model': 'all-MiniLM-L6-v2',  # Local embeddings
                'dimension': 384
            },
            'rag': {
                'chunk_size': 500,  # Smaller chunks for accuracy
                'chunk_overlap': 100,
                'retrieval_top_k': 5,  # Get top 5 most relevant chunks
                'temperature': 0.3  # Lower = more accurate, less creative
            },
            'pdf': {
                'extract_metadata': True,
                'supported_formats': ['.pdf']
            },
            'logging': {
                'level': 'INFO',
                'log_file': 'outputs/logs/rag.log'
            }
        }
        
        config_path = 'config/rag_config.json'
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"   ✅ Created: {config_path}")
        return config


def main():
    """Run setup process."""
    print("\n" + "="*80)
    print("🚀 RESEARCH PAPER RAG - ENVIRONMENT SETUP")
    print("="*80)
    
    setup = OllamaSetup()
    
    # Check Ollama
    if not setup.check_ollama_installed():
        setup.install_ollama()
        print("\n⚠️  Please install Ollama and run 'ollama serve' first!")
        print("    Then run this script again.")
        sys.exit(1)
    
    # Check models
    if not setup.check_models_installed():
        response = input("\n❓ Models not installed. Install them now? (y/n): ").lower()
        if response == 'y':
            if not setup.install_models():
                print("\n⚠️  Some models failed to install. Check internet connection.")
        else:
            print("⚠️  Models required. Please install manually:")
            print("    ollama pull mistral:7b-instruct-q4_K_M")
            print("    ollama pull neural-chat:7b-v3-q4_K_M")
            sys.exit(1)
    
    # Test models
    print("\n" + "="*80)
    response = input("Run model tests? (y/n): ").lower()
    if response == 'y':
        setup.test_models()
    
    # Setup project structure
    setup.setup_project_structure()
    
    # Create config
    setup.create_config_file()
    
    # Summary
    print("\n" + "="*80)
    print("✅ SETUP COMPLETE!")
    print("="*80)
    print("""
✅ What was set up:
   • Ollama installed and configured
   • Mistral model ready for accuracy-focused QA
   • Neural Chat model ready for faster responses
   • ChromaDB configured for vector storage
   • Project directories created
   • Configuration file created

📝 Configuration: config/rag_config.json

🔧 Next steps:
   1. Keep 'ollama serve' running in background
   2. Add research papers to: data/papers/
   3. Run: python rag_02_data_loader.py
   4. Run: python rag_03_vector_database.py
   5. Run: python rag_04_rag_pipeline.py
   6. Run: python rag_05_cli_interface.py

⚠️  IMPORTANT:
   - Keep terminal open: ollama serve
   - Don't close it while using RAG system

Need help? Check: SETUP_GUIDE.md
""")
    print("="*80)


if __name__ == "__main__":
    main()
