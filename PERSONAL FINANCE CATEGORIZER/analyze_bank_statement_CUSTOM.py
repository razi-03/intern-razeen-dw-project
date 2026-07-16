"""
💰 Bank Statement Analyzer - Custom Format Version
Analyzes Indian bank statements with format: date,DrCr,amount,balance,mode,name
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
env_path = Path('.env')
if env_path.exists():
    print(f"📄 Loading .env file...")
    load_dotenv(env_path)
    print(f"   ✅ .env loaded")
else:
    print(f"❌ .env file not found")
    sys.exit(1)

# Verify API key
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    print(f"❌ GEMINI_API_KEY not in .env")
    sys.exit(1)

print(f"✅ API Key loaded")

# Import modules
print(f"\n📦 Importing modules...")
try:
    from finance_01_categorizer import FinanceCategorizer
    from finance_02_anomaly_detector import AnomalyDetector
    from finance_03_csv_handler_CUSTOM import CustomBankStatementHandler
    from finance_04_report_generator import ReportGenerator
    print(f"   ✅ All modules imported")
except ImportError as e:
    print(f"   ❌ Import error: {e}")
    sys.exit(1)

def process_transactions(csv_path):
    """Process transactions with full analysis pipeline"""
    
    print(f"\n" + "="*80)
    print(f"💰 PERSONAL FINANCE ANALYZER - Indian Bank Statement Format")
    print(f"="*80)
    
    # Initialize systems
    print(f"\n🚀 Initializing systems...")
    try:
        categorizer = FinanceCategorizer(api_key=api_key)
        detector = AnomalyDetector()
        csv_handler = CustomBankStatementHandler()
        reporter = ReportGenerator(currency='INR')
        print(f"   ✅ All systems ready")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        sys.exit(1)
    
    # Load CSV with custom format
    print(f"\n📂 Loading transactions: {csv_path}")
    try:
        transactions = csv_handler.load_custom_format(csv_path)
        if not transactions:
            print(f"   ❌ No transactions loaded")
            return
        print(f"   ✅ Loaded {len(transactions)} transactions")
        print(f"   💱 Detected currency: {csv_handler.currency}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    # Categorize
    print(f"\n🤖 Categorizing {len(transactions)} transactions with AI...")
    try:
        categorized = categorizer.categorize_batch(transactions)
        print(f"   ✅ Categorized {len(categorized)} transactions")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    # Detect anomalies
    print(f"\n🔍 Detecting anomalies...")
    try:
        anomalies = detector.detect_all_anomalies(categorized)
        print(f"   ✅ Found {len(anomalies)} anomalies")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    # Flag anomalies
    anomaly_descs = {anom['transaction'].get('description') 
                     for anom in anomalies if 'transaction' in anom}
    for txn in categorized:
        txn['flagged'] = txn['description'] in anomaly_descs
    
    # Generate report
    print(f"\n📊 Generating report...")
    try:
        report_data = reporter.generate_dashboard_data(categorized, anomalies)
        reporter.save_dashboard_data(report_data)
        print(f"   ✅ Report saved to reports/dashboard_data.json")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    # Export to CSV
    print(f"\n📥 Exporting results to CSV...")
    try:
        csv_output = reporter.export_to_csv(categorized)
        print(f"   ✅ Exported to {csv_output}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    # Print summary
    print(f"\n")
    reporter.print_summary(report_data)
    
    print(f"\n" + "="*80)
    print(f"✅ ANALYSIS COMPLETE!")
    print(f"="*80)
    print(f"\n📁 Output files created:")
    print(f"   - reports/categorized_transactions.csv")
    print(f"   - reports/dashboard_data.json")

def main():
    """Main entry point"""
    print(f"\n" + "="*80)
    print(f"💰 INDIAN BANK STATEMENT ANALYZER")
    print(f"="*80)
    
    # Default file name
    raw_csv = "bankstatements.csv"
    
    # Check if raw CSV exists
    if not Path(raw_csv).exists():
        print(f"\n❌ File not found: {raw_csv}")
        print(f"   Place your bank statement CSV in the current directory")
        print(f"\n   Expected format:")
        print(f"   date,DrCr,amount,balance,mode,name,Day,Month,Year,Tday")
        sys.exit(1)
    
    # Process
    print(f"\n" + "-"*80)
    print(f"ANALYZING YOUR BANK STATEMENT")
    print(f"-"*80)
    process_transactions(raw_csv)

if __name__ == "__main__":
    main()
