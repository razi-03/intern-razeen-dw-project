#!/usr/bin/env python3
"""
Fix enriched_notes.json by adding missing content_preview field
"""

import json
from pathlib import Path

def fix_enriched_notes():
    """Add content_preview to all notes"""
    
    notes_path = Path("data/enriched_notes.json")
    
    if not notes_path.exists():
        print(f"❌ {notes_path} not found!")
        return False
    
    print("📝 Loading enriched notes...")
    with open(notes_path, 'r', encoding='utf-8') as f:
        enriched_notes = json.load(f)
    
    print("🔧 Adding content_preview field...")
    
    # Add content_preview to each note
    for note_id, note in enriched_notes.items():
        if 'content_preview' not in note:
            # Create preview from content (first 200 chars)
            content = note.get('content', '')
            preview = content[:200] + "..." if len(content) > 200 else content
            note['content_preview'] = preview
            print(f"   ✅ Added preview for {note_id}")
    
    print("💾 Saving updated notes...")
    with open(notes_path, 'w', encoding='utf-8') as f:
        json.dump(enriched_notes, f, indent=2)
    
    print(f"✅ Fixed {notes_path}!")
    return True

if __name__ == "__main__":
    fix_enriched_notes()
