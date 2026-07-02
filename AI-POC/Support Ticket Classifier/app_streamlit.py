"""
Streamlit Interactive Demo App
Purpose: Interactive demonstration of ticket classifier POC
Author: RAze
Date: 2026-07-01
Run with: streamlit run app_streamlit.py
"""

import streamlit as st
import pandas as pd
import pickle
import json
from datetime import datetime
import os

# Configure page
st.set_page_config(
    page_title="Support Ticket Classifier POC",
    page_icon="🎫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .metric-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .prediction-box {
        background-color: #e8f4f8;
        padding: 15px;
        border-left: 4px solid #0066cc;
        border-radius: 5px;
        margin: 10px 0;
    }
    .confidence-high {
        color: #00aa00;
        font-weight: bold;
    }
    .confidence-med {
        color: #ff9900;
        font-weight: bold;
    }
    .confidence-low {
        color: #cc0000;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'classifier_loaded' not in st.session_state:
    st.session_state.classifier_loaded = False
    st.session_state.classifier = None
    st.session_state.df_processed = None
    st.session_state.evaluation_report = None

    # Apply any pending sample ticket BEFORE the widget is created
if 'pending_ticket' in st.session_state:
    st.session_state.ticket_input = st.session_state.pending_ticket
    del st.session_state.pending_ticket

@st.cache_resource
def load_models():
    """Load pre-trained models."""
    try:
        with open('category_classifier.pkl', 'rb') as f:
            classifier = pickle.load(f)
        return classifier
    except FileNotFoundError:
        return None

@st.cache_data
def load_data_and_report():
    """Load processed data and evaluation report."""
    try:
        df = pd.read_csv('data_processed_tickets.csv')
        df['created_at'] = pd.to_datetime(df['created_at'])
        
        with open('model_evaluation_report.json', 'r') as f:
            report = json.load(f)
        
        return df, report
    except FileNotFoundError:
        return None, None

def predict_category(classifier, text):
    """Predict category for ticket."""
    prediction = classifier.predict([text])[0]
    probability = classifier.predict_proba([text])[0]
    confidence = float(max(probability))
    return prediction, confidence

def predict_sentiment(text):
    """Rule-based sentiment prediction."""
    negative_words = [
        'bug', 'broken', 'crash', 'error', 'fail', 'problem', 'issue',
        'not working', 'urgent', 'asap', 'critical', 'losing', 'lost',
        'expensive', 'slow', 'stuck'
    ]
    positive_words = [
        'thanks', 'great', 'excellent', 'good', 'love', 'appreciate',
        'fantastic', 'amazing', 'best', 'perfect', 'awesome'
    ]
    
    text_lower = text.lower()
    neg_count = sum(1 for word in negative_words if word in text_lower)
    pos_count = sum(1 for word in positive_words if word in text_lower)
    
    if neg_count > pos_count:
        sentiment = 'Negative'
        confidence = min(0.99, 0.5 + (neg_count * 0.15))
    elif pos_count > neg_count:
        sentiment = 'Positive'
        confidence = min(0.99, 0.5 + (pos_count * 0.15))
    else:
        sentiment = 'Neutral'
        confidence = 0.7
    
    return sentiment, float(confidence)

def get_confidence_color(confidence):
    """Get color based on confidence level."""
    if confidence >= 0.85:
        return 'confidence-high'
    elif confidence >= 0.70:
        return 'confidence-med'
    else:
        return 'confidence-low'

# HEADER
st.title("Support Ticket Classifier")
st.caption("AI-Powered Ticket Classification POC by Razeen")
st.markdown("---")

# Load models and data
classifier = load_models()
df_processed, evaluation_report = load_data_and_report()

if classifier is None or df_processed is None:
    st.error("Models not found. Run Phase 1-3 first.")
    st.info("Run: python 01_data_generation.py && python 02_data_preprocessing.py && python 03_ml_pipeline.py")
    st.stop()

# SIDEBAR - Navigation
with st.sidebar:
    st.header("Navigation")
    page = st.radio(
        "Select page:",
        ["Live Classifier", "Model Performance", "Dataset Analysis", "About"]
    )

# PAGE 1: LIVE CLASSIFIER
if page == "Live Classifier":
    st.header("Live Classifier Demo")
    st.write("Enter a support ticket and see real-time classification:")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        ticket_text = st.text_area(
            "Support Ticket Description",
            height=150,
            placeholder="Example: I cannot login to my account and getting 500 error...",
            key="ticket_input"
        )
    
    with col2:
        st.write("")
        st.write("")
        predict_btn = st.button("Classify", use_container_width=True)
    
    if predict_btn and ticket_text.strip():
        with st.spinner("Analyzing ticket..."):
            category, cat_conf = predict_category(classifier, ticket_text)
            sentiment, sent_conf = predict_sentiment(ticket_text)
            
            # Determine priority based on category and sentiment
            if sentiment == 'Negative' and category in ['Bug', 'Billing']:
                priority = 'High'
            elif category == 'Bug':
                priority = 'Medium'
            else:
                priority = 'Low'
            
            st.write("")
            st.markdown("### Prediction Results:")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div class="prediction-box">
                    <h4>Category</h4>
                    <h3>{category}</h3>
                    <p>Confidence: <span class="{get_confidence_color(cat_conf)}">{cat_conf:.1%}</span></p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="prediction-box">
                    <h4>Sentiment</h4>
                    <h3>{sentiment}</h3>
                    <p>Confidence: <span class="{get_confidence_color(sent_conf)}">{sent_conf:.1%}</span></p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                priority_color = 'RED' if priority == 'High' else 'YELLOW' if priority == 'Medium' else 'GREEN'
                st.markdown(f"""
                <div class="prediction-box">
                    <h4>Priority</h4>
                    <h3>{priority}</h3>
                    <p>Auto-assigned</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.write("")
            st.success("Classification complete!")
    
    elif predict_btn and not ticket_text.strip():
        st.warning("Please enter a ticket description")
    
    # Sample tickets section
    st.write("")
    st.markdown("### Try Sample Tickets:")
    
    samples = {
        "Bug Report": "Cannot login to my account. Getting 500 error on login page.",
        "Feature Request": "Can we add dark mode to the platform? Many users have requested it.",
        "Billing Issue": "Why was I charged twice this month? This is urgent!",
        "Technical Support": "How do I connect my database to the platform?",
        "Positive Feedback": "Thanks for the amazing support! Your team is fantastic."
    }
    
    cols = st.columns(len(samples))
    for idx, (label, text) in enumerate(samples.items()):
        with cols[idx]:
            if st.button(label, use_container_width=True, key=f"sample_{idx}"):
                st.session_state.pending_ticket = text
                st.rerun()

# PAGE 2: MODEL PERFORMANCE
elif page == "Model Performance":
    st.header("Model Performance Metrics")
    
    if evaluation_report:
        report = evaluation_report
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            cat_metrics = report['category_classifier']['metrics']
            st.metric(
                "Category Accuracy",
                f"{cat_metrics['accuracy']:.1%}"
            )
        
        with col2:
            st.metric(
                "Category F1-Score",
                f"{cat_metrics['f1_weighted']:.1%}"
            )
        
        with col3:
            sent_metrics = report['sentiment_analyzer']['metrics']
            st.metric(
                "Sentiment Accuracy",
                f"{sent_metrics['accuracy']:.1%}"
            )
        
        st.markdown("---")
        
        # Detailed performance per category
        st.subheader("Per-Category Performance:")
        
        class_report = cat_metrics['classification_report']
        perf_data = []
        
        for category, metrics in class_report.items():
            if category not in ['accuracy', 'macro avg', 'weighted avg']:
                perf_data.append({
                    'Category': category,
                    'Precision': f"{metrics['precision']:.2%}",
                    'Recall': f"{metrics['recall']:.2%}",
                    'F1-Score': f"{metrics['f1-score']:.2%}",
                    'Samples': int(metrics['support'])
                })
        
        perf_df = pd.DataFrame(perf_data)
        st.dataframe(perf_df, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        st.subheader("Model Configuration:")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Category Classifier**")
            st.json(report['category_classifier']['hyperparameters'])
        
        with col2:
            st.write("**Sentiment Analyzer**")
            st.json({
                "type": report['sentiment_analyzer']['model_type'],
                "approach": "Keyword-based"
            })

# PAGE 3: DATASET ANALYSIS
elif page == "Dataset Analysis":
    st.header("Dataset Analysis")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Tickets", len(df_processed))
    with col2:
        st.metric("Avg Words/Ticket", f"{df_processed['word_count'].mean():.0f}")
    with col3:
        st.metric("Date Range", f"{(df_processed['created_at'].max() - df_processed['created_at'].min()).days}d")
    with col4:
        st.metric("Categories", df_processed['true_category'].nunique())
    
    st.markdown("---")
    
    # Distribution charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Category Distribution")
        cat_dist = df_processed['true_category'].value_counts()
        st.bar_chart(cat_dist)
    
    with col2:
        st.subheader("Priority Distribution")
        pri_dist = df_processed['true_priority'].value_counts()
        st.bar_chart(pri_dist)
    
    st.markdown("---")
    
    # Sentiment distribution
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Sentiment Distribution")
        sent_dist = df_processed['true_sentiment'].value_counts()
        st.bar_chart(sent_dist)
    
    with col2:
        st.subheader("Text Length Distribution")
        word_dist = pd.cut(df_processed['word_count'], bins=10).value_counts().sort_index()
        word_dist.index = word_dist.index.astype(str)
        st.bar_chart(word_dist)

    st.markdown("---")
    
    # Sample data
    st.subheader("Sample Data")
    st.dataframe(
        df_processed[['ticket_id', 'description', 'true_category', 'true_priority', 'true_sentiment']].head(10),
        use_container_width=True,
        hide_index=True
    )

# PAGE 4: ABOUT
elif page == "About":
    st.header("About This POC")
    
    st.markdown("""
    ### Project Overview
    AI Proof-of-Concept for automated support ticket classification.
    
    **Built by:** Razeen (AI & DS Student, Data Engineering Intern)  
    **Date:** July 2026  
    **Timeline:** 1 week
    
    ### What It Does
    - Automatically classifies support tickets into categories (Bug, Feature Request, Billing, etc.)
    - Analyzes sentiment to identify escalations
    - Assigns priority levels automatically
    - Provides real-time predictions and analytics
    
    ### Technology Stack
    | Component | Technology |
    |-----------|-----------|
    | Data Processing | Python (pandas, numpy) |
    | ML Framework | scikit-learn |
    | NLP | TF-IDF, Naive Bayes |
    | Demo Interface | Streamlit |
    | Model Serialization | Pickle |
    
    ### Phases Completed
    Phase 1: Data generation & preprocessing (500 synthetic tickets)  
    Phase 2: Model training & evaluation  
    Phase 3: Integration & API (Streamlit app)  
    Phase 4: Demo & documentation
    
    ### Key Metrics
    - Category Classifier Accuracy: 79%+ on test set
    - Processing Speed: <100ms per ticket
    - Scalability: Tested on 500+ tickets
    
    ### Next Steps (Production)
    1. Fine-tune on real company support tickets
    2. Deploy as REST API
    3. Integrate with ticketing system
    4. Add priority prediction model
    5. Monitor performance in production
    """)
    
    st.markdown("---")

# Footer
st.markdown("---")
st.markdown(
    f"<p style='text-align: center; color: gray;'>POC Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} IST</p>",
    unsafe_allow_html=True
)
