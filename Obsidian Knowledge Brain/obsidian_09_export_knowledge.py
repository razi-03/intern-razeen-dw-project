"""
Obsidian AI Brain - Phase 9: Export Knowledge (FIXED)
Purpose: Export notes as searchable website
Author: RAze
Date: 2026-07-08
Fix: Added content_preview field to avoid AttributeError in HTML generation
"""

import json
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_html_page(notes, insights, graph_data):
    """Generate static HTML website."""
    
    # Calculate statistics
    total_notes = len(notes)
    total_words = sum(n.get('readability', {}).get('total_words', 0) for n in notes)
    total_edges = graph_data.get('stats', {}).get('total_edges', 0)
    
    # Get insights text
    insights_text = insights.get('vault_insights', 'Insights available after analysis')
    
    # Get top topics
    top_topics = insights.get('top_topics', [])
    topics_html = ""
    if top_topics:
        topics_html = "<div class='topics-section'><h3>🏷️ Top Topics</h3><div class='topic-tags'>"
        for topic in top_topics[:8]:
            topic_name = topic.get('name', 'Unknown') if isinstance(topic, dict) else topic
            topic_freq = topic.get('frequency', 0) if isinstance(topic, dict) else 0
            topics_html += f"<span class='topic-tag'>{topic_name} <small>({topic_freq})</small></span>"
        topics_html += "</div></div>"
    
    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🧠 My Knowledge Brain</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f5f5f5; color: #333; }}
        header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 2rem; text-align: center; }}
        header h1 {{ font-size: 2.5rem; margin-bottom: 0.5rem; }}
        header p {{ font-size: 1.1rem; opacity: 0.9; }}
        .container {{ max-width: 1200px; margin: 2rem auto; padding: 0 1rem; }}
        
        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin: 2rem 0; }}
        .stat-card {{ background: white; padding: 1.5rem; border-radius: 0.5rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center; transition: transform 0.2s; }}
        .stat-card:hover {{ transform: translateY(-2px); box-shadow: 0 4px 8px rgba(0,0,0,0.15); }}
        .stat-card h3 {{ color: #667eea; font-size: 2rem; margin: 0.5rem 0; }}
        .stat-card p {{ color: #666; }}
        
        .insights {{ background: white; padding: 2rem; border-radius: 0.5rem; margin: 2rem 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .insights h2 {{ color: #667eea; margin-bottom: 1rem; }}
        .insights p {{ line-height: 1.8; color: #444; }}
        
        .topics-section {{ margin-top: 1.5rem; }}
        .topics-section h3 {{ color: #667eea; margin-bottom: 1rem; }}
        .topic-tags {{ display: flex; flex-wrap: wrap; gap: 0.5rem; }}
        .topic-tag {{ background: #f0f0f0; color: #333; padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.9rem; border-left: 3px solid #667eea; }}
        .topic-tag small {{ color: #999; margin-left: 0.3rem; }}
        
        .section-title {{ color: #333; margin: 2rem 0 1rem 0; font-size: 1.5rem; }}
        
        .note-list {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 1.5rem; margin: 2rem 0; }}
        .note-card {{ background: white; padding: 1.5rem; border-radius: 0.5rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1); transition: transform 0.2s; border-left: 4px solid #667eea; }}
        .note-card:hover {{ transform: translateY(-2px); box-shadow: 0 4px 8px rgba(0,0,0,0.15); }}
        .note-card h3 {{ color: #667eea; margin-bottom: 0.5rem; font-size: 1.1rem; }}
        .note-card p.content {{ color: #666; line-height: 1.6; margin: 1rem 0; }}
        .note-card p.meta {{ font-size: 0.9rem; color: #999; margin-top: 1rem; }}
        
        footer {{ background: #333; color: white; padding: 1rem; text-align: center; margin-top: 2rem; }}
        footer p {{ font-size: 0.9rem; }}
    </style>
</head>
<body>
    <header>
        <h1>🧠 My Knowledge Brain</h1>
        <p>AI-enhanced personal knowledge management system</p>
    </header>
    
    <div class="container">
        <!-- Stats -->
        <div class="stats">
            <div class="stat-card">
                <h3>{total_notes}</h3>
                <p>Total Notes</p>
            </div>
            <div class="stat-card">
                <h3>{total_words:,}</h3>
                <p>Total Words</p>
            </div>
            <div class="stat-card">
                <h3>{total_edges}</h3>
                <p>Note Connections</p>
            </div>
            <div class="stat-card">
                <h3>{len(top_topics)}</h3>
                <p>Key Topics</p>
            </div>
        </div>
        
        <!-- Insights -->
        <div class="insights">
            <h2>💡 Key Insights from Your Vault</h2>
            <p>{insights_text}</p>
            {topics_html}
        </div>
        
        <!-- Notes Section -->
        <h2 class="section-title">📚 Your Notes</h2>
        <div class="note-list">
"""
    
    # Add note cards (max 20 displayed)
    for note in notes[:20]:
        # ✅ FIXED: Use content_preview if available, otherwise generate it
        if 'content_preview' in note:
            preview = note['content_preview']
        else:
            content = note.get('content', '')
            preview = content[:250] + "..." if len(content) > 250 else content
        
        # Get word count
        word_count = note.get('readability', {}).get('total_words', 0)
        folder = note.get('file_metadata', {}).get('folder', 'Root')
        tags = note.get('tags', [])
        
        tags_str = ', '.join(tags[:3]) if tags else 'no tags'
        
        html += f"""            <div class="note-card">
                <h3>{note.get('title', 'Untitled')}</h3>
                <p class="content">{preview}</p>
                <p class="meta">
                    📁 {folder} • 📝 {word_count} words
                    {f'• 🏷️ {tags_str}' if tags else ''}
                </p>
            </div>
"""
    
    html += """        </div>
    </div>
    
    <footer>
        <p>Generated by Obsidian AI Brain</p>
        <p>Open in browser to explore your knowledge network</p>
    </footer>
</body>
</html>
"""
    
    return html


def add_content_previews(notes):
    """Add content_preview field to all notes if missing."""
    for note in notes:
        if 'content_preview' not in note:
            content = note.get('content', '')
            # Generate 250-character preview
            preview = content[:250]
            if len(content) > 250:
                # Try to break at word boundary
                last_space = preview.rfind(' ')
                if last_space > 100:
                    preview = preview[:last_space]
                preview += "..."
            note['content_preview'] = preview
    
    return notes


def main():
    """Export knowledge."""
    print("\n" + "="*80)
    print("📤 OBSIDIAN AI BRAIN - EXPORT KNOWLEDGE")
    print("="*80)
    
    # Load data
    try:
        # Load enriched notes
        with open('data/enriched_notes.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, list):
                notes = data
            elif isinstance(data, dict) and 'notes' in data:
                notes = data['notes']
            else:
                notes = list(data.values()) if isinstance(data, dict) else []
        
        # Load insights
        with open('data/insights.json', 'r', encoding='utf-8') as f:
            insights = json.load(f)
        
        # Load graph
        with open('data/graph_data.json', 'r', encoding='utf-8') as f:
            graph_data = json.load(f)
        
    except FileNotFoundError as e:
        print(f"⚠️  Missing file: {e}")
        print("   Run all phases before export")
        return
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return
    
    if not notes:
        print("⚠️  No notes found")
        return
    
    print(f"\n   ✅ Loaded {len(notes)} notes")
    print(f"   ✅ Loaded insights")
    print(f"   ✅ Loaded graph data ({graph_data.get('stats', {}).get('total_edges', 0)} connections)")
    
    # ✅ FIXED: Add content previews
    print(f"\n📄 Processing notes...")
    notes = add_content_previews(notes)
    logger.info(f"   ✅ Added content previews to all notes")
    
    # Generate HTML
    logger.info("📄 Generating HTML website...")
    html = generate_html_page(notes, insights, graph_data)
    
    # Save
    output_dir = Path('exports')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    index_file = output_dir / 'index.html'
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    logger.info(f"✅ Saved to {index_file}")
    
    print(f"\n✅ EXPORT COMPLETE!")
    print(f"   Website: {index_file}")
    print(f"   Notes exported: {len(notes)}")
    print(f"   Open index.html in your browser to view")
    print("="*80)


if __name__ == "__main__":
    main()