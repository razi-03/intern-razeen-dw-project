#!/usr/bin/env python3
"""
Smart deduplicator - renames notes with duplicate titles to make them unique
"""

import json
from pathlib import Path
from collections import defaultdict

def deduplicate_notes():
    """Remove duplicates from enriched_notes.json by keeping unique ones"""
    
    notes_path = Path("data/enriched_notes.json")
    
    if not notes_path.exists():
        print(f"❌ {notes_path} not found!")
        return False
    
    print("📝 Loading enriched notes...")
    with open(notes_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Get notes (handle list format)
    if isinstance(data, list):
        notes = data
    elif isinstance(data, dict) and 'notes' in data:
        notes = data['notes']
    else:
        notes = list(data.values()) if isinstance(data, dict) else []
    
    print(f"📊 Found {len(notes)} total notes")
    
    # Group by title to find duplicates
    title_groups = defaultdict(list)
    for idx, note in enumerate(notes):
        title = note.get('title', f'note_{idx}')
        title_groups[title].append(idx)
    
    # Find duplicates
    duplicates = {title: indices for title, indices in title_groups.items() if len(indices) > 1}
    
    if not duplicates:
        print("✅ No duplicates found! All titles are unique.")
        return True
    
    print(f"\n⚠️  Found {len(duplicates)} duplicate titles:\n")
    
    # Remove duplicates by keeping only first occurrence
    indices_to_keep = set()
    for title, indices in title_groups.items():
        # Keep only the first occurrence
        indices_to_keep.add(indices[0])
        if len(indices) > 1:
            print(f"   '{title}' appears {len(indices)} times")
            print(f"      Keeping: index {indices[0]}")
            print(f"      Removing: indices {indices[1:]}")
    
    # Keep only unique notes
    deduplicated = [notes[i] for i in sorted(indices_to_keep)]
    
    print(f"\n📊 Kept {len(deduplicated)} unique notes (removed {len(notes) - len(deduplicated)} duplicates)")
    
    # Save deduplicated notes
    print("\n💾 Saving deduplicated notes...")
    
    if isinstance(data, list):
        output = deduplicated
    elif isinstance(data, dict) and 'notes' in data:
        output = {'notes': deduplicated}
    else:
        output = deduplicated
    
    with open(notes_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Saved {len(deduplicated)} unique notes to enriched_notes.json\n")
    return True

if __name__ == "__main__":
    if deduplicate_notes():
        print("="*60)
        print("Next steps:")
        print("  1. Delete vector store:")
        print("     Remove-Item -Recurse -Force vector_store")
        print()
        print("  2. Re-run script 3:")
        print("     python obsidian_03_vector_store.py")
        print()
        print("  3. Continue with scripts 4-7")
        print("="*60)
