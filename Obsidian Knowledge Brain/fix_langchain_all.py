#!/usr/bin/env python3
"""
Comprehensive LangChain 1.0+ import migration fixer
Fixes all old imports to new locations
"""

import re
from pathlib import Path

def fix_all_langchain_imports():
    """Fix all LangChain import compatibility issues"""
    
    scripts_to_fix = [
        "obsidian_06_insights_generator.py",
        "obsidian_07_streamlit_ui.py",
    ]
    
    # Comprehensive list of import migrations for LangChain 1.0+
    import_fixes = [
        # langchain.prompts -> langchain_core.prompts
        (r"from langchain\.prompts import", "from langchain_core.prompts import"),
        (r"from langchain\.prompts\.", "from langchain_core.prompts."),
        
        # langchain.schema -> langchain_core
        (r"from langchain\.schema import", "from langchain_core.messages import"),
        (r"from langchain\.schema\.", "from langchain_core.messages."),
        
        # langchain.output_parsers -> langchain_core.output_parsers
        (r"from langchain\.output_parsers import", "from langchain_core.output_parsers import"),
        
        # langchain.agents -> langchain
        (r"from langchain\.agents import", "from langchain import agents; from langchain.agents import"),
        
        # langchain.chains -> langchain
        (r"from langchain\.chains import", "from langchain.chains import"),
        
        # langchain.memory -> langchain
        (r"from langchain\.memory import", "from langchain.memory import"),
        
        # langchain.chat_models -> langchain_community.chat_models (already fixed)
        (r"from langchain\.chat_models import", "from langchain_community.chat_models import"),
        
        # langchain.llms -> langchain_community.llms (already fixed)
        (r"from langchain\.llms import", "from langchain_community.llms import"),
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
            
            # Apply all import fixes
            changes_made = 0
            for old_pattern, new_pattern in import_fixes:
                if re.search(old_pattern, content):
                    content = re.sub(old_pattern, new_pattern, content)
                    changes_made += 1
                    print(f"   ✅ Migrated import")
            
            # Additional fix: Handle specific common patterns
            # Fix: from langchain.prompts import PromptTemplate
            # Sometimes it's also in langchain.core.prompts
            if "from langchain.prompts import" in content and "langchain_core.prompts" not in content:
                content = content.replace(
                    "from langchain.prompts import",
                    "from langchain_core.prompts import"
                )
            
            # Check if we made changes
            if content != original_content:
                with open(script_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"   ✅ Updated {script_name} ({changes_made} imports fixed)")
                fixed_count += 1
            else:
                print(f"   ℹ️  {script_name} already uses new imports")
        
        except Exception as e:
            print(f"   ❌ Error fixing {script_name}: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*60)
    print(f"✅ Fixed {fixed_count} scripts!")
    print("="*60)
    print("\nReady to run:")
    print("  python obsidian_06_insights_generator.py")
    print("  streamlit run obsidian_07_streamlit_ui.py")
    print()

if __name__ == "__main__":
    fix_all_langchain_imports()
