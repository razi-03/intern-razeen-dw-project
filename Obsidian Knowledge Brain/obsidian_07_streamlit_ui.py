import streamlit as st
import json
import os
from datetime import datetime
import pandas as pd
from pathlib import Path
import re

try:
    from pyvis.network import Network
    import networkx as nx
except ImportError:
    st.warning("⚠️ Install pyvis and networkx: pip install pyvis networkx")

# Page config
st.set_page_config(page_title="🧠 Obsidian AI Brain", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .main { padding: 2rem; }
    .metric-card { 
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
    }
    .insight-box {
        background: #f0f4ff;
        border-left: 4px solid #667eea;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 4px;
    }
    .note-preview {
        background: #fafafa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
    }
    .knowledge-graph-container {
        background: white;
        border: 1px solid #ddd;
        border-radius: 8px;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "current_note" not in st.session_state:
    st.session_state.current_note = None

# Load data
@st.cache_resource
def load_data():
    data = {}
    try:
        if os.path.exists("data/vault_scan.json"):
            with open("data/vault_scan.json") as f:
                data["vault_scan"] = json.load(f)
    except: pass
    
    try:
        if os.path.exists("data/enriched_notes.json"):
            with open("data/enriched_notes.json") as f:
                data["enriched_notes"] = json.load(f)
    except: pass
    
    try:
        if os.path.exists("data/knowledge_graph.json"):
            with open("data/knowledge_graph.json") as f:
                data["knowledge_graph"] = json.load(f)
    except: pass
    
    try:
        if os.path.exists("data/insights.json"):
            with open("data/insights.json") as f:
                data["insights"] = json.load(f)
    except: pass
    
    try:
        if os.path.exists("data/link_suggestions.json"):
            with open("data/link_suggestions.json") as f:
                data["link_suggestions"] = json.load(f)
    except: pass
    
    return data

data = load_data()

# HEADER
col1, col2 = st.columns([0.8, 0.2])
with col1:
    st.title("🧠 Obsidian AI Brain")
    st.markdown("Your intelligent second brain • Locally powered • Always yours")
with col2:
    if st.button("🔄 Refresh Data", key="refresh_btn"):
        st.cache_resource.clear()
        st.rerun()

# TABS
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📚 Notes Browser",
    "🕸️ Knowledge Graph",
    "💡 Vault Intelligence",
    "🔗 Link Suggestions",
    "⚙️ Settings"
])

# ============ TAB 1: NOTES BROWSER ============
with tab1:
    st.header("📚 Browse Your Notes")
    
    if "enriched_notes" in data and data["enriched_notes"]:
        notes = data["enriched_notes"]
        
        # Search & filter
        col1, col2 = st.columns([0.7, 0.3])
        with col1:
            search_term = st.text_input("🔍 Search notes", placeholder="type to filter...")
        with col2:
            view_mode = st.radio("View:", ["Expanded", "Compact", "Table"], horizontal=True)
        
        # Filter notes
        filtered_notes = []
        for note in notes:
            title = note.get("title", "").lower()
            content = note.get("content", "").lower()
            if search_term.lower() in title or search_term.lower() in content:
                filtered_notes.append(note)
        
        st.markdown(f"**Found {len(filtered_notes)} of {len(notes)} notes**")
        
        if view_mode == "Expanded":
            # EXPANDED VIEW: Dual layout with content
            for i, note in enumerate(filtered_notes[:50]):  # Limit to 50 for performance
                with st.container():
                    col1, col2 = st.columns([0.6, 0.4])
                    
                    with col1:
                        st.markdown(f"### {note.get('title', 'Untitled')}")
                        st.markdown(f"📁 `{note.get('path', 'unknown')}`")
                        
                        content = note.get("content", "")[:500]
                        st.markdown(f"```\n{content}...\n```")
                    
                    with col2:
                        st.markdown("**📊 Metrics**")
                        col_a, col_b, col_c = st.columns(3)
                        with col_a:
                            st.metric("Words", note.get("word_count", 0))
                        with col_b:
                            st.metric("Headers", note.get("header_count", 0))
                        with col_c:
                            st.metric("Links", len(note.get("links", [])))
                        
                        tags = note.get("tags", [])
                        if tags:
                            st.markdown("**🏷️ Tags**")
                            for tag in tags[:5]:
                                st.write(f"`{tag}`")
                    
                    st.divider()
        
        elif view_mode == "Compact":
            # COMPACT VIEW: Streamlined list
            for note in filtered_notes[:100]:
                st.markdown(f"""
                **{note.get('title', 'Untitled')}**  
                📁 {note.get('path', 'unknown')} | 📝 {note.get('word_count', 0)} words | 🔗 {len(note.get('links', []))} links
                """)
                st.divider()
        
        else:  # Table view
            # TABLE VIEW: Sortable dataframe
            table_data = []
            for note in filtered_notes:
                table_data.append({
                    "Title": note.get("title", "Untitled"),
                    "Path": note.get("path", "unknown"),
                    "Words": note.get("word_count", 0),
                    "Headers": note.get("header_count", 0),
                    "Links": len(note.get("links", [])),
                    "Modified": note.get("modified", "unknown")
                })
            
            if table_data:
                df = pd.DataFrame(table_data)
                st.dataframe(df, use_container_width=True, height=500)
            else:
                st.info("No notes found matching your search.")
    else:
        st.info("No notes loaded. Run obsidian_02_note_parser.py first.")

# ============ TAB 2: KNOWLEDGE GRAPH ============
with tab2:
    st.header("🕸️ Knowledge Graph")
    
    if "knowledge_graph" in data and data["knowledge_graph"]:
        graph_data = data["knowledge_graph"]
        
        col1, col2 = st.columns([0.7, 0.3])
        with col1:
            st.subheader("Interactive Network Visualization")
        with col2:
            physics = st.checkbox("Physics simulation", value=True)
        
        try:
            # Create PyVis network
            net = Network(height='600px', directed=True, physics=physics)
            net.barnes_hut()
            
            # Add nodes
            nodes = graph_data.get("nodes", [])
            for node in nodes:
                size = min(30, max(10, node.get("size", 15)))
                color = "#667eea" if node.get("centrality", 0) > 0.1 else "#a0aec0"
                net.add_node(
                    node["id"],
                    label=node.get("label", node["id"])[:30],
                    title=node.get("label", node["id"]),
                    size=size,
                    color=color
                )
            
            # Add edges
            edges = graph_data.get("edges", [])
            for edge in edges:
                net.add_edge(edge["source"], edge["target"], weight=edge.get("weight", 1))
            
            # Save and display
            net.show("temp_graph.html")
            with open("temp_graph.html", "r", encoding="utf-8") as f:
                html_string = f.read()
            
            st.components.v1.html(html_string, height=650)
            
            # Graph statistics
            st.markdown("---")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Notes", len(nodes))
            with col2:
                st.metric("Total Connections", len(edges))
            with col3:
                avg_connections = len(edges) / max(1, len(nodes))
                st.metric("Avg Links/Note", f"{avg_connections:.1f}")
            with col4:
                st.metric("Network Density", f"{graph_data.get('density', 0):.2%}")
            
            # Top connected notes
            st.subheader("🌟 Most Connected Notes")
            top_nodes = sorted(nodes, key=lambda x: x.get("centrality", 0), reverse=True)[:10]
            for rank, node in enumerate(top_nodes, 1):
                st.markdown(f"**{rank}. {node.get('label', 'Unknown')}** ({node.get('centrality', 0):.2f})")
        
        except Exception as e:
            st.error(f"⚠️ Graph rendering error: {str(e)}")
            st.info("Ensure pyvis is installed: `pip install pyvis`")
    else:
        st.info("No knowledge graph data. Run obsidian_05_knowledge_graph.py first.")

# ============ TAB 3: VAULT INTELLIGENCE ============
with tab3:
    st.header("💡 Vault Intelligence")
    
    if "insights" in data and data["insights"]:
        insights = data["insights"]
        
        # Overview metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Notes", insights.get("total_notes", 0))
        with col2:
            st.metric("Total Words", f"{insights.get('total_words', 0):,}")
        with col3:
            st.metric("Average Note Length", f"{insights.get('avg_note_length', 0):.0f} words")
        with col4:
            st.metric("Network Density", f"{insights.get('network_density', 0):.2%}")
        
        st.markdown("---")
        
        # AI-Generated Insights
        st.subheader("🤖 AI Analysis")
        
        if "analysis" in insights:
            analysis = insights["analysis"]
            
            # Parse and format insights with proper line breaks
            if isinstance(analysis, str):
                # Split by numbered patterns (1., 2., etc)
                parts = re.split(r'(\d+\.)', analysis)
                
                insight_text = ""
                for i in range(1, len(parts), 2):
                    if i+1 < len(parts):
                        number = parts[i]
                        content = parts[i+1].strip()
                        insight_text += f"**{number}** {content}\n\n"
                
                st.markdown(insight_text)
            else:
                st.json(analysis)
        
        st.markdown("---")
        
        # Top Topics
        st.subheader("📚 Top Topics")
        if "top_topics" in insights:
            topics = insights["top_topics"]
            
            # Create columns for topics
            cols = st.columns(5)
            for i, topic in enumerate(topics[:10]):
                with cols[i % 5]:
                    st.metric(
                        topic.get("name", "Unknown"),
                        f"{topic.get('frequency', 0)} notes"
                    )
        
        st.markdown("---")
        
        # Learning Patterns
        st.subheader("🎯 Learning Patterns")
        if "patterns" in insights:
            for pattern in insights["patterns"][:5]:
                st.markdown(f"• {pattern}")
        
    else:
        st.info("No insights generated. Run obsidian_06_insights_generator.py first.")

# ============ TAB 4: LINK SUGGESTIONS ============
with tab4:
    st.header("🔗 Suggested Connections")
    
    if "link_suggestions" in data and data["link_suggestions"]:
        suggestions = data["link_suggestions"]
        
        # Filter by threshold
        threshold = st.slider("Similarity Threshold", 0.0, 1.0, 0.5)
        
        suggestion_list = suggestions.get("suggestions", [])
        filtered_suggestions = [s for s in suggestion_list if s.get("score", 0) >= threshold]
        
        st.markdown(f"**Showing {len(filtered_suggestions)} suggestions**")
        
        for sugg in filtered_suggestions[:50]:
            col1, col2, col3 = st.columns([0.4, 0.1, 0.4])
            
            with col1:
                st.markdown(f"📄 **{sugg.get('note1', 'Unknown')}**")
            
            with col2:
                score = sugg.get("score", 0)
                st.markdown(f"<div style='text-align: center; color: #667eea; font-weight: bold;'>{score:.2%}</div>", unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"📄 **{sugg.get('note2', 'Unknown')}**")
            
            reason = sugg.get("reason", "")
            st.caption(f"💡 {reason}")
            st.divider()
    
    else:
        st.info("No link suggestions. Run obsidian_04_link_suggester.py first.")

# ============ TAB 5: SETTINGS ============
with tab5:
    st.header("⚙️ Settings & Tools")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Data Status")
        
        status = {
            "Vault Scan": os.path.exists("data/vault_scan.json"),
            "Enriched Notes": os.path.exists("data/enriched_notes.json"),
            "Knowledge Graph": os.path.exists("data/knowledge_graph.json"),
            "Insights": os.path.exists("data/insights.json"),
            "Vector Store": os.path.exists("vector_store/"),
        }
        
        for name, exists in status.items():
            status_icon = "✅" if exists else "❌"
            st.write(f"{status_icon} {name}")
    
    with col2:
        st.subheader("Quick Actions")
        
        if st.button("🔄 Clear Cache", key="cache_clear"):
            st.cache_resource.clear()
            st.success("Cache cleared!")
        
        if st.button("📊 Export as JSON", key="export_json"):
            export_data = json.dumps(data, indent=2)
            st.download_button(
                label="Download JSON",
                data=export_data,
                file_name=f"obsidian_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    
    st.markdown("---")
    
    st.subheader("📖 How to Use")
    st.markdown("""
    1. **Setup Phase**: Run scripts in order from 01 to 06
    2. **Notes Browser**: Search and explore your vault
    3. **Knowledge Graph**: See connections between ideas
    4. **Vault Intelligence**: AI-generated insights
    5. **Link Suggestions**: Discover new connections
    
    **Need help?** See README.md in project folder
    """)
    
    st.subheader("🔧 Environment")
    st.write(f"App Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    st.write(f"Data Path: {os.path.abspath('data/')}")
    st.write(f"Vector Store Path: {os.path.abspath('vector_store/')}")