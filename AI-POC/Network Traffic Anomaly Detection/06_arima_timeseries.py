"""
Anomaly Detection Phase 3C: ARIMA Time Series
Purpose: Train and evaluate ARIMA for time series anomaly detection
Author: RAze
Date: 2026-07-01
Runtime: ~120 seconds (ARIMA is slower)
"""

import pandas as pd
import numpy as np
import pickle
import json
import warnings
from sklearn.metrics import (
    precision_score, recall_score, f1_score, roc_auc_score,
    confusion_matrix, accuracy_score
)
from datetime import datetime
import sys

# Suppress warnings for ARIMA
warnings.filterwarnings('ignore')

try:
    from statsmodels.tsa.arima.model import ARIMA
    from statsmodels.tsa.stattools import adfuller
    ARIMA_AVAILABLE = True
except ImportError:
    ARIMA_AVAILABLE = False
    print("⚠️  statsmodels not found. Using fallback ARIMA implementation.")


class ARIMATimeSeriesDetector:
    """ARIMA-based time series anomaly detection."""
    
    def __init__(self, primary_feature='packets_per_sec', order=(1, 1, 1), threshold_std=3.0):
        """
        Args:
            primary_feature: Main metric to model
            order: ARIMA order (p, d, q)
            threshold_std: Standard deviations for anomaly threshold
        """
        self.primary_feature = primary_feature
        self.order = order
        self.threshold_std = threshold_std
        self.models = {}  # One model per feature
        self.metrics = {}
        self.feature_columns = [
            'packets_per_sec',
            'bandwidth_mbps',
            'latency_ms',
            'error_rate',
            'cpu_usage',
            'memory_usage'
        ]
    
    def train(self, df, test_size=0.2):
        """Train ARIMA models for multiple features."""
        print("\n🔄 Training ARIMA Time Series Models...")
        
        # Split data
        split_idx = int(len(df) * (1 - test_size))
        df_train = df.iloc[:split_idx]
        df_test = df.iloc[split_idx:]
        y_test_true = df_test['is_anomaly'].values
        
        print(f"   Training set: {len(df_train):,} samples")
        print(f"   Test set: {len(df_test):,} samples")
        
        # Train ARIMA models for key features
        print("   Training ARIMA models (this will take a few minutes)...")
        
        residuals_all = []
        predictions_all = []
        
        for idx, feature in enumerate(self.feature_columns[:3], 1):  # Train on top 3 features
            print(f"      [{idx}/3] Training {feature}...")
            
            try:
                # Train on training data
                if ARIMA_AVAILABLE:
                    model = ARIMA(df_train[feature], order=self.order)
                    model = model.fit()
                else:
                    # Fallback: simple exponential smoothing
                    model = self._fallback_arima(df_train[feature])
                
                self.models[feature] = model
                
                # Make predictions on test data
                if ARIMA_AVAILABLE:
                    forecast_steps = len(df_test)
                    forecast = model.get_forecast(steps=forecast_steps)
                    predictions = forecast.predicted_mean.values
                else:
                    predictions = self._fallback_predict(model, len(df_test))
                
                # Calculate residuals
                residuals = df_test[feature].values - predictions
                residuals_all.append(residuals)
                predictions_all.append(predictions)
                
            except Exception as e:
                print(f"      ⚠️  Error training {feature}: {str(e)[:50]}")
                # Use simple anomaly detection as fallback
                residuals = df_test[feature].values - df_test[feature].rolling(window=10).mean().values
                residuals_all.append(residuals)
        
        # Combine residuals from all features (multivariate anomaly detection)
        # Normalize each residual series
        normalized_residuals = []
        for res in residuals_all:
            if len(res) > 0 and np.std(res) > 0:
                normalized_residuals.append((res - np.mean(res)) / np.std(res))
        
        if normalized_residuals:
            # Combined anomaly score = mean absolute deviation across all features
            residuals_combined = np.mean(np.abs(normalized_residuals), axis=0)
        else:
            residuals_combined = np.ones(len(df_test))
        
        # Detect anomalies using threshold
        threshold = self.threshold_std
        y_pred = (np.abs(residuals_combined) > threshold).astype(int)
        
        # Evaluate
        self._evaluate(y_test_true, y_pred, residuals_combined)
        
        # Store for later use
        self.test_predictions = y_pred
        self.test_scores = np.abs(residuals_combined)
        self.test_true_labels = y_test_true
        self.test_residuals_combined = residuals_combined
        
        return self.metrics
    
    def _fallback_arima(self, series):
        """Simple exponential smoothing as fallback."""
        alpha = 0.3
        result = [series.iloc[0]]
        for i in range(1, len(series)):
            result.append(alpha * series.iloc[i] + (1 - alpha) * result[-1])
        
        class SimpleModel:
            def __init__(self, smoothed):
                self.smoothed = smoothed
        
        return SimpleModel(result)
    
    def _fallback_predict(self, model, steps):
        """Fallback prediction using last smoothed value."""
        last_value = model.smoothed[-1]
        return np.full(steps, last_value)
    
    def _evaluate(self, y_true, y_pred, scores):
        """Evaluate model performance."""
        print(f"\n   Test Set Results:")
        
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
        self.metrics['test_accuracy'] = float(accuracy)
        self.metrics['test_precision'] = float(precision)
        self.metrics['test_recall'] = float(recall)
        self.metrics['test_f1'] = float(f1)
        self.metrics['test_auc'] = float(auc)
        self.metrics['test_confusion_matrix'] = confusion_matrix(y_true, y_pred).tolist()
        self.metrics['threshold_std'] = self.threshold_std
    
    def save(self, filepath):
        """Save model to disk."""
        with open(filepath, 'wb') as f:
            pickle.dump(self, f)
        print(f"\n✅ Saved ARIMA to {filepath}")


class ARIMAReport:
    """Generate report for ARIMA."""
    
    @staticmethod
    def generate(detector):
        """Generate comprehensive report."""
        report = {
            'algorithm': 'ARIMA Time Series',
            'timestamp': datetime.now().isoformat(),
            'parameters': {
                'order': detector.order,
                'primary_feature': detector.primary_feature,
                'threshold_std': detector.threshold_std,
                'features_modeled': detector.feature_columns[:3]
            },
            'metrics': detector.metrics,
            'description': """
ARIMA (AutoRegressive Integrated Moving Average) is a classical
time series forecasting method. Anomalies are detected by identifying
large residuals (prediction errors).

How it works:
1. Train ARIMA model to predict each metric
2. Calculate residuals (actual - predicted)
3. Flag large residuals as anomalies
4. Use multivariate residuals for final detection

Pros:
- Captures temporal patterns very well
- Interpretable parameters
- Handles trends and seasonality
- Classical, well-tested method

Cons:
- Slower training than Isolation Forest
- May struggle with sudden changes
- Requires stationary data (differencing)
- Parameter tuning can be complex
            """
        }
        
        return report


if __name__ == "__main__":
    # Load preprocessed data
    print("📂 Loading preprocessed network traffic data...")
    df = pd.read_csv('/home/claude/network_traffic_processed.csv')
    print(f"   Loaded {len(df):,} records")
    
    # Train ARIMA
    print("\n" + "="*70)
    print("🏗️  ARIMA TIME SERIES TRAINING")
    print("="*70)
    
    detector = ARIMATimeSeriesDetector(order=(1, 1, 1), threshold_std=3.0)
    metrics = detector.train(df, test_size=0.2)
    
    # Save model
    detector.save('/home/claude/arima_model.pkl')
    
    # Generate report
    report = ARIMAReport.generate(detector)
    with open('/home/claude/arima_report.json', 'w') as f:
        json.dump(report, f, indent=2, default=str)
    print("\n✅ Saved report to arima_report.json")
    
    print("\n" + "="*70)
    print("✨ ARIMA Training Complete!")
    print("="*70)
