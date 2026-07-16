"""
Personal Finance Categorizer - Streamlit Dashboard (Custom Format)
Web interface for Indian bank statements: date,DrCr,amount,balance,mode,name
Author: RAze
Date: 2026-07-16
"""

import streamlit as st
import pandas as pd
import json
from pathlib import Path
import os
from datetime import datetime

# Import our modules
from finance_01_categorizer import FinanceCategorizer
from finance_02_anomaly_detector import AnomalyDetector
from finance_03_csv_handler_CUSTOM import CustomBankStatementHandler
from finance_04_report_generator import ReportGenerator

st.set_page_config(
    page_title="💰 Finance Categorizer",
    layout="wide",
    page_icon="💰",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .metric-card { background-color: #f0f2f6; padding: 1rem; border-radius: 0.5rem; }
    .category-box { background-color: #e8f4f8; padding: 1rem; border-radius: 0.5rem; margin: 0.5rem 0; }
    .anomaly-high { background-color: #ffcccc; padding: 1rem; border-radius: 0.5rem; border-left: 4px solid #cc0000; }
    .anomaly-medium { background-color: #fff3cd; padding: 1rem; border-radius: 0.5rem; border-left: 4px solid #ff9800; }
    .anomaly-low { background-color: #e7f3ff; padding: 1rem; border-radius: 0.5rem; border-left: 4px solid #2196f3; }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# INITIALIZATION
# ============================================================================

@st.cache_resource
def init_systems():
    """Initialize all systems."""
    try:
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            return None, None, None, None
        
        categorizer = FinanceCategorizer(api_key=api_key)
        detector = AnomalyDetector()
        csv_handler = CustomBankStatementHandler()
        reporter = ReportGenerator(currency='INR')
        
        return categorizer, detector, csv_handler, reporter
    except Exception as e:
        st.error(f"❌ Error initializing: {e}")
        return None, None, None, None

# Initialize
categorizer, detector, csv_handler, reporter = init_systems()

if categorizer is None:
    st.error("❌ GEMINI_API_KEY not set. Set it as environment variable.")
    st.info("Example: export GEMINI_API_KEY='your-key'")
    st.stop()

# ============================================================================
# SIDEBAR
# ============================================================================

with st.sidebar:
    st.title("⚙️ Settings")
    st.divider()
    
    # Window size selector
    st.subheader("🔍 Anomaly Detection")
    window_size = st.radio(
        "Transactions to analyze:",
        options=[10, 20, 50, "All"],
        help="How many recent transactions to analyze for anomalies"
    )
    
    if window_size != "All":
        detector.window_size = window_size
    
    st.divider()
    
    # Info
    st.subheader("ℹ️ About")
    st.write("""
**Personal Finance Categorizer**

Indian Bank Statement Analyzer
- Upload bank statement CSV
- AI categorizes transactions
- Detects unusual spending
- Learn from corrections

Powered by Google Gemini
    """)

# ============================================================================
# MAIN TABS
# ============================================================================

tab1, tab2, tab3, tab4 = st.tabs(["📤 Upload & Analyze", "📊 Dashboard", "⚠️ Anomalies", "💾 Export"])

# ============================================================================
# TAB 1: UPLOAD & ANALYZE
# ============================================================================

with tab1:
    st.title("📤 Upload Bank Statement & Analyze")
    
    # File upload
    uploaded_file = st.file_uploader("Choose CSV file:", type="csv")
    
    if uploaded_file is not None:
        st.info(f"📁 File uploaded: {uploaded_file.name}")
        
        # Show preview of uploaded CSV
        try:
            preview_df = pd.read_csv(uploaded_file)
            st.subheader("📋 Preview of your data (first 5 rows):")
            st.dataframe(preview_df.head(5), use_container_width=True)
        except Exception as e:
            st.warning(f"Could not preview file: {e}")
        
        # Analyse button
        if st.button("🚀 ANALYSE", use_container_width=True, type="primary"):
            with st.spinner("⏳ Processing your data..."):
                try:
                    # Save temporarily
                    temp_path = Path(f"temp_{uploaded_file.name}")
                    with open(temp_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    # Load CSV with custom format
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    status_text.text("📂 Loading transactions...")
                    transactions = csv_handler.load_custom_format(temp_path)
                    currency = csv_handler.currency
                    symbol = csv_handler.get_currency_symbol()
                    
                    if not transactions:
                        st.error("❌ No transactions found in CSV")
                        temp_path.unlink()
                    else:
                        st.success(f"✅ Loaded {len(transactions)} transactions")
                        
                        # Categorize
                        progress_bar.progress(20)
                        status_text.text(f"🤖 Categorizing {len(transactions)} transactions with AI...")
                        categorized = categorizer.categorize_batch(transactions)
                        
                        # Detect anomalies
                        progress_bar.progress(60)
                        status_text.text("🔍 Detecting anomalies...")
                        anomalies = detector.detect_all_anomalies(categorized)
                        
                        # Flag transactions with anomalies
                        anomaly_descs = set()
                        for anom in anomalies:
                            if 'transaction' in anom:
                                anomaly_descs.add(anom['transaction'].get('description'))
                        
                        for txn in categorized:
                            txn['flagged'] = txn['description'] in anomaly_descs
                        
                        # Generate report
                        progress_bar.progress(80)
                        status_text.text("📊 Generating report...")
                        report_data = reporter.generate_dashboard_data(categorized, anomalies)
                        
                        # Save
                        reporter.save_dashboard_data(report_data)
                        reporter.export_to_csv(categorized)
                        
                        progress_bar.progress(100)
                        status_text.text("✅ Analysis complete!")
                        
                        # Store in session
                        st.session_state.categorized = categorized
                        st.session_state.anomalies = anomalies
                        st.session_state.report_data = report_data
                        st.session_state.currency = currency
                        st.session_state.symbol = symbol
                        
                        st.success("✅ Analysis Complete! Check the Dashboard tab for results.")
                        
                        # Clean up
                        temp_path.unlink()
                
                except Exception as e:
                    st.error(f"❌ Error during analysis: {str(e)}")
    
    else:
        st.info("👆 Upload your bank statement CSV to get started")
        
        # Show expected format
        st.divider()
        st.subheader("📋 Expected CSV Format")
        st.write("Your bank statement should have these columns:")
        st.code("""date,DrCr,amount,balance,mode,name,Day,Month,Year,Tday
2022-01-01,Db,10000.0,473292.87,ATM,,01,01,2022,1
2022-01-02,Db,930.0,462362.87,UPI,AYUBRAJE,02,01,2022,2
2022-01-07,Db,2000.0,460362.87,UPI,ABUTALAH,07,01,2022,3
2022-01-10,Cr,5000.0,465362.87,NEFT,,10,01,2022,4""", language="csv")

# ============================================================================
# TAB 2: DASHBOARD
# ============================================================================

with tab2:
    st.title("📊 Spending Dashboard")
    
    if 'categorized' not in st.session_state:
        st.info("👈 Upload a file and click 'ANALYSE' in the Upload tab first")
    else:
        data = st.session_state.report_data
        symbol = st.session_state.symbol
        stats = data['statistics']
        categories = data['by_category']
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("💳 Transactions", stats['total_transactions'])
        with col2:
            st.metric("💰 Total Spent", f"{symbol}{abs(stats['total_spent']):.2f}")
        with col3:
            st.metric("📊 Average", f"{symbol}{stats['average_transaction']:.2f}")
        with col4:
            st.metric("⚠️ Anomalies", data['anomaly_count'])
        
        st.divider()
        
        # Categories
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("📈 Spending by Category")
            
            for cat, info in categories.items():
                st.markdown(f"""
<div class="category-box">
<b>{cat}</b><br/>
{symbol}{info['total']:.2f} ({info['percentage']:.1f}%)<br/>
<small>{info['count']} transactions • Avg {symbol}{info['avg']:.2f}</small>
</div>
""", unsafe_allow_html=True)
        
        with col2:
            st.subheader("📊 Distribution")
            
            # Bar chart
            df = pd.DataFrame({
                'Category': categories.keys(),
                'Amount': [info['total'] for info in categories.values()]
            })
            
            st.bar_chart(df.set_index('Category'))
        
        st.divider()
        
        # Top merchants
        st.subheader("💳 Top Merchants")
        top_merchants = data['top_merchants']
        
        for desc, info in list(top_merchants.items())[:10]:
            st.write(f"**{desc}**: {symbol}{info['total']:.2f} ({info['count']} times)")

# ============================================================================
# TAB 3: ANOMALIES
# ============================================================================

with tab3:
    st.title("⚠️ Unusual Spending Detected")
    
    if 'anomalies' not in st.session_state or len(st.session_state.anomalies) == 0:
        st.info("✅ No anomalies detected!")
    else:
        data = st.session_state.report_data
        anomalies = st.session_state.anomalies
        symbol = st.session_state.symbol
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🔴 High", data['high_severity_count'])
        with col2:
            st.metric("🟠 Medium", data['medium_severity_count'])
        with col3:
            st.metric("🔵 Low", data['low_severity_count'])
        
        st.divider()
        
        # List anomalies
        for i, anom in enumerate(anomalies):
            severity = anom.get('severity', 'low')
            css_class = f"anomaly-{severity}"
            
            if 'transaction' in anom:
                txn = anom['transaction']
                st.markdown(f"""
<div class="{css_class}">
<b>{txn.get('description')}</b><br/>
Amount: {symbol}{abs(txn.get('amount', 0)):.2f}<br/>
Date: {txn.get('date', 'Unknown')}<br/>
Category: {txn.get('category', 'Other')}<br/>
<small>Reason: {anom['reason']}</small>
</div>
""", unsafe_allow_html=True)
            else:
                st.markdown(f"""
<div class="{css_class}">
<b>{anom.get('reason')}</b>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# TAB 4: EXPORT
# ============================================================================

with tab4:
    st.title("💾 Export & Learn")
    
    if 'categorized' not in st.session_state:
        st.info("👈 Upload a file and click 'ANALYSE' first")
    else:
        categorized = st.session_state.categorized
        symbol = st.session_state.symbol
        
        st.subheader("📥 Download CSV Report")
        
        # Generate CSV
        csv_data = ""
        csv_data += "Date,Description,Amount,Category,Confidence,Flagged\n"
        
        for txn in categorized:
            flagged = "Yes" if txn.get('flagged') else "No"
            csv_data += f"{txn.get('date')},{txn.get('description')},{txn.get('amount')},{txn.get('category')},{txn.get('confidence', 0):.0%},{flagged}\n"
        
        st.download_button(
            label="📥 Download CSV",
            data=csv_data,
            file_name=f"categorized_transactions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
        
        st.divider()
        
        st.subheader("🤖 Learn from Corrections")
        
        st.info("Found a wrong category? Teach the AI!")
        
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            wrong_txn = st.selectbox(
                "Select transaction:",
                [f"{t['description']} ({t['category']})" for t in categorized[:10]]
            )
        
        with col2:
            correct_category = st.text_input("Correct category:")
        
        with col3:
            if st.button("✅ Learn"):
                if correct_category and wrong_txn:
                    desc = wrong_txn.split(" (")[0]
                    categorizer.learn_correction(desc, correct_category)
                    st.success(f"✅ Learned: {desc} → {correct_category}")
        
        st.divider()
        
        st.subheader("📊 Learned Categories")
        learned = categorizer.get_learned_stats()
        
        if learned['total_learned'] > 0:
            for desc, category in list(learned['learned_items'].items())[:5]:
                st.write(f"- {desc} → **{category}**")
        else:
            st.info("No learned categories yet")

# ============================================================================
# FOOTER
# ============================================================================

st.divider()
st.caption("💰 Personal Finance Categorizer | Indian Bank Statements | Powered by Google Gemini | Made by RAze")
