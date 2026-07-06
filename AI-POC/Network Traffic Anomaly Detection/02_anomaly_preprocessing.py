"""
Phase 2: Anomaly Detection - Time Series Preprocessing
Handles temporal alignment, scaling, rolling statistics, and lag features.
Note: Phase 1 now uses non-overlapping anomaly clusters (no double-scaling).
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from datetime import datetime

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
        
        # Note: Phase 1 uses improved non-overlapping anomaly injection
        # This prevents double-scaling and keeps anomaly budget accurate
        print("   ℹ️  Phase 1 uses improved non-overlapping anomaly injection")
        self.scaler = StandardScaler()
    
    def handle_missing_values(self):
        """Handle any missing values (interpolation)."""
        print("   ⏳ Handling missing values...")
        
        for col in self.numeric_features:
            if col in self.df.columns and self.df[col].isnull().any():
                self.df[col].interpolate(method='linear', inplace=True)
                self.df[col].fillna(self.df[col].mean(), inplace=True)
        
        print(f"      ✓ Missing values handled")
    
    def create_rolling_features(self):
        """Create rolling window statistics (5, 10, 20 second windows)."""
        print("   ⏳ Creating rolling features...")
        
        windows = [5, 10, 20]
        new_cols = 0
        
        for window in windows:
            for col in self.numeric_features:
                # Rolling mean
                self.df[f'{col}_roll_mean_{window}'] = self.df[col].rolling(window=window, min_periods=1).mean()
                # Rolling std
                self.df[f'{col}_roll_std_{window}'] = self.df[col].rolling(window=window, min_periods=1).std().fillna(0)
                new_cols += 2
        
        print(f"      ✓ Created {new_cols} rolling features (3 windows × 7 metrics × 2 stats)")
    
    def create_lag_features(self):
        """Create lagged features (t-1, t-2, t-3 seconds)."""
        print("   ⏳ Creating lag features...")
        
        lags = [1, 2, 3]
        new_cols = 0
        
        for col in self.numeric_features:
            for lag in lags:
                self.df[f'{col}_lag_{lag}'] = self.df[col].shift(lag)
            new_cols += 3
        
        # Fill first few rows with backward fill (pandas 2.0+ syntax)
        self.df = self.df.bfill()
        
        print(f"      ✓ Created {new_cols} lag features (3 lags × 7 metrics)")
    
    def create_difference_features(self):
        """Create differenced features (delta/velocity)."""
        print("   ⏳ Creating difference features...")
        
        new_cols = 0
        
        for col in self.numeric_features:
            self.df[f'{col}_delta'] = self.df[col].diff().fillna(0)
            new_cols += 1
        
        print(f"      ✓ Created {new_cols} difference features (7 metrics)")
    
    def normalize_features(self):
        """Normalize numeric features to zero mean, unit variance."""
        print("   ⏳ Normalizing features...")
        
        feature_cols = [col for col in self.df.columns if col not in ['timestamp', 'is_anomaly', 'anomaly_type']]
        self.df[feature_cols] = self.scaler.fit_transform(self.df[feature_cols])
        
        print(f"      ✓ Normalized {len(feature_cols)} features")
    
    def preprocess(self):
        """Execute full preprocessing pipeline."""
        print("\n🔧 Phase 2: Time Series Preprocessing")
        print("=" * 60)
        
        self.handle_missing_values()
        self.create_rolling_features()
        self.create_lag_features()
        self.create_difference_features()
        self.normalize_features()
        
        print(f"\n✅ Phase 2 Complete")
        print(f"   Rows: {len(self.df):,}")
        print(f"   Features: {len(self.df.columns)}")
        print(f"   Columns: {list(self.df.columns)[:5]} ... + {len(self.df.columns) - 5} more")
        
        return self.df


if __name__ == "__main__":
    # Load data from Phase 1
    INPUT_FILE = "network_traffic_raw.csv"  # FIXED: correct filename from Phase 1
    OUTPUT_FILE = "preprocessed_data.csv"
    
    print(f"📖 Loading {INPUT_FILE}...")
    df = pd.read_csv(INPUT_FILE)
    
    # Preprocess
    preprocessor = TimeSeriesPreprocessor(df)
    df_processed = preprocessor.preprocess()
    
    # Save
    print(f"\n💾 Saving to {OUTPUT_FILE}...")
    df_processed.to_csv(OUTPUT_FILE, index=False)
    print(f"✅ Saved: {OUTPUT_FILE}")