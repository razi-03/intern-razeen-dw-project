#!/usr/bin/env python3
"""
Fix ChromaDB compatibility in ALL scripts at once
Patches scripts 4, 5, 6, 7 to use new ChromaDB API
"""

import re
from pathlib import Path

def fix_all_chromadb_scripts():
    """Fix ChromaDB in all scripts"""
    
    scripts_to_fix = [
        "obsidian_04_link_suggester.py",
        "obsidian_05_knowledge_graph.py",
        "obsidian_06_insights_generator.py",
        "obsidian_07_streamlit_ui.py",
    ]
    
    fixed_count = 0
    
    for script_name in scripts_to_fix:
        script_path = Path(script_name)
        
        if not script_path.exists():
            print(f"⚠️  {script_name} not found (skipping)")
            continue
        
        print(f"\n📝 Fixing {script_name}...")
        
        try:
            with open(script_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Fix 1: Remove SettingsOverride import
            content = re.sub(
                r"from chromadb\.config import SettingsOverride\n",
                "",
                content
            )
            
            # Fix 2: Replace chromadb.Client(settings) with PersistentClient
            # Pattern 1: With settings variable
            content = re.sub(
                r"settings = SettingsOverride\(\s*[^)]*\)\s*self\.client = chromadb\.Client\(settings\)",
                "self.client = chromadb.PersistentClient(path=\"vector_store\")",
                content,
                flags=re.DOTALL
            )
            
            # Pattern 2: Direct Client call
            content = re.sub(
                r"self\.client = chromadb\.Client\(settings\)",
                "self.client = chromadb.PersistentClient(path=\"vector_store\")",
                content
            )
            
            # Fix 3: Remove or comment out persist() calls
            content = re.sub(
                r"(\s+)self\.client\.persist\(\)",
                r"\1# self.client.persist()  # Auto-persisted by PersistentClient",
                content
            )
            
            # Fix 4: Remove settings definition blocks
            content = re.sub(
                r"(\s+)settings = SettingsOverride\(\s*chroma_db_impl[^)]*\)\n",
                "",
                content
            )
            
            # Check if we made changes
            if content != original_content:
                with open(script_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"   ✅ Fixed {script_name}")
                fixed_count += 1
            else:
                print(f"   ℹ️  {script_name} already uses new API")
        
        except Exception as e:
            print(f"   ❌ Error fixing {script_name}: {e}")
    
    print("\n" + "="*60)
    print(f"✅ Fixed {fixed_count} scripts!")
    print("="*60)
    print("\nReady to run:")
    print("  python obsidian_04_link_suggester.py")
    print("  python obsidian_05_knowledge_graph.py")
    print("  python obsidian_06_insights_generator.py")
    print("  streamlit run obsidian_07_streamlit_ui.py")
    print()

if __name__ == "__main__":
    fix_all_chromadb_scripts()
