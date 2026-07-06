"""
Phase 3: Feature Selection & Exploratory Data Analysis
Identifies most important features using mutual information and statistical tests.
Prepares train-test split for model training.
"""

import pandas as pd
import numpy as np
from sklearn.feature_selection import mutual_info_classif, chi2
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns

class FeatureSelectionEDA:
    """Feature selection and EDA for anomaly detection."""
    
    def __init__(self, df):
        self.df = df.copy()
        self.feature_cols = [col for col in df.columns if col not in ['timestamp', 'is_anomaly', 'anomaly_type']]
        self.X = df[self.feature_cols]
        self.y = df['is_anomaly']
    
    def compute_mutual_information(self):
        """Compute MI scores for each feature."""
        print("   ⏳ Computing mutual information scores...")
        
        # Ensure features are non-negative for MI
        X_positive = self.X.copy()
        X_positive = X_positive - X_positive.min() + 1e-10
        
        mi_scores = mutual_info_classif(X_positive, self.y, random_state=42)
        mi_df = pd.DataFrame({
            'feature': self.feature_cols,
            'mi_score': mi_scores
        }).sort_values('mi_score', ascending=False)
        
        print(f"      ✓ Top 10 features by MI:")
        for idx, row in mi_df.head(10).iterrows():
            print(f"         {row['feature']}: {row['mi_score']:.4f}")
        
        return mi_df
    
    def analyze_anomaly_distribution(self):
        """Analyze anomaly distribution across types."""
        print("   ⏳ Analyzing anomaly distribution...")
        
        if 'anomaly_type' in self.df.columns:
            anomaly_dist = self.df['anomaly_type'].value_counts()
            print(f"      ✓ Anomaly type distribution:")
            for atype, count in anomaly_dist.items():
                pct = (count / len(self.df)) * 100
                print(f"         {atype}: {count:,} ({pct:.2f}%)")
        
        normal_count = (self.y == 0).sum()
        anomaly_count = (self.y == 1).sum()
        print(f"\n      ✓ Class distribution:")
        print(f"         Normal: {normal_count:,} ({(normal_count/len(self.df))*100:.2f}%)")
        print(f"         Anomaly: {anomaly_count:,} ({(anomaly_count/len(self.df))*100:.2f}%)")
    
    def compute_feature_statistics(self):
        """Compute basic statistics for each feature."""
        print("   ⏳ Computing feature statistics...")
        
        stats = pd.DataFrame({
            'feature': self.feature_cols,
            'mean': self.X.mean().values,
            'std': self.X.std().values,
            'min': self.X.min().values,
            'max': self.X.max().values,
            'skewness': self.X.skew().values,
            'kurtosis': self.X.kurtosis().values
        })
        
        print(f"      ✓ Computed statistics for {len(stats)} features")
        return stats
    
    def select_top_features(self, n_features=50):
        """Select top N features by MI score."""
        print(f"   ⏳ Selecting top {n_features} features...")
        
        mi_df = self.compute_mutual_information()
        top_features = mi_df.head(n_features)['feature'].tolist()
        
        print(f"      ✓ Selected {len(top_features)} features")
        return top_features
    
    def train_test_split(self, test_size=0.2, random_state=42):
        """Split data into train and test sets."""
        print(f"   ⏳ Splitting data (80/20 train/test)...")
        
        # Use top features
        top_features = self.select_top_features(n_features=50)
        X_selected = self.X[top_features]
        
        X_train, X_test, y_train, y_test = train_test_split(
            X_selected, self.y,
            test_size=test_size,
            random_state=random_state,
            stratify=self.y
        )
        
        print(f"      ✓ Train set: {len(X_train):,} rows ({(len(X_train)/len(self.X))*100:.1f}%)")
        print(f"      ✓ Test set: {len(X_test):,} rows ({(len(X_test)/len(self.X))*100:.1f}%)")
        print(f"      ✓ Features: {len(top_features)}")
        
        return X_train, X_test, y_train, y_test, top_features
    
    def run_eda(self):
        """Execute full EDA pipeline."""
        print("\n📊 Phase 3: Feature Selection & EDA")
        print("=" * 60)
        
        self.analyze_anomaly_distribution()
        mi_df = self.compute_mutual_information()
        stats_df = self.compute_feature_statistics()
        
        print(f"\n✅ Phase 3 Complete")
        print(f"   Features analyzed: {len(self.feature_cols)}")
        print(f"   Top feature: {mi_df.iloc[0]['feature']} (MI: {mi_df.iloc[0]['mi_score']:.4f})")
        
        return mi_df, stats_df


if __name__ == "__main__":
    # Load data from Phase 2
    INPUT_FILE = "preprocessed_data.csv"
    
    print(f"📖 Loading {INPUT_FILE}...")
    df = pd.read_csv(INPUT_FILE)
    
    # Run EDA
    selector = FeatureSelectionEDA(df)
    mi_df, stats_df = selector.run_eda()
    
    # Prepare train-test split
    X_train, X_test, y_train, y_test, top_features = selector.train_test_split()
    
    # Save splits
    print(f"\n💾 Saving train/test splits...")
    train_df = pd.concat([X_train, y_train], axis=1)
    test_df = pd.concat([X_test, y_test], axis=1)
    
    train_df.to_csv("train_data.csv", index=False)
    test_df.to_csv("test_data.csv", index=False)
    
    # Save feature list
    with open("selected_features.txt", "w") as f:
        f.write("\n".join(top_features))
    
    print(f"✅ Saved: train_data.csv, test_data.csv, selected_features.txt")
