"""
RAG Project - Phase 5: CLI Interface
Purpose: Interactive command-line interface for RAG queries
Author: RAze
Date: 2026-07-07
Runtime: Interactive
"""

import json
from pathlib import Path
import sys
from datetime import datetime
import logging
from rag_04_rag_pipeline import OllamaModelManager, RAGPipeline

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class RAGCLIInterface:
    """Command-line interface for RAG system."""
    
    def __init__(self):
        self.rag = None
        self.model_manager = None
        self.query_history = []
        self.commands = {
            'help': 'Show this help menu',
            'models': 'List available models',
            'switch': 'Switch to a different model',
            'summarize': 'Summarize loaded papers',
            'history': 'Show query history',
            'save': 'Save query history',
            'clear': 'Clear query history',
            'exit': 'Exit the program'
        }
    
    def initialize(self):
        """Initialize RAG pipeline."""
        print("\n" + "="*80)
        print("🚀 RESEARCH PAPER RAG - CLI INTERFACE")
        print("="*80)
        
        # Initialize model manager
        try:
            logger.info("🤖 Initializing Ollama models...")
            self.model_manager = OllamaModelManager()
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("\n⚠️  Make sure:")
            print("   1. Ollama is running: ollama serve")
            print("   2. Models are downloaded")
            return False
        
        # Initialize RAG pipeline
        try:
            logger.info("📂 Initializing RAG pipeline...")
            self.rag = RAGPipeline(self.model_manager)
            print("\n✅ System ready!")
            return True
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("\n⚠️  Vector database not found. Run Phase 3 first:")
            print("   python rag_03_vector_database.py")
            return False
    
    def show_banner(self):
        """Show welcome banner."""
        print("\n" + "="*80)
        print("📚 RESEARCH PAPER RAG - INTERACTIVE QUERY SYSTEM")
        print("="*80)
        print(f"""
Active Model: {self.model_manager.get_active_model()}

Commands:
  ? or help     - Show commands
  models        - List available models
  switch        - Switch to different model
  summarize     - Summarize papers
  history       - Show query history
  save          - Save query history
  clear         - Clear history
  exit          - Exit

Just type your question and press Enter!
(Questions with 'help', 'models', 'switch', etc. trigger commands)

Type 'help' for more information.
""")
        print("="*80)
    
    def show_help(self):
        """Show help menu."""
        print("\n" + "="*80)
        print("📖 COMMAND HELP")
        print("="*80)
        print("\nCommands:")
        for cmd, desc in self.commands.items():
            print(f"  {cmd:<12} - {desc}")
        
        print("\nUsage:")
        print("  • Questions: Just type naturally (e.g., 'What are the main findings?')")
        print("  • Commands: Type command name (e.g., 'models' or 'switch')")
        print("  • Exit: Type 'exit' or press Ctrl+C")
        print("\nTips:")
        print("  • Ask specific questions for best results")
        print("  • Use 'switch' to try different models")
        print("  • Model accuracy > speed (Mistral preferred)")
        print("="*80)
    
    def show_models(self):
        """Show available models."""
        print("\n" + "="*80)
        print("🤖 AVAILABLE MODELS")
        print("="*80)
        
        models = self.model_manager.get_available_models()
        active = self.model_manager.get_active_model()
        
        for model, desc in models.items():
            status = "✅ ACTIVE" if model == active else "○ Available"
            print(f"\n  {model.upper()}")
            print(f"    {desc}")
            print(f"    Status: {status}")
        
        print("\n  Type 'switch' to change model")
        print("="*80)
    
    def switch_model(self):
        """Switch active model."""
        print("\n" + "="*80)
        print("🔄 SWITCH MODEL")
        print("="*80)
        
        models = list(self.model_manager.get_available_models().keys())
        
        print("\nAvailable models:")
        for i, model in enumerate(models, 1):
            print(f"  [{i}] {model}")
        
        try:
            choice = input("\nSelect model (number): ").strip()
            choice_idx = int(choice) - 1
            
            if 0 <= choice_idx < len(models):
                new_model = models[choice_idx]
                if self.model_manager.switch_model(new_model):
                    print(f"\n✅ Switched to {new_model}")
                else:
                    print(f"\n❌ Failed to switch to {new_model}")
            else:
                print("\n⚠️  Invalid choice")
        except ValueError:
            print("\n⚠️  Please enter a number")
        except Exception as e:
            print(f"\n❌ Error: {e}")
        
        print("="*80)
    
    def handle_question(self, question):
        """Process and answer a question."""
        result = self.rag.answer_question(question)
        
        if result:
            self.query_history.append(result)
            
            # Ask if user wants to continue
            print("\n" + "-"*80)
            response = input("\nWould you like to ask another question? (y/n): ").strip().lower()
            if response != 'y':
                print("Exiting...")
                return False
        
        return True
    
    def show_history(self):
        """Show query history."""
        if not self.query_history:
            print("\n⚠️  No queries in history")
            return
        
        print("\n" + "="*80)
        print("📋 QUERY HISTORY")
        print("="*80)
        
        for i, result in enumerate(self.query_history, 1):
            print(f"\n[{i}] {result['timestamp']}")
            print(f"   Model: {result['model']}")
            print(f"   Q: {result['question'][:80]}...")
            print(f"   A: {result['answer'][:100]}...")
        
        print("\n" + "="*80)
    
    def save_history(self):
        """Save query history to file."""
        if not self.query_history:
            print("\n⚠️  No queries to save")
            return
        
        output_dir = Path('outputs/results')
        output_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = output_dir / f"query_history_{timestamp}.json"
        
        try:
            with open(output_file, 'w') as f:
                json.dump({
                    'saved_at': datetime.now().isoformat(),
                    'total_queries': len(self.query_history),
                    'queries': self.query_history
                }, f, indent=2)
            
            print(f"\n✅ Saved {len(self.query_history)} queries to {output_file}")
        except Exception as e:
            print(f"\n❌ Error saving: {e}")
    
    def clear_history(self):
        """Clear query history."""
        response = input(f"\n⚠️  Clear {len(self.query_history)} queries? (y/n): ").strip().lower()
        if response == 'y':
            self.query_history = []
            print("✅ History cleared")
        else:
            print("Cancelled")
    
    def run_interactive(self):
        """Run interactive mode."""
        self.show_banner()
        
        while True:
            try:
                print(f"\n[{self.model_manager.get_active_model()}] ", end='')
                user_input = input("Your question (or command): ").strip()
                
                if not user_input:
                    continue
                
                # Check for commands
                lower_input = user_input.lower()
                
                if lower_input in ['?', 'help']:
                    self.show_help()
                
                elif lower_input == 'models':
                    self.show_models()
                
                elif lower_input == 'switch':
                    self.switch_model()
                
                elif lower_input == 'summarize':
                    self.rag.summarize_papers()
                
                elif lower_input == 'history':
                    self.show_history()
                
                elif lower_input == 'save':
                    self.save_history()
                
                elif lower_input == 'clear':
                    self.clear_history()
                
                elif lower_input == 'exit':
                    print("\n👋 Goodbye!")
                    break
                
                else:
                    # Regular question
                    if not self.handle_question(user_input):
                        break
            
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                logger.error(f"Error: {e}")
                print(f"\n❌ Error: {e}")


def main():
    """Main entry point."""
    cli = RAGCLIInterface()
    
    # Initialize
    if not cli.initialize():
        sys.exit(1)
    
    # Run interactive mode
    try:
        cli.run_interactive()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)


if __name__ == "__main__":
    main()
