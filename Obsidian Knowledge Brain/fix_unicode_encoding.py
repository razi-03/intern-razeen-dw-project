#!/usr/bin/env python3
"""
Fix Unicode encoding issues in all scripts
Adds explicit UTF-8 encoding to json.load() calls
"""

import re
from pathlib import Path

def fix_unicode_encoding():
    """Add UTF-8 encoding to all JSON file operations"""
    
    scripts = [
        "obsidian_03_vector_store.py",
        "obsidian_04_link_suggester.py",
        "obsidian_05_knowledge_graph.py",
        "obsidian_06_insights_generator.py",
        "obsidian_07_streamlit_ui.py",
    ]
    
    fixes_made = 0
    
    for script_name in scripts:
        script_path = Path(script_name)
        
        if not script_path.exists():
            print(f"⚠️  {script_name} not found")
            continue
        
        print(f"📝 Fixing {script_name}...")
        
        with open(script_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Fix json.load calls - add encoding='utf-8'
        patterns = [
            # json.load(f) -> json.load(f, encoding='utf-8') [doesn't work, need to fix open instead]
            # Better: fix open() calls to have encoding='utf-8'
            (r"open\(([^,]+),\s*['\"]r['\"]\)", r"open(\1, 'r', encoding='utf-8')"),
            (r"open\(([^,]+),\s*['\"]w['\"]\)", r"open(\1, 'w', encoding='utf-8')"),
        ]
        
        for old_pattern, new_pattern in patterns:
            if re.search(old_pattern, content):
                content = re.sub(old_pattern, new_pattern, content)
                fixes_made += 1
                print(f"   ✅ Fixed encoding issues")
        
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    print("\n" + "="*60)
    print(f"✅ Fixed encoding in {fixes_made} locations!")
    print("="*60)
    print("\nNow re-run the scripts:")
    print("  python obsidian_01_vault_scanner.py")
    print("  python obsidian_02_note_parser.py")
    print("  python obsidian_03_vector_store.py")
    print("  ... etc")

if __name__ == "__main__":
    fix_unicode_encoding()
