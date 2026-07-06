"""
Anomaly Detection Phase 3A: Isolation Forest
Purpose: Train and evaluate Isolation Forest for anomaly detection
Author: RAze
Date: 2026-07-01
Runtime: ~30 seconds
"""

import pandas as pd
import numpy as np
import pickle
import json
from sklearn.ensemble import IsolationForest
from sklearn.metrics import (
    precision_score, recall_score, f1_score, roc_auc_score,
    confusion_matrix, classification_report, accuracy_score
)
from datetime import datetime

class IsolationForestAnomalyDetector:
    """Isolation Forest based anomaly detection."""
    
    def __init__(self, contamination=0.10, random_state=42):
        self.contamination = contamination
        self.model = IsolationForest(
            contamination=contamination,
            random_state=random_state,
            n_estimators=100,
            max_samples='auto',
            n_jobs=-1
        )
        self.metrics = {}
        self.feature_columns = None
    
    def prepare_features(self, df):
        """Prepare features for Isolation Forest."""
        # Select numeric features (normalized ones are best)
        feature_cols = [
            'packets_per_sec_normalized',
            'bandwidth_mbps_normalized',
            'latency_ms_normalized',
            'cpu_usage_normalized',
            'memory_usage_normalized',
            'error_rate_normalized',
            'stress_index',
            'efficiency_ratio',
            'traffic_to_error_ratio'
        ]
        
        # Check which columns exist
        available_cols = [col for col in feature_cols if col in df.columns]
        
        # Add rolling stats if available
        rolling_cols = [col for col in df.columns if 'rolling_std' in col]
        available_cols.extend(rolling_cols[:7])  # Add first 7 rolling std features
        
        # Add rate of change features
        rate_cols = [col for col in df.columns if 'rate_change' in col and 'lag' not in col]
        available_cols.extend(rate_cols[:7])
        
        self.feature_columns = available_cols
        
        print(f"   Using {len(available_cols)} features for training")
        return df[available_cols].values
    
    def train(self, df, test_size=0.2):
        """Train Isolation Forest model."""
        print("\n🔄 Training Isolation Forest...")
        
        # Prepare features
        X = self.prepare_features(df)
        y = df['is_anomaly'].values
        
        # Split data (last 20% as test)
        split_idx = int(len(df) * (1 - test_size))
        X_train, X_test = X[:split_idx], X[split_idx:]
        y_train, y_test = y[:split_idx], y[split_idx:]
        
        print(f"   Training set: {len(X_train):,} samples")
        print(f"   Test set: {len(X_test):,} samples")
        print(f"   Positive class rate (train): {y_train.mean():.1%}")
        print(f"   Positive class rate (test): {y_test.mean():.1%}")
        
        # Train model
        print("   Training model...")
        self.model.fit(X_train)
        
        # Predict
        y_pred_train = self.model.predict(X_train)
        y_pred_test = self.model.predict(X_test)
        
        # Convert predictions: -1 (anomaly) -> 1, 1 (normal) -> 0
        y_pred_train_binary = (y_pred_train == -1).astype(int)
        y_pred_test_binary = (y_pred_test == -1).astype(int)
        
        # Get anomaly scores
        scores_train = -self.model.score_samples(X_train)  # Higher = more anomalous
        scores_test = -self.model.score_samples(X_test)
        
        # Evaluate
        self._evaluate(y_train, y_pred_train_binary, scores_train, 'Train')
        self._evaluate(y_test, y_pred_test_binary, scores_test, 'Test')
        
        # Store test metrics as primary
        self.metrics['dataset'] = 'Test Set'
        
        # Store predictions for later analysis
        self.test_predictions = y_pred_test_binary
        self.test_scores = scores_test
        self.test_true_labels = y_test
        
        return self.metrics
    
    def _evaluate(self, y_true, y_pred, scores, dataset_name):
        """Evaluate model performance."""
        print(f"\n   {dataset_name} Set Results:")
        
        accuracy = accuracy_score(y_true, y_pred)
        precision = precision_score(y_true, y_pred, zero_division=0)
        recall = recall_score(y_true, y_pred, zero_division=0)
        f1 = f1_score(y_true, y_pred, zero_division=0)
        
        try:
            auc = roc_auc_score(y_true, scores)
        except:
            auc = 0.0
        
        print(f"      Accuracy:  {accuracy:.3f}")
        print(f"      Precision: {precision:.3f}")
        print(f"      Recall:    {recall:.3f}")
        print(f"      F1-Score:  {f1:.3f}")
        print(f"      ROC-AUC:   {auc:.3f}")
        
        # Store metrics
        key = dataset_name.lower()
        self.metrics[f'{key}_accuracy'] = float(accuracy)
        self.metrics[f'{key}_precision'] = float(precision)
        self.metrics[f'{key}_recall'] = float(recall)
        self.metrics[f'{key}_f1'] = float(f1)
        self.metrics[f'{key}_auc'] = float(auc)
        self.metrics[f'{key}_confusion_matrix'] = confusion_matrix(y_true, y_pred).tolist()
    
    def predict(self, X):
        """Make predictions on new data."""
        raw_predictions = self.model.predict(X)
        scores = -self.model.score_samples(X)
        predictions = (raw_predictions == -1).astype(int)
        
        return predictions, scores
    
    def save(self, filepath):
        """Save model to disk."""
        with open(filepath, 'wb') as f:
            pickle.dump(self, f)
        print(f"\n✅ Saved Isolation Forest to {filepath}")


class IFReport:
    """Generate report for Isolation Forest."""
    
    @staticmethod
    def generate(detector):
        """Generate comprehensive report."""
        report = {
            'algorithm': 'Isolation Forest',
            'timestamp': datetime.now().isoformat(),
            'parameters': {
                'contamination': detector.contamination,
                'n_estimators': 100,
                'max_samples': 'auto',
                'random_state': 42
            },
            'features_used': detector.feature_columns,
            'metrics': detector.metrics,
            'description': """
Isolation Forest works by randomly selecting features and split values,
then isolating anomalies in fewer splits. Fast and effective for
high-dimensional data.

Pros:
- Very fast training and prediction
- No need to scale features
- Handles high-dimensional data well
- No parameter tuning needed

Cons:
- Less interpretable than density-based methods
- May struggle with varying density clusters
            """
        }
        
        return report


if __name__ == "__main__":
    # Load preprocessed data
    print("📂 Loading preprocessed network traffic data...")
    df = pd.read_csv('/home/claude/network_traffic_processed.csv')
    print(f"   Loaded {len(df):,} records")
    
    # Train Isolation Forest
    print("\n" + "="*70)
    print("🏗️  ISOLATION FOREST TRAINING")
    print("="*70)
    
    detector = IsolationForestAnomalyDetector(contamination=0.10)
    metrics = detector.train(df, test_size=0.2)
    
    # Save model
    detector.save('/home/claude/isolation_forest_model.pkl')
    
    # Generate report
    report = IFReport.generate(detector)
    with open('/home/claude/isolation_forest_report.json', 'w') as f:
        json.dump(report, f, indent=2, default=str)
    print("\n✅ Saved report to isolation_forest_report.json")
    
    print("\n" + "="*70)
    print("✨ Isolation Forest Complete!")
    print("="*70)
