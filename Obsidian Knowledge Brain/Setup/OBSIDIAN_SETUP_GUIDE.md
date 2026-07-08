# 🧠 Obsidian AI Brain - Complete Setup Guide

**Status:** ✅ Production-Ready  
**Phase:** Option A - Local-First  
**Timeline:** 2-3 weeks to build, daily use thereafter  
**Level:** Beginner-Friendly  

---

## 📋 What You're Building

An **AI-powered second brain** that:
- 🔍 Indexes your entire Obsidian vault
- 🤖 Uses local AI (Mistral) for insights
- 🕸️ Builds a knowledge graph of connections
- 💡 Generates insights from your notes
- 🌐 Creates a beautiful web dashboard
- 🔄 Keeps everything in sync automatically

---

## 🚀 QUICK START (5 Steps)

### **STEP 1: Prerequisites**
```bash
# Check Python version (need 3.8+)
python --version

# Install Ollama from https://ollama.ai
# Then run in terminal:
ollama serve

# Keep this running in background!
```

### **STEP 2: Install Dependencies**
```bash
pip install -r obsidian_requirements.txt
```

### **STEP 3: Prepare Your Vault**
```bash
# Create folder
mkdir obsidian_vault

# Copy your notes there
cp -r /path/to/your/obsidian/* obsidian_vault/
```

### **STEP 4: Run Pipeline (in order)**
```bash
python obsidian_01_vault_scanner.py        # Scan vault
python obsidian_02_note_parser.py          # Parse notes
python obsidian_03_vector_store.py         # Create embeddings
python obsidian_04_link_suggester.py       # Suggest links
python obsidian_05_knowledge_graph.py      # Build graph
python obsidian_06_insights_generator.py   # Generate insights
```

### **STEP 5: Launch Dashboard**
```bash
streamlit run obsidian_07_streamlit_ui.py
```

Then visit: http://localhost:8501

---

## 📚 What Each Script Does

### **01_vault_scanner.py** (5 seconds)
- Finds all markdown files in your vault
- Extracts basic metadata (titles, folders)
- Detects links and tags
- **Output:** `data/vault_scan.json`

### **02_note_parser.py** (30 seconds)
- Reads full content of each note
- Extracts headers, code, quotes, lists
- Identifies important concepts (bold text)
- Calculates readability metrics
- **Output:** `data/enriched_notes.json`

### **03_vector_store.py** (2-5 minutes)
- Creates embeddings for all notes
- Stores in ChromaDB (local vector database)
- Makes semantic search possible
- **Output:** `vector_store/` directory

### **04_link_suggester.py** (1 minute)
- Finds similar notes by content
- Suggests connections by shared tags
- Suggests connections by concepts
- **Output:** `data/link_suggestions.json`

### **05_knowledge_graph.py** (30 seconds)
- Builds graph of all connections
- Calculates centrality (most connected notes)
- Prepares data for visualization
- **Output:** `data/graph_data.json`, `data/knowledge_graph.json`

### **06_insights_generator.py** (1-2 minutes)
- Uses Ollama (Mistral) to analyze vault
- Generates insights about your learning
- Identifies top topics
- **Output:** `data/insights.json`

### **07_streamlit_ui.py** (Runs forever)
- Beautiful dashboard to explore vault
- Search and browse notes
- View knowledge graph
- Read AI insights
- **Command:** `streamlit run obsidian_07_streamlit_ui.py`

### **08_sync_worker.py** (30 seconds)
- Detects changed notes
- Updates vector store
- Keeps everything in sync
- **Run:** `python obsidian_08_sync_worker.py` (or setup as scheduled task)

### **09_export_knowledge.py** (10 seconds)
- Creates static HTML website
- Searchable, shareable version
- **Output:** `exports/index.html`

---

## ⏱️ Execution Timeline

| Step | Time | Command |
|------|------|---------|
| 1. Scan vault | 5s | `python obsidian_01_vault_scanner.py` |
| 2. Parse notes | 30s | `python obsidian_02_note_parser.py` |
| 3. Create vectors | 2-5m | `python obsidian_03_vector_store.py` |
| 4. Link suggestions | 1m | `python obsidian_04_link_suggester.py` |
| 5. Knowledge graph | 30s | `python obsidian_05_knowledge_graph.py` |
| 6. AI insights | 1-2m | `python obsidian_06_insights_generator.py` |
| 7. Launch UI | ∞ | `streamlit run obsidian_07_streamlit_ui.py` |
| **Total first run** | **~10 minutes** | |
| **Subsequent syncs** | **<1 minute** | `python obsidian_08_sync_worker.py` |

---

## 📁 Folder Structure

```
obsidian-ai-brain/
├── obsidian_01_vault_scanner.py
├── obsidian_02_note_parser.py
├── obsidian_03_vector_store.py
├── obsidian_04_link_suggester.py
├── obsidian_05_knowledge_graph.py
├── obsidian_06_insights_generator.py
├── obsidian_07_streamlit_ui.py
├── obsidian_08_sync_worker.py
├── obsidian_09_export_knowledge.py
├── obsidian_requirements.txt
│
├── obsidian_vault/                 ← Your notes here!
│   ├── note1.md
│   ├── note2.md
│   └── folder/
│       └── note3.md
│
├── data/
│   ├── vault_scan.json
│   ├── enriched_notes.json
│   ├── link_suggestions.json
│   ├── graph_data.json
│   ├── knowledge_graph.json
│   ├── insights.json
│   └── .vault_hashes.json
│
├── vector_store/                   ← ChromaDB storage
│   └── ...
│
└── exports/
    └── index.html                  ← Your website!
```

---

## 🤖 Local LLM Setup

This project uses **Ollama** + **Mistral 7B** for local AI insights.

### Installation
```bash
# Windows/Mac/Linux
Visit: https://ollama.ai
Download and install
```

### First Run
```bash
# Terminal 1 (keep running):
ollama serve

# Terminal 2 (new terminal):
ollama pull mistral:7b-instruct-q4_K_M
```

Then the project uses it automatically!

---

## ✅ Verification Checklist

Before you start:
- [ ] Python 3.8+ installed
- [ ] Ollama installed and models downloaded
- [ ] ~10GB disk space available
- [ ] ~8GB RAM available
- [ ] Your Obsidian vault location known

After first run:
- [ ] `data/vault_scan.json` created
- [ ] `data/enriched_notes.json` created
- [ ] `vector_store/` directory created
- [ ] `data/insights.json` created
- [ ] Streamlit UI loads without errors

---

## 🎯 Dashboard Features

### Dashboard Tab
- Total notes counter
- Word count statistics
- Tag and link counts
- AI-generated vault insights
- Top learning topics
- Notes distribution chart

### Notes Tab
- Browse all notes
- Filter by folder
- Sort by title/word count/date
- View note preview
- See tags and links

### Knowledge Graph Tab
- Connection statistics
- Most connected notes
- Visualization data

### Insights Tab
- Vault-wide insights (AI-generated)
- Top learning topics
- Learning path recommendations

### Links Tab
- Smart suggestions for each note
- Why notes are related
- One-click navigation

---

## 🔄 Continuous Usage

### Daily Workflow
1. Add/edit notes in Obsidian normally
2. Run sync worker occasionally:
   ```bash
   python obsidian_08_sync_worker.py
   ```
3. View dashboard:
   ```bash
   streamlit run obsidian_07_streamlit_ui.py
   ```

### Weekly Workflow
- Review insights
- Check knowledge graph
- Export website if sharing

### Monthly Workflow
- Re-run full pipeline for fresh insights
- Review learning progress
- Plan next learning topics

---

## 🐛 Troubleshooting

### "Ollama not found"
- Install from https://ollama.ai
- Make sure 'ollama serve' is running
- Windows: May need to add to PATH

### "No notes found"
- Check `obsidian_vault/` folder exists
- Add some markdown files (.md)
- Run `obsidian_01_vault_scanner.py` again

### "Vector store error"
- Delete `vector_store/` folder
- Re-run `obsidian_03_vector_store.py`

### "Streamlit connection refused"
- Make sure you're in correct directory
- Try a different port: `streamlit run script.py --server.port 8502`

### "Out of memory"
- Close other applications
- Reduce vault size for testing
- Try smaller sample first

---

## 🎓 Learning Path

1. **Week 1:** Understand RAG + embeddings
2. **Week 2:** Build the pipeline
3. **Week 3:** Customize and optimize
4. **Ongoing:** Use and improve

---

## 🌟 Next Steps (Option C - Hybrid)

After completing Option A, you can upgrade to:
- Add Claude API for better insights
- Create a cloud sync option
- Build sharing features
- Add collaborative notes

---

## 💡 Tips for Success

1. **Start small** - Test with 10-20 notes first
2. **Quality notes** - Clean markdown helps
3. **Good tags** - Improves suggestions
4. **Regular updates** - Keep Ollama running
5. **Explore settings** - Customize for your needs

---

## 📊 Performance Expectations

| Metric | Time | Quality |
|--------|------|---------|
| Scan 100 notes | 5s | Fast |
| Parse 100 notes | 30s | Good |
| Embed 100 notes | 2m | Accurate |
| Graph 100 notes | 30s | Connected |
| Generate insights | 1-2m | Deep |
| Dashboard load | <1s | Smooth |
| Query response | <100ms | Instant |

---

## 🎉 You've Built an AI Brain!

You now have:
✅ Indexed knowledge base  
✅ AI-powered insights  
✅ Smart link suggestions  
✅ Beautiful dashboard  
✅ Searchable website  

Ready to think better! 🧠

---

**Next:** Run the 9 scripts in order, then explore your knowledge brain!

Built with ❤️ by RAze | July 2026
