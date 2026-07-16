# 💰 Personal Finance Categorizer

> AI-powered transaction categorization and spending analysis with anomaly detection, automated insights, and beautiful financial dashboards.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Status: Active](https://img.shields.io/badge/Status-Active-brightgreen.svg)]()
[![API: Gemini](https://img.shields.io/badge/API-Google%20Gemini-blue.svg)](https://ai.google.dev/)

---

## 🎯 Overview

Personal Finance Categorizer is an intelligent financial analysis system that automatically categorizes your bank transactions, detects unusual spending patterns, and generates actionable insights. Powered by Google Gemini AI, it transforms raw bank statements into meaningful financial intelligence—all with a beautiful web interface.

**Perfect for:**
- Students tracking personal expenses
- Freelancers managing multiple income streams
- Anyone wanting automated spending analysis
- Financial enthusiasts building data-driven habits
- Teams managing shared finances

---

## ✨ Features

### Core Functionality
- **🤖 AI-Powered Categorization** – Google Gemini automatically classifies transactions
- **🔍 Anomaly Detection** – Identifies unusual spending patterns and outliers
- **📊 Beautiful Dashboard** – Real-time spending visualization and analytics
- **💾 Smart Learning** – System learns from your corrections over time
- **📥 Multi-Format Support** – Handle various bank statement formats (standard & custom Indian)
- **📤 Export Reports** – Generate CSV and JSON reports
- **💱 Multi-Currency Support** – Auto-detects and handles different currencies
- **⚡ Fast Processing** – Batch process hundreds of transactions efficiently

### Dashboard Features

**📊 Dashboard Tab**
- Real-time spending metrics
- Category breakdown with percentages
- Top merchants by spending
- Transaction statistics (avg, median, range)
- Visual spending distribution

**⚠️ Anomalies Tab**
- High, medium, low severity flags
- Unusual amount detection
- New spending category alerts
- High-frequency spending days
- Detailed anomaly reasoning

**💾 Export Tab**
- Download categorized CSV
- JSON dashboard data
- Learn from corrections
- View learned patterns

**📤 Upload Tab**
- Simple CSV upload
- Real-time data preview
- One-click analysis button
- Progress tracking

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ ([Download](https://www.python.org/downloads/))
- 4GB+ RAM
- Google Gemini API key (free tier available)
- pip package manager

### 5-Minute Setup

**1. Clone repository**
```bash
git clone https://github.com/yourusername/personal-finance-categorizer.git
cd personal-finance-categorizer
```

**2. Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

**3. Install dependencies**
```bash
pip install -r finance_requirements.txt
```

**4. Get Gemini API Key**
- Visit [https://ai.google.dev/](https://ai.google.dev/)
- Click "Get API Key"
- Create new project (if needed)
- Copy API key

**5. Set up environment**

Create `.env` file in project root:
```env
GEMINI_API_KEY=your-api-key-here
```

Or set as environment variable:
```bash
export GEMINI_API_KEY="your-api-key-here"
```

**6. (Optional) Test your setup**
```bash
python diagnose_api_key.py
```

**7. Launch dashboard**
```bash
streamlit run finance_05_dashboard.py
```

Open **http://localhost:8501** in your browser. ✅

---

## 📦 Project Structure

```
personal-finance-categorizer/
│
├── Core Modules
├── finance_01_categorizer.py          # Gemini AI categorization engine
├── finance_02_anomaly_detector.py     # Anomaly detection system
├── finance_03_csv_handler.py          # Standard CSV parsing
├── finance_03_csv_handler_CUSTOM.py   # Indian bank format handling
├── finance_04_report_generator.py     # Report generation & export
├── finance_05_dashboard.py            # Main Streamlit dashboard
│
├── Utilities
├── analyze_bank_statement_CUSTOM.py   # CLI analyzer (custom format)
├── diagnose_api_key.py                # API key validation tool
│
├── Configuration & Docs
├── finance_requirements.txt           # Python dependencies
├── .env.example                       # Environment template
├── FINANCE_SETUP.md                   # Detailed setup guide
└── README.md                          # This file
│
├── Generated Data (auto-created)
├── data/
│   └── learned_categories.json        # User corrections
├── reports/
│   ├── categorized_transactions.csv   # Analyzed data
│   └── dashboard_data.json            # Dashboard state
│
└── Test Files
    └── bankstatements.csv             # Sample (add your own)
```

---

## 🔧 Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **LLM API** | Google Gemini 2.0 Flash | Transaction categorization |
| **Web UI** | Streamlit | Interactive dashboard |
| **Data Processing** | Pandas | CSV handling & analysis |
| **Environment** | python-dotenv | Secure API key management |
| **Analysis** | Statistics (built-in) | Anomaly detection |
| **Export** | JSON, CSV | Report generation |

---

## 📋 Module Overview

### 01. Categorizer (`finance_01_categorizer.py`)
- Uses Google Gemini to classify transactions
- Learns from user corrections
- Caches learned categories
- Returns: category, confidence, reasoning

```python
categorizer = FinanceCategorizer(api_key=api_key)
result = categorizer.categorize_transaction(
    amount=45.50,
    description="Starbucks Coffee",
    date="2024-07-08"
)
# Returns: {category: "Food", confidence: 0.95, ...}
```

### 02. Anomaly Detector (`finance_02_anomaly_detector.py`)
- Detects outlier amounts (2+ std deviations)
- Identifies new spending categories
- Flags high-frequency spending days
- Severity levels: high, medium, low

```python
detector = AnomalyDetector(window_size=20)
anomalies = detector.detect_all_anomalies(transactions)
```

### 03. CSV Handler (`finance_03_csv_handler.py`)
- Auto-detects CSV format
- Extracts: date, description, amount
- Auto-detects currency
- Parses dates intelligently

```python
handler = CSVHandler()
transactions = handler.load_csv("bankstatements.csv")
# Returns: [{date, description, amount}, ...]
```

### 03. Custom Handler (`finance_03_csv_handler_CUSTOM.py`)
- Handles Indian bank format: `date,DrCr,amount,balance,mode,name`
- Converts debits (negative) and credits (positive)
- Perfect for HDFC, ICICI, Axis, SBI exports

```python
handler = CustomBankStatementHandler()
transactions = handler.load_custom_format("bankstatements.csv")
```

### 04. Report Generator (`finance_04_report_generator.py`)
- Calculates spending by category
- Finds top merchants
- Generates statistics
- Exports CSV & JSON

```python
reporter = ReportGenerator(currency='USD')
report_data = reporter.generate_dashboard_data(
    categorized_txns, 
    anomalies
)
reporter.save_dashboard_data(report_data)
```

### 05. Dashboard (`finance_05_dashboard.py`)
- Streamlit web interface
- 4 main tabs: Upload, Dashboard, Anomalies, Export
- Real-time analysis
- Interactive visualizations

---

## 📊 Workflow

### Step 1: Prepare Data
Export bank statement as CSV from your bank:
```
Date,Description,Amount
2024-07-08,Starbucks Coffee,-45.50
2024-07-08,Salary Deposit,5000.00
2024-07-07,Amazon Purchase,-89.99
```

### Step 2: Upload & Analyze
1. Open dashboard
2. Go to "Upload & Analyze" tab
3. Upload CSV
4. Click "ANALYSE" button
5. Wait for processing (~30 seconds for 100 transactions)

### Step 3: Review Results
- **Dashboard** – See spending patterns
- **Anomalies** – Check unusual transactions
- **Export** – Download or learn corrections

### Step 4: Improve (Optional)
- Find wrong category
- Select transaction
- Enter correct category
- Click "Learn"
- AI remembers next time

---

## 💡 Usage Examples

### Example 1: Analyze Monthly Statement
```bash
# Have: Sep_2024_statement.csv
streamlit run finance_05_dashboard.py
# Upload file → click ANALYSE → review results
```

### Example 2: Categorize Specific Transactions
```python
from finance_01_categorizer import FinanceCategorizer

categorizer = FinanceCategorizer(api_key="your-key")
result = categorizer.categorize_transaction(
    amount=89.99,
    description="Amazon Purchase",
    date="2024-07-07"
)
print(f"Category: {result['category']}")
print(f"Confidence: {result['confidence']:.0%}")
print(f"Reasoning: {result['reasoning']}")
```

### Example 3: Detect Anomalies in Bulk
```python
from finance_02_anomaly_detector import AnomalyDetector

detector = AnomalyDetector()
anomalies = detector.detect_all_anomalies(transactions)

for anom in anomalies:
    print(f"🚨 {anom['reason']} (Severity: {anom['severity']})")
```

### Example 4: Custom Indian Bank Format
```python
from finance_03_csv_handler_CUSTOM import CustomBankStatementHandler

handler = CustomBankStatementHandler()
txns = handler.load_custom_format("HDFC_statement.csv")
# Handles: date, DrCr, amount, balance, mode, name
```

---

## 📋 CSV Format Support

### Standard Format (Recommended)
```csv
Date,Description,Amount
2024-07-08,Starbucks,-45.50
2024-07-08,Salary,5000.00
```

**Supported column names:**
- Date: "Date", "Transaction Date", "Posted"
- Description: "Description", "Merchant", "Details", "Note"
- Amount: "Amount", "Debit", "Credit", "Withdrawal", "Deposit"

### Indian Bank Format (Custom Handler)
```csv
date,DrCr,amount,balance,mode,name
2022-01-01,Db,10000.0,473292.87,ATM,
2022-01-02,Cr,5000.0,483292.87,NEFT,SALARY
```

**Uses custom handler:**
```python
from finance_03_csv_handler_CUSTOM import CustomBankStatementHandler
handler = CustomBankStatementHandler()
transactions = handler.load_custom_format("your_file.csv")
```

---

## 🔒 Security & Privacy

✅ **Local Processing** – All data stays on your machine  
✅ **API Key Secure** – Uses .env file (not in git)  
✅ **No Tracking** – Zero analytics or telemetry  
✅ **Your Data** – Complete ownership  

**Note:** Gemini API calls are sent to Google. All other processing is local.

---

## ⚡ Performance

| Operation | Time | Notes |
|-----------|------|-------|
| **Upload CSV** | <1s | File reading |
| **Categorize 100 txns** | ~30s | Gemini API calls |
| **Detect anomalies** | ~2s | Local processing |
| **Generate report** | <1s | Data aggregation |
| **Dashboard load** | <1s | Streamlit rendering |
| **Total first run** | ~45s | End-to-end |

### Optimization Tips
- Use **Gemini 2.0 Flash** (faster model)
- Batch transactions together
- Limit to last 1-3 months for analysis
- Use smaller chunks if quota is tight

---

## 🐛 Troubleshooting

### "GEMINI_API_KEY not found"
```bash
# Check .env exists:
cat .env

# If missing, create:
echo 'GEMINI_API_KEY=your-key-here' > .env

# Or set environment variable:
export GEMINI_API_KEY="your-key"
```

### "API Error: 429 RESOURCE_EXHAUSTED"
- Free tier quota exceeded
- Wait 24 hours (resets daily)
- Or upgrade to paid plan at https://ai.google.dev/
- Check usage: https://ai.google.dev/usage

### "ModuleNotFoundError: No module named 'pandas'"
```bash
# Reinstall dependencies:
pip install --upgrade -r finance_requirements.txt
```

### "Cannot detect CSV format"
- Verify CSV has these columns: Date, Description, Amount
- Try renaming columns if using different names
- Use custom handler for Indian bank formats

### "Streamlit won't start"
```bash
# Try different port:
streamlit run finance_05_dashboard.py --server.port 8502

# Clear Streamlit cache:
streamlit cache clear
```

### "No transactions loaded"
- Check CSV file is not empty
- Verify date and amount columns have data
- Try CSV preview in dashboard first

See [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) for more solutions.

---

## 📊 Category Taxonomy

Default categories (customizable):

```
🍔 Food & Dining
    - Restaurants, Cafes, Grocery, Delivery

🚗 Transportation
    - Uber/Lyft, Gas, Parking, Public Transit

🏠 Utilities
    - Electricity, Water, Internet, Phone

🎬 Entertainment
    - Movies, Games, Hobbies, Events

🛍️ Shopping
    - Clothing, Electronics, Home, Gifts

🏥 Healthcare
    - Medical, Pharmacy, Fitness, Wellness

📚 Education
    - Tuition, Books, Courses, Training

📱 Subscription
    - Netflix, Spotify, Software, Memberships

💸 Transfer
    - Bank transfers, P2P payments, Investments

❓ Other
    - Anything else
```

---

## 🛣️ Roadmap

- [x] Phase 1: Basic categorization (Gemini)
- [x] Phase 2: Anomaly detection
- [x] Phase 3: Streamlit dashboard
- [x] Phase 4: Learn from corrections
- [ ] Phase 5: Multi-currency support
- [ ] Phase 6: Recurring transaction detection
- [ ] Phase 7: Budget tracking
- [ ] Phase 8: Mobile app
- [ ] Phase 9: Multi-user support
- [ ] Phase 10: API endpoints

---

## 📈 Example Output

### Dashboard Metrics
```
💳 Total Transactions: 127
💰 Total Spent: $2,456.32
📊 Average: $19.34
📉 Median: $15.00
📊 Range: $2.50 - $89.99
```

### Category Breakdown
```
🍔 Food & Dining: $456.23 (18.6%) - 28 transactions
🛍️ Shopping: $389.45 (15.9%) - 12 transactions
🚗 Transportation: $234.12 (9.5%) - 18 transactions
📱 Subscription: $189.99 (7.7%) - 6 transactions
```

### Anomalies Found
```
🔴 HIGH: Amazon Purchase ($89.99) - 2.5x usual shopping amount
🟠 MEDIUM: Multiple ATM withdrawals ($450 total) on same day
🔵 LOW: First transaction in "Home Improvement" category
```

---

## 🤝 Contributing

Contributions welcome! 

1. Fork the repo
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

### Ideas for contributions:
- Additional category types
- New anomaly detection algorithms
- Budget goal tracking
- Recurring transaction grouping
- Export to other formats (PDF, Excel)
- Mobile app companion
- API endpoints

See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

---

## 📝 License

This project is licensed under the MIT License - see [LICENSE](./LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Google Gemini API** – Transaction categorization
- **Streamlit** – Web framework
- **Pandas** – Data manipulation
- **Python Community** – Amazing tools and libraries

---

## 📞 Support & Contact

- **Issues:** [GitHub Issues](https://github.com/yourusername/personal-finance-categorizer/issues)
- **Discussions:** [GitHub Discussions](https://github.com/yourusername/personal-finance-categorizer/discussions)
- **Email:** your.email@example.com
- **Twitter:** [@yourhandle](https://twitter.com/yourhandle)

---

## 💡 Tips & Best Practices

### For Best Results
1. **Use consistent descriptions** – Similar formats for merchants
2. **Regular sync** – Add statements monthly
3. **Learn corrections** – Teach the AI your preferences
4. **Review anomalies** – Verify legitimate unusual spending
5. **Export reports** – Keep CSV copies for records

### Privacy Recommendations
- Keep `.env` file out of git
- Don't share API keys
- Consider using separate test account
- Review Gemini API privacy policy

### Optimization
- Use 3-month rolling window for analysis
- Archive old statements separately
- Clean up duplicate entries first
- Use custom handler for your bank format

---

## 🎯 Next Steps

1. **Get Started** – Follow Quick Start above
2. **Upload Data** – Try with real bank statement
3. **Review Results** – Check categorization accuracy
4. **Teach AI** – Correct any wrong categories
5. **Export Report** – Download analyzed data
6. **Track Habits** – Repeat monthly for insights

---

## ⭐ Show Your Support

If this helped you understand your finances:
- ⭐ Star this repo
- 🔄 Share with friends
- 💬 Provide feedback
- 🐛 Report issues
- 🤝 Contribute improvements

---

<div align="center">

**Made with ❤️ by [RAze](https://github.com/yourusername)**

💰 **Understand your spending, improve your finances** 📊

[Star](https://github.com/yourusername/personal-finance-categorizer) · [Fork](https://github.com/yourusername/personal-finance-categorizer/fork) · [Watch](https://github.com/yourusername/personal-finance-categorizer/subscription)

</div>
