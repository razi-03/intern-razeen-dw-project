"""
Obsidian AI Brain - Phase 7: Streamlit Web Interface
Purpose: Beautiful dashboard for knowledge brain
Author: RAze
Date: 2026-07-08
"""

import streamlit as st
import json
from pathlib import Path
import networkx as nx
import matplotlib.pyplot as plt

st.set_page_config(page_title="🧠 Obsidian AI Brain", layout="wide", page_icon="🧠")

# CSS
st.markdown("""
<style>
    .metric-card { background-color: #f0f2f6; padding: 1.5rem; border-radius: 0.5rem; }
    .insight-box { background-color: #e8f4f8; color: #000000; padding: 1.5rem; border-radius: 0.5rem; margin: 1rem 0; }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SIDEBAR
# ============================================================================

with st.sidebar:
    st.title("⚙️ Settings")
    st.divider()
    
    # Try to load data
    @st.cache_data
    def load_data():
        try:
            with open('data/enriched_notes.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    notes = data
                elif isinstance(data, dict) and 'notes' in data:
                    notes = data['notes']
                else:
                    notes = list(data.values()) if isinstance(data, dict) else []
            
            with open('data/graph_data.json', 'r', encoding='utf-8') as f:
                graph_data = json.load(f)
            with open('data/insights.json', 'r', encoding='utf-8') as f:
                insights = json.load(f)
            with open('data/link_suggestions.json', 'r', encoding='utf-8') as f:
                suggestions = json.load(f)
            return notes, graph_data, insights, suggestions
        except Exception as e:
            st.error(f"Error loading data: {e}")
            return None, None, None, None
    
    notes, graph_data, insights, suggestions = load_data()
    
    if notes is None:
        st.warning("⚠️  Run setup phases first!")
        st.stop()
    
    st.metric("Total Notes", len(notes))
    st.metric("Total Connections", graph_data['stats']['total_edges'])
    st.divider()
    
    search_query = st.text_input("🔍 Search notes:")

# ============================================================================
# MAIN TABS
# ============================================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Dashboard", "📝 Notes", "🕸️ Graph", "💡 Insights", "🔗 Links"
])

# ============================================================================
# TAB 1: DASHBOARD
# ============================================================================

with tab1:
    st.title("🧠 Your Knowledge Brain")
    st.markdown("Powered by AI-enhanced Obsidian vault analysis")
    
    st.divider()
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📚 Total Notes", len(notes))
    with col2:
        total_words = sum(n['readability']['total_words'] for n in notes)
        st.metric("📝 Total Words", f"{total_words:,}")
    with col3:
        all_tags = set()
        for n in notes:
            all_tags.update(n['tags'])
        st.metric("🏷️ Unique Tags", len(all_tags))
    with col4:
        st.metric("🔗 Total Links", graph_data['stats']['total_edges'])
    
    st.divider()
    
    # Insights
    if insights:
        st.subheader("💡 Vault Insights")
        st.markdown(f"""
<div class="insight-box">
{insights.get('vault_insights', 'Insights generating...')}
</div>
""", unsafe_allow_html=True)
    
    st.divider()
    
    # Top topics
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("🎯 Top Learning Topics")
        if insights and 'top_topics' in insights:
            for i, topic in enumerate(insights['top_topics'][:5], 1):
                st.write(f"{i}. **{topic}**")
    
    with col2:
        st.subheader("📊 Notes Distribution")
        folders = {}
        for note in notes:
            folder = note['file_metadata']['folder']
            folders[folder] = folders.get(folder, 0) + 1
        
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.pie(folders.values(), labels=folders.keys(), autopct='%1.1f%%')
        ax.set_title('Notes by Folder')
        st.pyplot(fig)

# ============================================================================
# TAB 2: NOTES BROWSER
# ============================================================================

with tab2:
    st.title("📚 Notes Browser")
    
    # Filter options
    col1, col2 = st.columns([1, 1])
    with col1:
        selected_folder = st.selectbox(
            "Filter by folder:",
            ['All'] + list(set(n['file_metadata']['folder'] for n in notes))
        )
    with col2:
        sort_by = st.radio("Sort by:", ["Title", "Word Count", "Modified Date"])
    
    # Filter notes
    filtered_notes = notes
    if selected_folder != 'All':
        filtered_notes = [n for n in notes if n['file_metadata']['folder'] == selected_folder]
    
    # Sort notes
    if sort_by == "Word Count":
        filtered_notes = sorted(filtered_notes, key=lambda x: x['readability']['total_words'], reverse=True)
    elif sort_by == "Modified Date":
        filtered_notes = sorted(filtered_notes, key=lambda x: x['file_metadata']['modified'], reverse=True)
    else:
        filtered_notes = sorted(filtered_notes, key=lambda x: x['title'])
    
    # Display notes
    for note in filtered_notes:
        with st.expander(f"📄 {note['title']} ({note['readability']['total_words']} words)"):
            st.write(f"**Folder:** {note['file_metadata']['folder']}")
            preview = note.get('content_preview', note.get('content', 'No preview available')[:200]); st.write(f"**Preview:** {preview}")
            
            if note['tags']:
                tags = " ".join([f"`{t}`" for t in note['tags'][:5]])
                st.write(f"**Tags:** {tags}")
            
            if note['links']:
                st.write(f"**Links to:** {', '.join(note['links'][:3])}")

# ============================================================================
# TAB 3: KNOWLEDGE GRAPH
# ============================================================================

with tab3:
    st.title("🕸️ Knowledge Graph")
    st.info("Visual representation of connections between your notes")
    
    # Simple stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Nodes", graph_data['stats']['total_nodes'])
    with col2:
        st.metric("Edges", graph_data['stats']['total_edges'])
    with col3:
        density = graph_data['stats']['total_edges'] / max(graph_data['stats']['total_nodes'], 1)
        st.metric("Connectivity", f"{density:.2f}")
    
    st.divider()
    
    # Top connected notes
    st.subheader("🌟 Most Connected Notes")
    
    # Calculate in-degree
    note_connections = {}
    for edge in graph_data['edges']:
        target = edge['target']
        note_connections[target] = note_connections.get(target, 0) + 1
    
    sorted_notes = sorted(note_connections.items(), key=lambda x: x[1], reverse=True)
    
    for node_id, count in sorted_notes[:10]:
        # Find note title
        note_title = None
        for node in graph_data['nodes']:
            if node['id'] == node_id:
                note_title = node['label']
                break
        
        if note_title:
            st.write(f"📍 **{note_title}** - {count} connections")

# ============================================================================
# TAB 4: INSIGHTS
# ============================================================================

with tab4:
    st.title("💡 AI-Generated Insights")
    
    if insights:
        st.subheader("Vault Intelligence")
        st.markdown(f"""
<div class="insight-box">
{insights.get('vault_insights', 'Generating insights...')}
</div>
""", unsafe_allow_html=True)
        
        st.divider()
        
        st.subheader("🎯 What You're Learning")
        st.write("Based on your notes, these are your main learning topics:")
        
        for i, topic in enumerate(insights.get('top_topics', [])[:10], 1):
            st.write(f"{i}. {topic}")

# ============================================================================
# TAB 5: LINK SUGGESTIONS
# ============================================================================

with tab5:
    st.title("🔗 Smart Link Suggestions")
    
    # Select a note
    selected_note_title = st.selectbox(
        "Choose a note to see suggestions:",
        [n['title'] for n in notes]
    )
    
    # Find note ID
    selected_note_id = None
    for note in notes:
        if note['title'] == selected_note_title:
            selected_note_id = note['id']
            break
    
    if selected_note_id and selected_note_id in suggestions:
        sugg_data = suggestions[selected_note_id]
        
        st.subheader(f"Suggested links for: {selected_note_title}")
        
        if sugg_data['suggestions']:
            for i, sugg in enumerate(sugg_data['suggestions'], 1):
                with st.expander(f"{i}. {sugg['title']} - {sugg['reason']}"):
                    st.write(f"**Reason:** {sugg['reason']}")
                    st.write(f"**Location:** {sugg['folder']}")
        else:
            st.info("No suggestions found for this note")

# ============================================================================
# FOOTER
# ============================================================================

st.divider()
st.caption("🧠 Obsidian AI Brain | Powered by AI & ChromaDB | Made with Streamlit")