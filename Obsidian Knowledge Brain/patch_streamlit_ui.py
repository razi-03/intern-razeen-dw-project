#!/usr/bin/env python3
"""
Patch obsidian_07_streamlit_ui.py to handle missing content_preview field
"""

from pathlib import Path

def patch_streamlit_ui():
    """Patch the streamlit UI script"""
    
    script_path = Path("obsidian_07_streamlit_ui.py")
    
    if not script_path.exists():
        print(f"❌ {script_path} not found!")
        return False
    
    print("📝 Reading script...")
    with open(script_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("🔧 Patching content_preview access...")
    
    # Replace direct access with .get() method
    old_line = "st.write(f\"**Preview:** {note['content_preview']}\")"
    new_line = "preview = note.get('content_preview', note.get('content', 'No preview available')[:200]); st.write(f\"**Preview:** {preview}\")"
    
    if old_line in content:
        content = content.replace(old_line, new_line)
        print("   ✅ Patched line 161")
    
    # More general fix: replace all note['content_preview'] with note.get('content_preview', ...)
    import re
    content = re.sub(
        r"note\['content_preview'\]",
        "note.get('content_preview', note.get('content', 'No preview')[:200])",
        content
    )
    
    print("💾 Saving patched script...")
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Patched obsidian_07_streamlit_ui.py!")
    return True

if __name__ == "__main__":
    patch_streamlit_ui()
