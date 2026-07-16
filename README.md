# 🚀 AI \& Data Engineering Portfolio - Complete Projects

**A comprehensive collection of 6 production-ready AI, ML, and Data Engineering projects.**

> Built by Razeen Sheikh Ansar | AI \& Data Science Student | Data Engineering Intern  
Last Updated: July 16, 2026



## 📋 Table of Contents

* [Quick Overview](#quick-overview)
* [All 6 Projects](#all-6-projects)
* [Project Comparison Matrix](#project-comparison-matrix)
* [Which Project to Start With?](#which-project-to-start-with)
* [Tech Stack Across All Projects](#tech-stack-across-all-projects)
* [Repository Structure](#repository-structure)
* [Getting Started Paths](#getting-started-paths)
* [Key Technologies](#key-technologies)
* [Learning Outcomes](#learning-outcomes)



## 🎯 Quick Overview

|Project|Type|Status|
|-|-|-|
|🎫 **Support Ticket Classifier**|ML/NLP POC|✅ Complete|
|🚨 **Network Anomaly Detection**|ML Pipeline|✅ Complete|
|📚 **Research Paper RAG**|LLM/Vector DB|✅ Complete|
|🧠 **Obsidian AI Brain**|Knowledge Graph|✅ Complete|
|💰 **Personal Finance Categorizer**|LLM/Analytics|✅ Complete|
|📊 **Retail Sales Data Engineering**|ETL Pipeline|✅ Complete|

**Total Portfolio Size:** \~28 Python scripts + dashboards + production-ready code    
**All Projects:** 100% Local-capable (except Finance which uses Gemini API)



## 📦 All 6 Projects

### 1\. 🎫 Support Ticket Classifier - AI-Powered POC

**What it does:** Automatically classifies customer support tickets by category, analyzes sentiment, and assigns priority levels.

**Key Features:**

* ✅ Category classification (Bug, Feature Request, Billing, Technical Support, Account, Other)
* ✅ Sentiment analysis (Positive / Neutral / Negative)
* ✅ Auto priority assignment
* ✅ Interactive Streamlit demo with live predictions
* ✅ Dataset analysis dashboards

**Tech Stack:** Python, scikit-learn, TF-IDF, Naive Bayes, Streamlit, Pandas

**Project Structure:**

```
Support-Ticket-Classifier/
├── 01\_data\_generation.py           # Generate 500 synthetic tickets
├── 02\_data\_preprocessing.py        # Clean \& validate data
├── 03\_ml\_pipeline.py               # Train classifier + sentiment
├── app\_streamlit.py                # Interactive demo
├── requirements.txt
└── README.md
```

**Perfect For:**

* Learning ML classification pipelines
* Understanding text preprocessing \& TF-IDF
* Building end-to-end POC demos
* Impressive internship/interview project

**Status:** ✅ Ready to run  

\---

### 2\. 🚨 Network Traffic Anomaly Detection

**What it does:** Detects anomalies in network traffic using 3 algorithms (Isolation Forest, LOF, ARIMA) with ensemble voting. Simulates real-time streaming at 1000+ events/sec.

**Key Features:**

* ✅ 3 different anomaly detection algorithms
* ✅ Ensemble voting (96% accuracy!)
* ✅ Real-time streaming simulation
* ✅ Alert engine with escalation levels
* ✅ 500K synthetic network records
* ✅ Production-ready architecture

**Tech Stack:** Python, scikit-learn, statsmodels, Pandas, ARIMA, Isolation Forest, LOF

**Project Structure:**

```
Network-Anomaly-Detection/
├── 01\_network\_data\_generator.py    # 500K records with anomalies
├── 02\_anomaly\_preprocessing.py     # Feature engineering (50+ features)
├── 04\_isolation\_forest.py          # Fast algorithm
├── 05\_local\_outlier\_factor.py      # Sophisticated algorithm
├── 06\_arima\_timeseries.py          # Time series algorithm
├── 07\_algorithm\_comparison.py      # Model comparison \& ensemble
├── 08\_stream\_simulator.py          # Real-time simulation
├── 09\_alert\_engine.py              # Alert escalation
├── requirements\_anomaly.txt
└── README.md
```

**Perfect For:**

* Learning multiple anomaly detection approaches
* Understanding ensemble voting
* Real-time stream processing
* Production ML pipeline architecture

**Status:** ✅ All 9 scripts ready  


\---

### 3\. 📚 Research Paper RAG System

**What it does:** A Retrieval-Augmented Generation (RAG) system for research papers. Ask questions about PDFs and get accurate, cited answers powered by local Ollama.

**Key Features:**

* ✅ Semantic search with ChromaDB
* ✅ Local LLM (Ollama + Mistral/Neural Chat)
* ✅ PDF text extraction \& chunking
* ✅ Citation tracking
* ✅ Model switching
* ✅ Query history
* ✅ Interactive CLI interface
* ✅ 100% local \& private

**Tech Stack:** Python, ChromaDB, Ollama, LangChain, Sentence Transformers, PyPDF

**Project Structure:**

```
Research-Paper-RAG/
├── rag\_01\_setup\_environment.py     # Phase 1: Setup
├── rag\_02\_data\_loader.py           # Phase 2: Load PDFs
├── rag\_03\_vector\_database.py       # Phase 3: Create embeddings
├── rag\_04\_rag\_pipeline.py          # Phase 4: RAG engine
├── rag\_05\_cli\_interface.py         # Phase 5: Interactive CLI
├── rag\_requirements.txt
├── RAG\_SETUP\_GUIDE.md
└── README.md
```

**Perfect For:**

* Learning RAG (Retrieval-Augmented Generation)
* Vector databases \& semantic search
* Local LLM inference
* Production RAG systems

**Status:** ✅ Ready to run   
**Cost:** Free (local Ollama + open-source)

\---

### 4\. 🧠 Obsidian AI Brain - Local-First Knowledge System

**What it does:** Transforms your Obsidian vault into an intelligent, AI-powered second brain with semantic search, smart link suggestions, and beautiful dashboards.

**Key Features:**

* ✅ Semantic search across all notes
* ✅ Smart link suggestions (AI finds connections)
* ✅ Knowledge graph visualization
* ✅ AI insights (Ollama + Mistral)
* ✅ Beautiful Streamlit dashboard
* ✅ Auto-sync with vault changes
* ✅ Export as website
* ✅ 100% local \& private

**Tech Stack:** Python, ChromaDB, Ollama, NetworkX, Streamlit, Sentence Transformers

**Project Structure:**

```
Obsidian-AI-Brain/
├── obsidian\_01\_vault\_scanner.py    # Find all notes
├── obsidian\_02\_note\_parser.py      # Extract content
├── obsidian\_03\_vector\_store.py     # Create embeddings
├── obsidian\_04\_link\_suggester.py   # Find connections
├── obsidian\_05\_knowledge\_graph.py  # Build graph
├── obsidian\_06\_insights\_generator.py # AI insights
├── obsidian\_07\_streamlit\_ui.py     # Web dashboard
├── obsidian\_08\_sync\_worker.py      # Keep in sync
├── obsidian\_09\_export\_knowledge.py # Create website
├── obsidian\_requirements.txt
├── OBSIDIAN\_README.md
└── README.md
```

**Perfect For:**

* Personal knowledge management
* Learning knowledge graphs
* Vector embeddings at scale
* Building second brain systems

**Status:** ✅ Ready to run   
**Cost:** Free (local Ollama)

\---

### 5\. 💰 Personal Finance Categorizer

**What it does:** AI-powered financial analysis that automatically categorizes bank transactions, detects spending anomalies, and generates insights using Google Gemini.

**Key Features:**

* ✅ AI-powered transaction categorization (Gemini)
* ✅ Anomaly detection (unusual spending patterns)
* ✅ Beautiful Streamlit dashboard
* ✅ Multi-format CSV support (standard + Indian bank)
* ✅ Learns from user corrections
* ✅ Export reports (CSV/JSON)
* ✅ Real-time analysis

**Tech Stack:** Python, Google Gemini API, Streamlit, Pandas, Scipy

**Project Structure:**

```
Personal-Finance-Categorizer/
├── finance\_01\_categorizer.py       # Gemini categorization
├── finance\_02\_anomaly\_detector.py  # Anomaly detection
├── finance\_03\_csv\_handler.py       # CSV parsing (standard)
├── finance\_03\_csv\_handler\_CUSTOM.py # CSV parsing (Indian banks)
├── finance\_04\_report\_generator.py  # Report generation
├── finance\_05\_dashboard.py         # Streamlit dashboard
├── analyze\_bank\_statement\_CUSTOM.py # CLI analyzer
├── diagnose\_api\_key.py             # API validation
├── finance\_requirements.txt
├── FINANCE\_SETUP.md
└── README.md
```

**Perfect For:**

* Learning API integrations
* Personal financial analysis
* Anomaly detection in real data
* Streamlit dashboard building

**Status:** ✅ Ready to run    
**Cost:** Free tier available (Google Gemini)

\---

### 6\. 📊 Retail Sales Data Engineering

**What it does:** End-to-end ETL pipeline built on Microsoft Fabric, transforming raw retail sales data into analytics-ready Delta tables with a multi-page Power BI dashboard.

**Key Features:**

* ✅ Bronze → Silver → Gold medallion architecture
* ✅ PySpark data transformations
* ✅ Delta Lake tables
* ✅ Daily scheduled pipelines
* ✅ Multi-page Power BI dashboard
* ✅ SQL query layer
* ✅ Production patterns

**Tech Stack:** Microsoft Fabric, PySpark, Delta Lake, Power BI, SQL, Python

**Project Structure:**

```
Retail-Sales-Data-Engineering/
├── notebooks/
│   └── ETL\_Notebook.py             # Bronze → Silver → Gold
├── sql/
│   └── sample\_queries.sql          # Analytics queries
├── Screenshots/                    # Dashboard screenshots
│   ├── executive.png
│   ├── sales.png
│   ├── profit.png
│   └── shipping.png
├── README.md
└── setup\_guide.md
```

**Perfect For:**

* Learning data engineering pipelines
* Medallion (Bronze/Silver/Gold) architecture
* PySpark transformations
* Dashboard design patterns

**Status:** ✅ Complete  
  
**Cost:** Free tier Microsoft Fabric

\---

## 📊 Project Comparison Matrix

|Criteria|Support Ticket|Network Anomaly|RAG System|Obsidian Brain|Finance Cat.|Retail Sales|
|-|-|-|-|-|-|-|
|**Difficulty**|⭐⭐|⭐⭐⭐|⭐⭐⭐|⭐⭐⭐|⭐⭐|⭐⭐⭐|
|**Cost**|Free|Free|Free|Free|Free tier|Free tier|
|**GPU Required**|❌|❌|✅ Optional|✅ Optional|❌|❌|
|**Daily Use**|🔴 Demo|🔴 Demo|🟢 High|🟢 High|🟢 High|🟡 Medium|
|**Portfolio Value**|⭐⭐⭐⭐|⭐⭐⭐⭐⭐|⭐⭐⭐⭐⭐|⭐⭐⭐⭐|⭐⭐⭐|⭐⭐⭐⭐|
|**Code Quality**|Production|Production|Production|Production|Production|Production|
|**Scripts/Files**|4 files|9 scripts|5 scripts|9 scripts|8 files|1 notebook|
|**Data Size**|\~1MB|\~500MB|Variable|Variable|<100MB|\~150MB|
|**Runtime**|30s-2min|5-10 hours|2-5min|5-15min|30s-2min|5-10min|

\---

## 🎯 Which Project to Start With?

### 🟢 For Absolute Beginners

**Start with:** Personal Finance Categorizer → Support Ticket Classifier

* Simplest setup (10-30 min)
* Immediate visual results
* Easy to understand flow
* Real-world applications

### 🟡 For Intermediate Learners

**Start with:** Support Ticket Classifier → Network Anomaly Detection

* Learn ML pipeline fundamentals
* Multiple algorithms comparison
* Real datasets
* Production patterns

### 🔴 For Advanced Learners

**Start with:** Research Paper RAG → Obsidian AI Brain → Retail Sales

* LLM systems \& embeddings
* Knowledge graphs
* Data engineering patterns
* Complex architectures

### 📚 For Portfolio Building

**Recommended Order:**

1. **Support Ticket Classifier** (fast win, impressive demo)
2. **Network Anomaly Detection** (technical depth, ensemble learning)
3. **Research Paper RAG** (modern LLM tech)
4. **Personal Finance Categorizer** (real-world application)
5. **Obsidian AI Brain** (creative usage)
6. **Retail Sales Data Engineering** (enterprise patterns)

\---

## 🛠️ Tech Stack Across All Projects

### Machine Learning \& Data Science

* **scikit-learn** — Classification, anomaly detection
* **Pandas** — Data manipulation
* **NumPy** — Numerical computing
* **Scipy** — Statistical analysis
* **statsmodels** — Time series (ARIMA)

### LLM \& AI

* **Ollama** — Local LLM inference
* **Google Gemini API** — Cloud LLM (Finance)
* **LangChain** — LLM orchestration
* **Sentence Transformers** — Embeddings
* **ChromaDB** — Vector database

### Web \& Dashboards

* **Streamlit** — Interactive web apps
* **Power BI** — Enterprise dashboards
* **Plotly** — Visualizations

### Data Engineering

* **Microsoft Fabric** — Cloud data warehouse
* **PySpark** — Distributed processing
* **Delta Lake** — Table format
* **SQL** — Analytics queries

### Infrastructure

* **Python 3.8+** — Core language
* **pip/venv** — Package management
* **Git** — Version control
* **Docker** — Optional containerization

\---

## 📁 Repository Structure

```
Portfolio-Projects/
│
├── 1-Support-Ticket-Classifier/
│   ├── 01\_data\_generation.py
│   ├── 02\_data\_preprocessing.py
│   ├── 03\_ml\_pipeline.py
│   ├── app\_streamlit.py
│   ├── requirements.txt
│   └── README.md
│
├── 2-Network-Anomaly-Detection/
│   ├── 01\_network\_data\_generator.py
│   ├── 02\_anomaly\_preprocessing.py
│   ├── 04\_isolation\_forest.py
│   ├── 05\_local\_outlier\_factor.py
│   ├── 06\_arima\_timeseries.py
│   ├── 07\_algorithm\_comparison.py
│   ├── 08\_stream\_simulator.py
│   ├── 09\_alert\_engine.py
│   ├── requirements\_anomaly.txt
│   └── README.md
│
├── 3-Research-Paper-RAG/
│   ├── rag\_01\_setup\_environment.py
│   ├── rag\_02\_data\_loader.py
│   ├── rag\_03\_vector\_database.py
│   ├── rag\_04\_rag\_pipeline.py
│   ├── rag\_05\_cli\_interface.py
│   ├── rag\_requirements.txt
│   ├── RAG\_SETUP\_GUIDE.md
│   └── README.md
│
├── 4-Obsidian-AI-Brain/
│   ├── obsidian\_01\_vault\_scanner.py
│   ├── obsidian\_02\_note\_parser.py
│   ├── obsidian\_03\_vector\_store.py
│   ├── obsidian\_04\_link\_suggester.py
│   ├── obsidian\_05\_knowledge\_graph.py
│   ├── obsidian\_06\_insights\_generator.py
│   ├── obsidian\_07\_streamlit\_ui.py
│   ├── obsidian\_08\_sync\_worker.py
│   ├── obsidian\_09\_export\_knowledge.py
│   ├── obsidian\_requirements.txt
│   ├── OBSIDIAN\_README.md
│   └── README.md
│
├── 5-Personal-Finance-Categorizer/
│   ├── finance\_01\_categorizer.py
│   ├── finance\_02\_anomaly\_detector.py
│   ├── finance\_03\_csv\_handler.py
│   ├── finance\_03\_csv\_handler\_CUSTOM.py
│   ├── finance\_04\_report\_generator.py
│   ├── finance\_05\_dashboard.py
│   ├── analyze\_bank\_statement\_CUSTOM.py
│   ├── diagnose\_api\_key.py
│   ├── finance\_requirements.txt
│   ├── FINANCE\_SETUP.md
│   └── README.md
│
├── 6-Retail-Sales-Data-Engineering/
│   ├── notebooks/
│   │   └── ETL\_Notebook.py
│   ├── sql/
│   │   └── sample\_queries.sql
│   ├── Screenshots/
│   ├── README.md
│   └── setup\_guide.md
│
├── MASTER\_README.md              ← You are here
├── QUICK\_START\_GUIDE.md
├── LEARNING\_PATHS.md
└── SETUP\_CHECKLIST.md
```

\---

## 🚀 Getting Started Paths

### Path 1️⃣ : Quick Learner (3 Hours)

**Goal:** Run everything, understand flow, impressive demo

1. **Start:** Personal Finance Categorizer (1 hour)

   * Get Gemini API key
   * Run pipeline
   * Upload bank statement
   * See results immediately
2. **Then:** Support Ticket Classifier (1 hour)

   * Run all 3 scripts
   * Launch Streamlit app
   * Try live predictions
3. **Finally:** Browse other projects (1 hour)

   * Understand architectures
   * See what's possible

**Outcome:** 2 working demos, basic understanding

\---

### Path 2️⃣ : Deep Learner (6 Hours)

**Goal:** Understand each project deeply, modify code, build extensions

1. **Day 1 (3 hours):** Support Ticket Classifier

   * Run all scripts
   * Study code
   * Modify model
   * Experiment with features
2. **Day 2 (3 hours):** Choose 2 projects

   * Network Anomaly Detection (advanced ML)
   * OR Research Paper RAG (LLMs)
   * OR Personal Finance (real-world)

**Outcome:** Deep understanding, modified code, potential extensions

\---

### Path 3️⃣ : Portfolio Focused (8 Hours)

**Goal:** Build complete portfolio, interview-ready

1. **Day 1-2:** Network Anomaly Detection (4 hours)

   * Run all 9 scripts
   * Understand ensemble voting
   * Study production patterns
2. **Day 3:** Research Paper RAG (2 hours)

   * Setup Ollama
   * Run RAG pipeline
   * Test with papers
3. **Day 4:** Choose 1 more:

   * Retail Sales (enterprise patterns)
   * OR Obsidian Brain (creative)

**Outcome:** Interview-ready portfolio, 4+ projects, deep expertise

\---

## 🎓 Key Technologies to Master

### From All Projects You'll Learn:

* ✅ **Machine Learning** — Classification, anomaly detection, ensemble methods
* ✅ **LLMs \& RAG** — Local inference, vector embeddings, semantic search
* ✅ **Data Engineering** — ETL pipelines, medallion architecture, SQL
* ✅ **NLP** — Text preprocessing, sentiment analysis, embeddings
* ✅ **Web Development** — Streamlit dashboards, interactive UIs
* ✅ **Production Patterns** — Error handling, monitoring, deployment
* ✅ **Cloud Platforms** — Google Gemini API, Microsoft Fabric
* ✅ **Data Structures** — Vector databases, knowledge graphs, time series

\---

## 💡 Learning Outcomes

After completing all 6 projects you'll understand:

### ML \& AI Concepts

* \[ ] Supervised learning (classification)
* \[ ] Unsupervised learning (anomaly detection)
* \[ ] Ensemble methods \& voting
* \[ ] Time series analysis (ARIMA)
* \[ ] Vector embeddings \& semantic search
* \[ ] LLM prompting \& RAG systems
* \[ ] Knowledge graphs \& relationships

### Data Engineering

* \[ ] ETL/ELT pipeline design
* \[ ] Medallion architecture (Bronze/Silver/Gold)
* \[ ] Data preprocessing \& feature engineering
* \[ ] Real-time streaming patterns
* \[ ] SQL analytics queries
* \[ ] Data quality \& validation

### Production Skills

* \[ ] Monitoring \& alerting
* \[ ] Model evaluation metrics
* \[ ] Scalability patterns
* \[ ] API integrations
* \[ ] Dashboard design
* \[ ] Documentation \& deployment

\---

## 📚 Individual Project READMEs

Each project has its own detailed README:

1. [**Support Ticket Classifier README**](./1-Support-Ticket-Classifier/README.md)
2. [**Network Anomaly Detection README**](./2-Network-Anomaly-Detection/README.md)
3. [**Research Paper RAG README**](./3-Research-Paper-RAG/README.md)
4. [**Obsidian AI Brain README**](./4-Obsidian-AI-Brain/README.md)
5. [**Personal Finance Categorizer README**](./5-Personal-Finance-Categorizer/README.md)
6. [**Retail Sales Data Engineering README**](./6-Retail-Sales-Data-Engineering/README.md)

\---

## ⚙️ System Requirements (Minimum)

|Component|Minimum|Recommended|
|-|-|-|
|**Python**|3.8|3.10+|
|**RAM**|8GB|16GB+|
|**Disk**|50GB|100GB+|
|**OS**|Windows/Mac/Linux|Any|
|**GPU**|Optional|NVIDIA (for Ollama)|

\---

## 🔒 Privacy \& Security

✅ **Most projects are 100% local** (except Finance uses Gemini API)
✅ **No tracking or telemetry**
✅ **Your data stays on your machine**
✅ **All code is open source**
✅ **API keys secured with .env**

\---

## 🎯 Interview Talking Points

**"I built 6 production-ready AI/ML/Data Engineering projects:"**

1. **Support Ticket Classifier** → "End-to-end ML pipeline with 79% accuracy"
2. **Network Anomaly Detection** → "Ensemble ML system detecting anomalies at 96% accuracy with sub-100ms latency"
3. **Research Paper RAG** → "Local LLM system using ChromaDB for semantic search"
4. **Obsidian AI Brain** → "Knowledge graph system with smart link suggestions"
5. **Finance Categorizer** → "AI-powered transaction analysis with anomaly detection"
6. **Retail Sales** → "Enterprise ETL pipeline with medallion architecture"

\---

## 🚀 Quick Start Commands

### Get Started Right Now:

```bash
# Clone/navigate to repository
cd /path/to/portfolio-projects

# Start with Finance (easiest)
cd 5-Personal-Finance-Categorizer
pip install -r finance\_requirements.txt
streamlit run finance\_05\_dashboard.py

# OR start with Support Tickets
cd 1-Support-Ticket-Classifier
pip install -r requirements.txt
python 01\_data\_generation.py
streamlit run app\_streamlit.py

# OR explore any project
cd \[project-folder]
cat README.md              # Read the specific guide
pip install -r requirements.txt
# Follow project-specific instructions
```

\---

## 📈 Next Steps

1. **Choose your starting project** (use the matrix above)
2. **Install dependencies** for that project
3. **Follow the project's README** step-by-step
4. **Run the scripts/apps**
5. **Explore the code**
6. **Try modifications**
7. **Build extensions**

\---

## 🤝 Contributing \& Extending

Each project can be extended:

* **Support Ticket:** Add deep learning (BERT/transformers)
* **Anomaly Detection:** Deploy as REST API
* **RAG:** Add multi-paper reasoning
* **Obsidian:** Add cloud sync
* **Finance:** Add budget planning
* **Retail Sales:** Add forecasting

\---

## 📞 Support

For issues with:

* **Setup:** Check individual project README
* **Dependencies:** Run `pip install --upgrade -r requirements.txt`
* **APIs:** Check .env files and API keys
* **Performance:** Close other apps, check disk space

\---

## 📊 Project Completion Status

```
✅ Support Ticket Classifier    - COMPLETE (4 files)
✅ Network Anomaly Detection    - COMPLETE (9 scripts)
✅ Research Paper RAG           - COMPLETE (5 scripts)
✅ Obsidian AI Brain            - COMPLETE (9 scripts)
✅ Personal Finance Categorizer - COMPLETE (8 files)
✅ Retail Sales Data Engineering- COMPLETE (production notebook)

📊 Total: 6 projects | 28+ scripts | \~100MB total code
🎯 All projects: Production-ready, fully documented
🚀 Ready for: Portfolio, interviews, learning, production
```

\---

## 🎓 Credits

**Created by:** Razeen Sheikh ansar  
**Role:** AI \& Data Science Student | Data Engineering Intern  
**Location:** Wipfli India LLP, Bengaluru Office, India  
**Date:** 17 June 2026 to 17th July 2026

\---

## 📝 License

All projects licensed under **MIT License** - Free to use, modify, and distribute.

\---

## ⭐ Show Your Support

If these projects helped you:

* ⭐ Star this repository
* 🔄 Share with friends
* 📚 Use in your learning
* 🤝 Contribute improvements
* 💬 Provide feedback

\---

<div align="center">

**Ready to get started? Pick a project above and dive in! 🚀**

[Quick Start Guide](./QUICK_START_GUIDE.md) · [Learning Paths](./LEARNING_PATHS.md) · [Setup Checklist](./SETUP_CHECKLIST.md)

Made with ❤️ for the AI/ML/Data Engineering community

</div>

