"""
Anomaly Detection Phase 2: Time Series Preprocessing & Feature Engineering
Purpose: Prepare time series data for anomaly detection models
Author: RAze
Date: 2026-07-01
Runtime: ~60 seconds
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from datetime import datetime
import json

class TimeSeriesPreprocessor:
    """Preprocess and prepare time series data for anomaly detection."""
    
    def __init__(self, df):
        self.df = df.copy()
        self.df['timestamp'] = pd.to_datetime(self.df['timestamp'])
        self.df = self.df.sort_values('timestamp').reset_index(drop=True)
        
        # Metrics to process
        self.numeric_features = [
            'packets_per_sec', 'bandwidth_mbps', 'latency_ms',
            'active_connections', 'error_rate', 'cpu_usage', 'memory_usage'
        ]
    
    def add_rolling_statistics(self, window_minutes=60):
        """Add rolling statistics (mean, std, min, max) for each feature."""
        print(f"📊 Computing rolling statistics (window={window_minutes} min)...")
        
        # Window in terms of 10-second intervals
        window = (window_minutes * 60) // 10
        
        for feature in self.numeric_features:
            # Rolling mean
            self.df[f'{feature}_rolling_mean'] = self.df[feature].rolling(window=window, center=True).mean()
            
            # Rolling std
            self.df[f'{feature}_rolling_std'] = self.df[feature].rolling(window=window, center=True).std()
            
            # Rolling min/max
            self.df[f'{feature}_rolling_min'] = self.df[feature].rolling(window=window, center=True).min()
            self.df[f'{feature}_rolling_max'] = self.df[feature].rolling(window=window, center=True).max()
        
        # Fill NaN values (edges) with forward/backward fill
        self.df = self.df.fillna(method='bfill').fillna(method='ffill')
    
    def add_lag_features(self, lags=[1, 6, 24, 144, 288]):
        """
        Add lag features for autoregressive patterns.
        lags in 10-sec intervals:
        - 1 lag = 10 seconds
        - 6 lags = 1 minute
        - 144 lags = 24 minutes (1440 for 24 hours)
        """
        print("⏱️  Adding lag features...")
        
        for feature in self.numeric_features:
            for lag in lags:
                self.df[f'{feature}_lag_{lag}'] = self.df[feature].shift(lag)
        
        # Fill NaN values from lagging
        self.df = self.df.fillna(method='bfill').fillna(method='ffill')
    
    def add_rate_of_change(self):
        """Add rate of change features (velocity)."""
        print("📈 Adding rate of change features...")
        
        for feature in self.numeric_features:
            # Rate of change in last minute (6 intervals * 10 sec)
            self.df[f'{feature}_rate_change'] = self.df[feature].diff(6)
            
            # Rate of change in last hour (360 intervals * 10 sec)
            self.df[f'{feature}_rate_change_1h'] = self.df[feature].diff(360)
        
        self.df = self.df.fillna(0)
    
    def add_temporal_features(self):
        """Add temporal features (hour of day, day of week, etc)."""
        print("🕐 Adding temporal features...")
        
        self.df['hour'] = self.df['timestamp'].dt.hour
        self.df['day_of_week'] = self.df['timestamp'].dt.dayofweek
        self.df['day_of_month'] = self.df['timestamp'].dt.day
        self.df['is_weekend'] = (self.df['day_of_week'] >= 5).astype(int)
    
    def normalize_features(self):
        """Normalize numeric features using StandardScaler."""
        print("📏 Normalizing features...")
        
        scaler = StandardScaler()
        
        # Features to normalize (original + rolling stats, but not lags)
        features_to_normalize = []
        for col in self.df.columns:
            if col in self.numeric_features or 'rolling' in col or 'rate_change' in col:
                if 'lag' not in col:
                    features_to_normalize.append(col)
        
        normalized_data = scaler.fit_transform(self.df[features_to_normalize])
        
        for idx, col in enumerate(features_to_normalize):
            self.df[f'{col}_normalized'] = normalized_data[:, idx]
        
        # Save scaler info for inference
        self.scaler_mean = scaler.mean_.tolist()
        self.scaler_std = scaler.scale_.tolist()
        
        return scaler
    
    def add_multivariate_features(self):
        """Add features based on correlations between metrics."""
        print("🔗 Adding multivariate features...")
        
        # Ratio features (traffic vs errors)
        self.df['traffic_to_error_ratio'] = (
            self.df['packets_per_sec'] / (self.df['error_rate'] + 0.001)
        )
        
        # Combined stress index
        self.df['stress_index'] = (
            self.df['cpu_usage'] / 100 +
            self.df['memory_usage'] / 100 +
            self.df['error_rate'] +
            (self.df['latency_ms'] / self.df['latency_ms'].max())
        ) / 4
        
        # Traffic-bandwidth efficiency
        self.df['efficiency_ratio'] = (
            self.df['packets_per_sec'] / (self.df['bandwidth_mbps'] + 0.01)
        )
        
        # Clip extreme values
        self.df['stress_index'] = self.df['stress_index'].clip(0, 1)
    
    def prepare_for_models(self):
        """Full preprocessing pipeline."""
        print("\n🔄 STARTING PREPROCESSING PIPELINE\n")
        
        # Step 1: Rolling statistics
        self.add_rolling_statistics(window_minutes=60)
        
        # Step 2: Lag features
        self.add_lag_features()
        
        # Step 3: Rate of change
        self.add_rate_of_change()
        
        # Step 4: Temporal features
        self.add_temporal_features()
        
        # Step 5: Multivariate features
        self.add_multivariate_features()
        
        # Step 6: Normalize
        scaler = self.normalize_features()
        
        print("\n✅ Preprocessing complete!")
        
        return self.df, scaler


class DataQualityChecker:
    """Check data quality after preprocessing."""
    
    @staticmethod
    def check_quality(df):
        """Check for issues in preprocessed data."""
        print("\n🔍 Checking data quality...")
        
        issues = []
        
        # Check nulls
        null_counts = df.isnull().sum()
        if null_counts.sum() > 0:
            print(f"⚠️  Found {null_counts.sum()} null values:")
            print(null_counts[null_counts > 0])
        else:
            print("✅ No null values")
        
        # Check for infinities
        inf_count = np.isinf(df.select_dtypes(include=[np.number])).sum().sum()
        if inf_count > 0:
            issues.append(f"⚠️  Found {inf_count} infinite values")
            print(f"⚠️  Found {inf_count} infinite values")
        else:
            print("✅ No infinite values")
        
        # Check for duplicates
        dup_count = df.duplicated().sum()
        if dup_count > 0:
            issues.append(f"⚠️  Found {dup_count} duplicate rows")
            print(f"⚠️  Found {dup_count} duplicate rows")
        else:
            print("✅ No duplicates")
        
        if not issues:
            print("✅ All quality checks passed!")
        
        return len(issues) == 0


class PreprocessingSummary:
    """Summarize preprocessing results."""
    
    @staticmethod
    def print_summary(df_original, df_processed):
        """Print summary of preprocessing."""
        print("\n" + "="*70)
        print("📊 PREPROCESSING SUMMARY")
        print("="*70)
        
        print(f"\n📈 Original Features: {len(df_original.columns)}")
        print(f"📈 Processed Features: {len(df_processed.columns)}")
        print(f"📈 Features Added: {len(df_processed.columns) - len(df_original.columns)}")
        
        print("\n🏷️  Feature Categories:")
        print(f"   Original metrics: 7")
        print(f"   Rolling statistics: {sum(1 for col in df_processed.columns if 'rolling' in col)}")
        print(f"   Lag features: {sum(1 for col in df_processed.columns if 'lag' in col)}")
        print(f"   Rate of change: {sum(1 for col in df_processed.columns if 'rate_change' in col)}")
        print(f"   Normalized: {sum(1 for col in df_processed.columns if 'normalized' in col)}")
        print(f"   Temporal: {sum(1 for col in df_processed.columns if col in ['hour', 'day_of_week', 'is_weekend'])}")
        print(f"   Multivariate: {sum(1 for col in df_processed.columns if col in ['stress_index', 'efficiency_ratio', 'traffic_to_error_ratio'])}")
        
        print("\n📊 Memory Usage:")
        original_mb = df_original.memory_usage(deep=True).sum() / 1024**2
        processed_mb = df_processed.memory_usage(deep=True).sum() / 1024**2
        print(f"   Original: {original_mb:.1f} MB")
        print(f"   Processed: {processed_mb:.1f} MB")
        print(f"   Increase: {(processed_mb - original_mb):.1f} MB ({((processed_mb/original_mb - 1)*100):.0f}%)")
        
        print("\n✅ Preprocessing ready for model training!")
        print("="*70)
    
    @staticmethod
    def generate_report(df_original, df_processed):
        """Generate JSON report."""
        report = {
            'timestamp': datetime.now().isoformat(),
            'original_shape': [len(df_original), len(df_original.columns)],
            'processed_shape': [len(df_processed), len(df_processed.columns)],
            'features_added': len(df_processed.columns) - len(df_original.columns),
            'feature_types': {
                'original_metrics': 7,
                'rolling_statistics': sum(1 for col in df_processed.columns if 'rolling' in col),
                'lag_features': sum(1 for col in df_processed.columns if 'lag' in col),
                'rate_of_change': sum(1 for col in df_processed.columns if 'rate_change' in col),
                'normalized_features': sum(1 for col in df_processed.columns if 'normalized' in col),
                'temporal_features': 3,
                'multivariate_features': 3
            },
            'memory_usage_mb': {
                'original': float(df_original.memory_usage(deep=True).sum() / 1024**2),
                'processed': float(df_processed.memory_usage(deep=True).sum() / 1024**2)
            }
        }
        
        return report


if __name__ == "__main__":
    # Load raw data
    print("📂 Loading raw network traffic data...")
    df_raw = pd.read_csv('/home/claude/network_traffic_raw.csv')
    print(f"   Loaded {len(df_raw):,} records")
    
    # Preprocess
    print("\n🔨 Starting preprocessing...")
    preprocessor = TimeSeriesPreprocessor(df_raw)
    df_processed, scaler = preprocessor.prepare_for_models()
    
    # Quality check
    print("\n" + "="*70)
    checker = DataQualityChecker()
    checker.check_quality(df_processed)
    
    # Summary
    summary = PreprocessingSummary()
    summary.print_summary(df_raw, df_processed)
    
    # Save processed data
    print("\n💾 Saving processed data...")
    df_processed.to_csv('/home/claude/network_traffic_processed.csv', index=False)
    print("✅ Saved to network_traffic_processed.csv")
    
    # Save report
    report = summary.generate_report(df_raw, df_processed)
    with open('/home/claude/anomaly_preprocessing_report.json', 'w') as f:
        json.dump(report, f, indent=2, default=str)
    print("✅ Saved preprocessing report")
    
    # Show sample
    print("\n📋 Sample of Processed Data (first 5 rows):")
    cols_to_show = ['timestamp', 'packets_per_sec', 'packets_per_sec_rolling_mean', 
                    'packets_per_sec_lag_1', 'hour', 'stress_index', 'is_anomaly']
    print(df_processed[cols_to_show].head().to_string())
    
    print("\n🎉 Phase 2 Complete!")
