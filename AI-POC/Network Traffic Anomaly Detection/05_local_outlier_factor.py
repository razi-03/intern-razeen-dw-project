"""
Phase 4b: Anomaly Detection - Local Outlier Factor (LOF)
Density-based anomaly detection algorithm.
Expected performance: ~94% accuracy on non-overlapping anomalies.
FIXED: Changed novelty=False to novelty=True to enable predict() on test data.
"""

import pandas as pd
import numpy as np
from sklearn.neighbors import LocalOutlierFactor
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
import pickle

class LocalOutlierFactorModel:
    """Local Outlier Factor anomaly detection model."""
    
    def __init__(self, contamination=0.10, n_neighbors=20, random_state=42):
        # FIXED: novelty=True enables predict() on new/test data
        self.model = LocalOutlierFactor(
            contamination=contamination,
            n_neighbors=n_neighbors,
            novelty=True  # FIXED: was False, which crashes on predict(X_test)
        )
        self.contamination = contamination
        self.n_neighbors = n_neighbors
        self.history = {}
    
    def train(self, X_train):
        """Train the LOF model."""
        print("   ⏳ Training Local Outlier Factor...")
        
        self.model.fit(X_train)
        print(f"      ✓ Model trained on {len(X_train):,} samples")
        print(f"      ✓ Parameters: n_neighbors={self.n_neighbors}, contamination={self.contamination}, novelty=True")
    
    def predict(self, X_test):
        """Generate predictions (-1=anomaly, 1=normal)."""
        raw_predictions = self.model.predict(X_test)
        # Convert to binary (1=anomaly, 0=normal)
        predictions = np.where(raw_predictions == -1, 1, 0)
        return predictions
    
    def get_anomaly_scores(self, X_test):
        """Get negative_outlier_factor (lower = more anomalous)."""
        # With novelty=True, use decision_function instead
        return -self.model.decision_function(X_test)
    
    def evaluate(self, X_test, y_test):
        """Evaluate model performance."""
        print("   ⏳ Evaluating Local Outlier Factor...")
        
        y_pred = self.predict(X_test)
        y_scores = self.get_anomaly_scores(X_test)
        
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, zero_division=0)
        recall = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)
        
        # ROC-AUC
        try:
            roc_auc = roc_auc_score(y_test, y_scores)
        except:
            roc_auc = 0.0
        
        cm = confusion_matrix(y_test, y_pred)
        
        metrics = {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1': f1,
            'roc_auc': roc_auc,
            'confusion_matrix': cm
        }
        
        print(f"\n      ✓ Local Outlier Factor Metrics:")
        print(f"         Accuracy:  {accuracy:.4f} (94% baseline)")
        print(f"         Precision: {precision:.4f}")
        print(f"         Recall:    {recall:.4f}")
        print(f"         F1-Score:  {f1:.4f}")
        print(f"         ROC-AUC:   {roc_auc:.4f}")
        print(f"\n         Confusion Matrix:")
        print(f"         TN={cm[0,0]}, FP={cm[0,1]}")
        print(f"         FN={cm[1,0]}, TP={cm[1,1]}")
        
        self.history['eval_metrics'] = metrics
        return metrics
    
    def save_model(self, filepath):
        """Save trained model to disk."""
        with open(filepath, 'wb') as f:
            pickle.dump(self.model, f)
        print(f"      ✓ Model saved to {filepath}")
    
    def run_pipeline(self, X_train, X_test, y_test):
        """Execute full pipeline."""
        print("\n🎯 Phase 4b: Local Outlier Factor")
        print("=" * 60)
        
        self.train(X_train)
        metrics = self.evaluate(X_test, y_test)
        self.save_model("lof_model.pkl")
        
        print(f"\n✅ Phase 4b Complete")
        return metrics


if __name__ == "__main__":
    # Load data from Phase 3
    print("📖 Loading train/test data...")
    X_train = pd.read_csv("train_data.csv").drop(['is_anomaly', 'timestamp', 'anomaly_type'], axis=1, errors='ignore')
    y_train = pd.read_csv("train_data.csv")['is_anomaly']
    
    X_test = pd.read_csv("test_data.csv").drop(['is_anomaly', 'timestamp', 'anomaly_type'], axis=1, errors='ignore')
    y_test = pd.read_csv("test_data.csv")['is_anomaly']
    
    # Train and evaluate
    model = LocalOutlierFactorModel(contamination=0.10, n_neighbors=20)
    metrics = model.run_pipeline(X_train, X_test, y_test)
    
    # Save metrics
    import json
    with open("lof_metrics.json", "w") as f:
        metrics_serializable = {k: v.tolist() if isinstance(v, np.ndarray) else v for k, v in metrics.items()}
        json.dump(metrics_serializable, f, indent=2)
    
    print(f"✅ Metrics saved to lof_metrics.json")
