#!/usr/bin/env python3
"""
Fix LangChain compatibility issues in all scripts
Updates old langchain.llms imports to new langchain_community imports
"""

import re
from pathlib import Path

def fix_langchain_imports():
    """Fix LangChain import issues in all scripts"""
    
    scripts_to_check = [
        "obsidian_06_insights_generator.py",
        "obsidian_07_streamlit_ui.py",
    ]
    
    # Old import patterns and their replacements
    fixes = [
        # Old: from langchain.llms.ollama import Ollama
        # New: from langchain_community.llms import Ollama
        (
            r"from langchain\.llms\.ollama import Ollama",
            "from langchain_community.llms import Ollama"
        ),
        # Old: from langchain.llms import Ollama
        # New: from langchain_community.llms import Ollama
        (
            r"from langchain\.llms import Ollama",
            "from langchain_community.llms import Ollama"
        ),
        # Old: from langchain.chat_models import ChatOllama
        # New: from langchain_community.chat_models import ChatOllama
        (
            r"from langchain\.chat_models import ChatOllama",
            "from langchain_community.chat_models import ChatOllama"
        ),
        # Old: from langchain.embeddings import HuggingFaceEmbeddings
        # New: from langchain_community.embeddings import HuggingFaceEmbeddings
        (
            r"from langchain\.embeddings import HuggingFaceEmbeddings",
            "from langchain_community.embeddings import HuggingFaceEmbeddings"
        ),
        # Old: from langchain.vectorstores import Chroma
        # New: from langchain_community.vectorstores import Chroma
        (
            r"from langchain\.vectorstores import Chroma",
            "from langchain_community.vectorstores import Chroma"
        ),
    ]
    
    fixed_count = 0
    
    for script_name in scripts_to_check:
        script_path = Path(script_name)
        
        if not script_path.exists():
            print(f"⚠️  {script_name} not found (skipping)")
            continue
        
        print(f"\n📝 Checking {script_name}...")
        
        try:
            with open(script_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Apply all fixes
            for old_pattern, new_pattern in fixes:
                if re.search(old_pattern, content):
                    content = re.sub(old_pattern, new_pattern, content)
                    print(f"   ✅ Fixed: {old_pattern}")
            
            # Check if we made changes
            if content != original_content:
                with open(script_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"   ✅ Updated {script_name}")
                fixed_count += 1
            else:
                print(f"   ℹ️  {script_name} already uses new imports")
        
        except Exception as e:
            print(f"   ❌ Error fixing {script_name}: {e}")
    
    print("\n" + "="*60)
    print(f"✅ Fixed {fixed_count} scripts!")
    print("="*60)
    print("\nReady to run:")
    print("  python obsidian_06_insights_generator.py")
    print("  streamlit run obsidian_07_streamlit_ui.py")
    print()

if __name__ == "__main__":
    fix_langchain_imports()
