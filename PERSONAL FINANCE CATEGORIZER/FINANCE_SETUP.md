# 💰 Personal Finance Categorizer - Setup Guide

## 📋 What You're Building

A web app that:
- Uploads your bank statement (CSV)
- AI categorizes transactions automatically
- Detects unusual spending
- Learn from corrections
- Export reports

---

## 🚀 Quick Start (5 Steps)

### **Step 1: Get Gemini API Key**
```bash
# Visit: https://ai.google.dev/
# Create free account
# Get API key from console
```

### **Step 2: Install Python Packages**
```bash
pip install -r finance_requirements.txt
```

### **Step 3: Set API Key**
```bash
export GEMINI_API_KEY="your-api-key-here"
```

Or create `.env` file:
```
GEMINI_API_KEY=your-api-key-here
```

### **Step 4: Test Scripts (Optional)**
```bash
# Test categorizer
python finance_01_categorizer.py

# Test anomaly detector
python finance_02_anomaly_detector.py

# Test CSV handler
python finance_03_csv_handler.py

# Test report generator
python finance_04_report_generator.py
```

### **Step 5: Launch Dashboard**
```bash
streamlit run finance_05_dashboard.py
```

Then visit: **http://localhost:8501**

---

## 📁 File Structure

```
finance-categorizer/
├── finance_01_categorizer.py       ← Gemini AI categorization
├── finance_02_anomaly_detector.py  ← Detect unusual spending
├── finance_03_csv_handler.py       ← Read bank statements
├── finance_04_report_generator.py  ← Generate reports
├── finance_05_dashboard.py         ← Web interface
├── finance_requirements.txt        ← Dependencies
│
├── data/
│   └── learned_categories.json    ← Learned corrections
│
└── reports/
    ├── categorized_transactions.csv
    └── dashboard_data.json
```

---

## 💳 How to Use

### 1. Prepare Your Bank Statement

Export from your bank as CSV with columns:
- Date
- Description
- Amount

**Example:**
```csv
Date,Description,Amount
2024-07-08,Starbucks Coffee,-45.50
2024-07-08,Salary Deposit,5000.00
2024-07-07,Amazon Purchase,-89.99
```

### 2. Upload to Dashboard

1. Open http://localhost:8501
2. Go to "Upload & Analyze" tab
3. Upload CSV
4. Wait for categorization

### 3. Review Results

- **Dashboard**: See spending by category
- **Anomalies**: Check unusual transactions
- **Export**: Download CSV or learn corrections

### 4. Teach AI

- Find wrong category
- Select transaction
- Enter correct category
- Click "Learn"
- AI remembers for next time

---

## 🤖 What Each Script Does

| Script | Purpose |
|--------|---------|
| **01_categorizer.py** | Uses Gemini AI to categorize transactions |
| **02_anomaly_detector.py** | Finds unusual spending patterns |
| **03_csv_handler.py** | Reads CSV, detects currency automatically |
| **04_report_generator.py** | Creates reports and exports |
| **05_dashboard.py** | Streamlit web interface |

---

## ⚙️ Settings in Dashboard

### Anomaly Detection Window
Choose how many recent transactions to analyze:
- **10**: Quick, recent transactions only
- **20**: Normal analysis
- **50**: Deeper analysis
- **All**: All transactions

---

## 💡 Features

✅ **Auto-Categorize**
- Gemini analyzes each transaction
- Smart matching with descriptions

✅ **Detect Anomalies**
- Amount outliers (2x average)
- New categories
- High-frequency spending days

✅ **Learn from Corrections**
- User marks wrong categories
- AI remembers for next time
- Improves over time

✅ **Multi-Currency**
- Auto-detects currency
- Shows correct symbol

✅ **Export Reports**
- CSV with all data
- Dashboard JSON
- Full audit trail

---

## 🐛 Troubleshooting

### "GEMINI_API_KEY not found"
```bash
# Set environment variable
export GEMINI_API_KEY="sk-..."

# Or create .env file
echo 'GEMINI_API_KEY=sk-...' > .env
```

### "Cannot detect CSV format"
Make sure CSV has columns named:
- Date (or similar)
- Description (or merchant, details)
- Amount (or debit, credit)

### "No anomalies detected"
- Upload file with more transactions
- Use "All" window size for deeper analysis
- Some datasets have normal spending

### "Streamlit won't start"
```bash
# Try different port
streamlit run finance_05_dashboard.py --server.port 8502
```

---

## 📊 Output Files

After running:

**CSV Report**
- Categorized transactions
- All columns for Excel/Google Sheets
- Ready to analyze further

**Dashboard Data**
- JSON format
- Categories with totals
- Anomalies flagged
- Statistics

**Learned Categories**
- JSON file
- Your corrections
- Improves over time

---

## 🎯 Example Workflow

1. **Export statement from bank** → CSV file
2. **Upload to dashboard** → "Upload & Analyze" tab
3. **Review categories** → Dashboard tab
4. **Check anomalies** → "Anomalies" tab
5. **Teach corrections** → Export tab → "Learn"
6. **Download report** → Export tab → "Download CSV"

---

## 💰 Cost

- **Gemini API**: FREE (you get 60 requests/min free)
- **Streamlit**: FREE (local)
- **Everything**: 100% FREE

---

## 🎉 You're Done!

You now have:
- ✅ AI-powered transaction categorizer
- ✅ Anomaly detection system
- ✅ Beautiful web dashboard
- ✅ CSV export functionality
- ✅ Learning system that improves over time

**Start uploading bank statements!** 💳

---

Built with ❤️ by RAze
