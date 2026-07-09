#!/usr/bin/env python3
"""
Smart fixer for enriched_notes.json - handles various structures
"""

import json
from pathlib import Path

def fix_enriched_notes_smart():
    """Fix enriched notes with flexible structure handling"""
    
    notes_path = Path("data/enriched_notes.json")
    
    if not notes_path.exists():
        print(f"❌ {notes_path} not found!")
        return False
    
    print("📝 Loading enriched notes...")
    with open(notes_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print("🔧 Analyzing structure...")
    
    # Handle different structures
    if isinstance(data, dict):
        # Structure: {note_id: {fields...}, ...}
        print("   Found dict structure")
        
        for note_id, note in data.items():
            if isinstance(note, dict):
                # Add content_preview if missing
                if 'content_preview' not in note:
                    content = note.get('content', '')
                    if isinstance(content, str):
                        preview = content[:200] + "..." if len(content) > 200 else content
                    else:
                        preview = "No preview available"
                    note['content_preview'] = preview
                    print(f"   ✅ Fixed {note_id}")
            elif isinstance(note, list):
                # Skip lists (like metadata)
                print(f"   ⏭️  Skipping {note_id} (list type)")
                continue
    
    print("💾 Saving updated notes...")
    with open(notes_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    
    print("✅ Fixed enriched_notes.json!")
    return True

if __name__ == "__main__":
    try:
        fix_enriched_notes_smart()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
