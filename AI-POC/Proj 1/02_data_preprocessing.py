"""
Phase 1 Part 2: Data Validation & Preprocessing
Purpose: Clean and validate ticket data before model training
Author: RAze
Date: 2026-07-01
"""

import pandas as pd
import numpy as np
import re
from datetime import datetime
import json

class DataValidator:
    """Validate ticket dataset quality."""
    
    @staticmethod
    def validate_schema(df):
        """Check if dataframe has required columns."""
        required_columns = [
            'ticket_id', 'created_at', 'description', 
            'true_category', 'true_priority', 'true_sentiment'
        ]
        
        missing = [col for col in required_columns if col not in df.columns]
        if missing:
            raise ValueError(f"❌ Missing required columns: {missing}")
        
        print("✅ Schema validation passed")
        return True
    
    @staticmethod
    def validate_values(df):
        """Check for null values and invalid data."""
        valid_categories = ['Bug', 'Feature Request', 'Billing', 'Technical Support', 'Account', 'Other']
        valid_priorities = ['Low', 'Medium', 'High', 'Critical']
        valid_sentiments = ['Positive', 'Neutral', 'Negative']
        
        issues = []
        
        # Check nulls
        null_counts = df.isnull().sum()
        if null_counts.sum() > 0:
            issues.append(f"⚠️  Found {null_counts.sum()} null values")
            print(null_counts[null_counts > 0])
        
        # Check invalid categories
        invalid_cat = df[~df['true_category'].isin(valid_categories)]
        if len(invalid_cat) > 0:
            issues.append(f"⚠️  {len(invalid_cat)} invalid categories")
        
        # Check invalid priorities
        invalid_pri = df[~df['true_priority'].isin(valid_priorities)]
        if len(invalid_pri) > 0:
            issues.append(f"⚠️  {len(invalid_pri)} invalid priorities")
        
        # Check invalid sentiments
        invalid_sent = df[~df['true_sentiment'].isin(valid_sentiments)]
        if len(invalid_sent) > 0:
            issues.append(f"⚠️  {len(invalid_sent)} invalid sentiments")
        
        # Check for empty descriptions
        empty_desc = df[df['description'].str.strip() == '']
        if len(empty_desc) > 0:
            issues.append(f"⚠️  {len(empty_desc)} empty descriptions")
        
        if issues:
            print("Validation Issues:")
            for issue in issues:
                print(issue)
        else:
            print("✅ Value validation passed - all data is valid")
        
        return len(issues) == 0


class DataPreprocessor:
    """Clean and preprocess text data."""
    
    @staticmethod
    def clean_text(text):
        """Clean and normalize text."""
        # Convert to lowercase
        text = text.lower()
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+', '', text)
        
        # Remove special characters but keep spaces
        text = re.sub(r'[^a-z0-9\s\?\!]', '', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text
    
    @staticmethod
    def preprocess_dataframe(df):
        """Apply preprocessing to entire dataset."""
        print("🔄 Starting preprocessing...")
        
        df_clean = df.copy()
        
        # Clean descriptions
        print("  - Cleaning text...")
        df_clean['description_clean'] = df_clean['description'].apply(
            DataPreprocessor.clean_text
        )
        
        # Add text length feature
        print("  - Computing text statistics...")
        df_clean['text_length'] = df_clean['description_clean'].str.len()
        df_clean['word_count'] = df_clean['description_clean'].str.split().str.len()
        
        # Parse datetime
        print("  - Parsing timestamps...")
        df_clean['created_at'] = pd.to_datetime(df_clean['created_at'])
        df_clean['day_of_week'] = df_clean['created_at'].dt.day_name()
        df_clean['hour'] = df_clean['created_at'].dt.hour
        
        print("✅ Preprocessing complete")
        return df_clean


class DataAnalyzer:
    """Exploratory Data Analysis."""
    
    @staticmethod
    def generate_report(df):
        """Generate EDA report."""
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_records': len(df),
            'columns': list(df.columns),
            'null_values': df.isnull().sum().to_dict(),
            'data_types': df.dtypes.astype(str).to_dict(),
            'category_distribution': df['true_category'].value_counts().to_dict(),
            'priority_distribution': df['true_priority'].value_counts().to_dict(),
            'sentiment_distribution': df['true_sentiment'].value_counts().to_dict(),
            'text_statistics': {
                'min_length': int(df['text_length'].min()),
                'max_length': int(df['text_length'].max()),
                'mean_length': float(df['text_length'].mean()),
                'median_length': float(df['text_length'].median()),
                'min_words': int(df['word_count'].min()),
                'max_words': int(df['word_count'].max()),
                'mean_words': float(df['word_count'].mean())
            },
            'temporal_info': {
                'date_range': f"{df['created_at'].min()} to {df['created_at'].max()}",
                'tickets_by_hour': df['hour'].value_counts().to_dict(),
                'tickets_by_day': df['day_of_week'].value_counts().to_dict()
            }
        }
        
        return report
    
    @staticmethod
    def print_summary(df):
        """Print readable summary."""
        print("\n" + "="*60)
        print("📊 DATA ANALYSIS SUMMARY")
        print("="*60)
        
        print(f"\n📈 Dataset Size: {len(df)} tickets")
        
        print("\n📂 Category Distribution:")
        for cat, count in df['true_category'].value_counts().items():
            pct = (count / len(df)) * 100
            print(f"   {cat:20} {count:4d} ({pct:5.1f}%)")
        
        print("\n⚡ Priority Distribution:")
        for pri, count in df['true_priority'].value_counts().items():
            pct = (count / len(df)) * 100
            print(f"   {pri:20} {count:4d} ({pct:5.1f}%)")
        
        print("\n😊 Sentiment Distribution:")
        for sent, count in df['true_sentiment'].value_counts().items():
            pct = (count / len(df)) * 100
            print(f"   {sent:20} {count:4d} ({pct:5.1f}%)")
        
        print("\n📝 Text Statistics:")
        print(f"   Average length: {df['text_length'].mean():.0f} chars")
        print(f"   Average words: {df['word_count'].mean():.1f} words")
        print(f"   Range: {df['word_count'].min()}-{df['word_count'].max()} words")
        
        print("\n⏰ Temporal Distribution:")
        print(f"   Date range: {df['created_at'].min().date()} to {df['created_at'].max().date()}")
        top_hour = df['hour'].value_counts().head(3)
        print(f"   Most common hours: {top_hour.to_dict()}")
        
        print("="*60)


if __name__ == "__main__":
    # Load raw data
    print("📂 Loading raw data...")
    df_raw = pd.read_csv('data_raw_tickets.csv')
    
    # Validate
    print("\n🔍 Validating data...")
    DataValidator.validate_schema(df_raw)
    DataValidator.validate_values(df_raw)
    
    # Preprocess
    print("\n🔨 Preprocessing data...")
    df_clean = DataPreprocessor.preprocess_dataframe(df_raw)
    
    # Analyze
    print("\n📊 Analyzing data...")
    DataAnalyzer.print_summary(df_clean)
    
    # Save processed data
    df_clean.to_csv('data_processed_tickets.csv', index=False)
    print("\n✅ Saved processed data to data_processed_tickets.csv")
    
    # Generate and save analysis report
    report = DataAnalyzer.generate_report(df_clean)
    with open('eda_report.json', 'w') as f:
        json.dump(report, f, indent=2, default=str)
    print("✅ Saved EDA report to eda_report.json")
    
    # Show sample
    print("\n📋 Sample of Processed Data:")
    print(df_clean[['ticket_id', 'description_clean', 'true_category', 'true_priority', 'word_count']].head(10))
