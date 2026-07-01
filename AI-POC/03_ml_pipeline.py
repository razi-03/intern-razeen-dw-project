"""
Phase 2: ML Model Pipeline
Purpose: Train classifier, sentiment analyzer, and evaluate performance
Author: RAze
Date: 2026-07-01
"""

import pandas as pd
import numpy as np
import pickle
import json
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report
)

class CategoryClassifier:
    """Train and evaluate category classifier."""
    
    def __init__(self):
        self.model = None
        self.vectorizer = None
        self.metrics = {}
    
    def train(self, df, text_column='description_clean', label_column='true_category'):
        """Train category classifier."""
        print("🔄 Training Category Classifier...")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            df[text_column], 
            df[label_column],
            test_size=0.2,
            random_state=42,
            stratify=df[label_column]
        )
        
        print(f"   Training set: {len(X_train)} samples")
        print(f"   Test set: {len(X_test)} samples")
        
        # Create pipeline: TF-IDF + Naive Bayes
        self.model = Pipeline([
            ('tfidf', TfidfVectorizer(max_features=100, ngram_range=(1, 2))),
            ('classifier', MultinomialNB(alpha=1.0))
        ])
        
        # Train
        self.model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test)
        
        self.metrics = {
            'accuracy': float(accuracy_score(y_test, y_pred)),
            'precision_weighted': float(precision_score(y_test, y_pred, average='weighted')),
            'recall_weighted': float(recall_score(y_test, y_pred, average='weighted')),
            'f1_weighted': float(f1_score(y_test, y_pred, average='weighted')),
            'classification_report': classification_report(y_test, y_pred, output_dict=True),
            'confusion_matrix': confusion_matrix(y_test, y_pred).tolist(),
            'classes': list(self.model.named_steps['classifier'].classes_)
        }
        
        print("✅ Category Classifier trained")
        print(f"   Accuracy: {self.metrics['accuracy']:.2%}")
        print(f"   Weighted F1: {self.metrics['f1_weighted']:.2%}")
        
        return self.metrics
    
    def predict(self, text):
        """Predict category for single text."""
        prediction = self.model.predict([text])[0]
        probability = self.model.predict_proba([text])[0]
        confidence = float(np.max(probability))
        
        return {
            'category': prediction,
            'confidence': confidence
        }
    
    def save(self, filepath):
        """Save model to disk."""
        with open(filepath, 'wb') as f:
            pickle.dump(self.model, f)
        print(f"✅ Saved category classifier to {filepath}")


class SentimentAnalyzer:
    """Analyze sentiment using rule-based and optional ML approach."""
    
    def __init__(self):
        self.negative_words = [
            'bug', 'broken', 'crash', 'error', 'fail', 'problem', 'issue',
            'not working', 'urgent', 'asap', 'critical', 'losing', 'lost',
            'expensive', 'slow', 'stuck', 'terrible', 'awful', 'bad'
        ]
        self.positive_words = [
            'thanks', 'great', 'excellent', 'good', 'love', 'appreciate',
            'fantastic', 'amazing', 'best', 'perfect', 'awesome'
        ]
    
    def analyze(self, text):
        """Analyze sentiment with confidence."""
        text_lower = text.lower()
        
        negative_count = sum(1 for word in self.negative_words if word in text_lower)
        positive_count = sum(1 for word in self.positive_words if word in text_lower)
        
        # Determine sentiment
        if negative_count > positive_count:
            sentiment = 'Negative'
            confidence = min(0.99, 0.5 + (negative_count * 0.15))
        elif positive_count > negative_count:
            sentiment = 'Positive'
            confidence = min(0.99, 0.5 + (positive_count * 0.15))
        else:
            sentiment = 'Neutral'
            confidence = 0.7
        
        return {
            'sentiment': sentiment,
            'confidence': float(confidence)
        }
    
    def evaluate(self, df, text_column='description_clean', label_column='true_sentiment'):
        """Evaluate sentiment analyzer on ground truth."""
        print("\n🔄 Evaluating Sentiment Analyzer...")
        
        predictions = df[text_column].apply(lambda x: self.analyze(x)['sentiment'])
        
        accuracy = accuracy_score(df[label_column], predictions)
        metrics = {
            'accuracy': float(accuracy),
            'classification_report': classification_report(
                df[label_column], predictions, output_dict=True
            ),
            'confusion_matrix': confusion_matrix(df[label_column], predictions).tolist()
        }
        
        print(f"✅ Sentiment Analyzer evaluated")
        print(f"   Accuracy: {accuracy:.2%}")
        
        return metrics


class ModelEvaluator:
    """Comprehensive model evaluation and reporting."""
    
    @staticmethod
    def generate_report(category_metrics, sentiment_metrics, df):
        """Generate comprehensive evaluation report."""
        report = {
            'timestamp': datetime.now().isoformat(),
            'dataset_summary': {
                'total_samples': len(df),
                'train_test_split': '80-20',
                'random_state': 42
            },
            'category_classifier': {
                'model_type': 'TF-IDF + Multinomial Naive Bayes',
                'hyperparameters': {
                    'max_features': 100,
                    'ngram_range': '(1, 2)',
                    'alpha': 1.0
                },
                'metrics': category_metrics
            },
            'sentiment_analyzer': {
                'model_type': 'Rule-based (keyword matching)',
                'metrics': sentiment_metrics
            },
            'recommendations': [
                "Category classifier performs well - ready for production testing",
                "Consider fine-tuning on company-specific tickets",
                "Sentiment analyzer could be improved with pre-trained model (transformers)",
                "Add priority prediction model in Phase 3"
            ]
        }
        
        return report
    
    @staticmethod
    def print_report(category_metrics, sentiment_metrics):
        """Print readable evaluation report."""
        print("\n" + "="*70)
        print("📊 MODEL EVALUATION REPORT")
        print("="*70)
        
        print("\n🏷️  CATEGORY CLASSIFIER PERFORMANCE:")
        print(f"   Accuracy:  {category_metrics['accuracy']:.2%}")
        print(f"   Precision: {category_metrics['precision_weighted']:.2%}")
        print(f"   Recall:    {category_metrics['recall_weighted']:.2%}")
        print(f"   F1-Score:  {category_metrics['f1_weighted']:.2%}")
        
        print("\n😊 SENTIMENT ANALYZER PERFORMANCE:")
        print(f"   Accuracy:  {sentiment_metrics['accuracy']:.2%}")
        
        print("\n📈 PER-CLASS CATEGORY PERFORMANCE:")
        for category, metrics in category_metrics['classification_report'].items():
            if category not in ['accuracy', 'macro avg', 'weighted avg']:
                print(f"   {category:20} P:{metrics['precision']:.2f} R:{metrics['recall']:.2f} F1:{metrics['f1-score']:.2f}")
        
        print("\n✅ NEXT STEPS:")
        print("   1. Deploy category classifier to production")
        print("   2. Integrate with support ticket system")
        print("   3. Monitor performance on real tickets")
        print("   4. Add priority prediction model")
        
        print("="*70)


if __name__ == "__main__":
    # Load processed data
    print("📂 Loading processed data...")
    df = pd.read_csv('data_processed_tickets.csv')
    df['created_at'] = pd.to_datetime(df['created_at'])
    
    # Train Category Classifier
    print("\n" + "="*70)
    classifier = CategoryClassifier()
    category_metrics = classifier.train(df)
    classifier.save('category_classifier.pkl')
    
    # Train Sentiment Analyzer
    print("\n" + "="*70)
    sentiment = SentimentAnalyzer()
    sentiment_metrics = sentiment.evaluate(df)
    
    # Generate Report
    print("\n" + "="*70)
    full_report = ModelEvaluator.generate_report(category_metrics, sentiment_metrics, df)
    ModelEvaluator.print_report(category_metrics, sentiment_metrics)
    
    # Save Report
    with open('model_evaluation_report.json', 'w') as f:
        json.dump(full_report, f, indent=2, default=str)
    print("\n✅ Saved evaluation report to model_evaluation_report.json")
    
    # Test predictions
    print("\n" + "="*70)
    print("🧪 SAMPLE PREDICTIONS:")
    print("="*70)
    
    test_tickets = [
        "The login button is broken and I cannot access my account!",
        "Can you add dark mode to the platform?",
        "I was charged twice, this is urgent.",
        "How do I reset my password?",
        "Your platform is amazing, thanks for the help!"
    ]
    
    for i, ticket in enumerate(test_tickets, 1):
        cat_pred = classifier.predict(ticket)
        sent_pred = sentiment.analyze(ticket)
        
        print(f"\nTicket {i}: {ticket[:50]}...")
        print(f"   Category: {cat_pred['category']} (confidence: {cat_pred['confidence']:.2%})")
        print(f"   Sentiment: {sent_pred['sentiment']} (confidence: {sent_pred['confidence']:.2%})")
