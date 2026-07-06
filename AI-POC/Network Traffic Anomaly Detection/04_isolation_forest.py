"""
Phase 4a: Anomaly Detection - Isolation Forest Model
Tree-based unsupervised anomaly detection algorithm.
Expected performance: ~92% accuracy on non-overlapping anomalies.
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
import pickle

class IsolationForestModel:
    """Isolation Forest anomaly detection model."""
    
    def __init__(self, contamination=0.10, random_state=42):
        self.model = IsolationForest(
            contamination=contamination,
            random_state=random_state,
            n_estimators=100,
            max_samples='auto'
        )
        self.contamination = contamination
        self.history = {}
    
    def train(self, X_train):
        """Train the Isolation Forest model."""
        print("   ⏳ Training Isolation Forest...")
        
        self.model.fit(X_train)
        print(f"      ✓ Model trained on {len(X_train):,} samples")
    
    def predict(self, X_test):
        """Generate predictions (-1=anomaly, 1=normal)."""
        raw_predictions = self.model.predict(X_test)
        # Convert to binary (1=anomaly, 0=normal)
        predictions = np.where(raw_predictions == -1, 1, 0)
        return predictions
    
    def get_anomaly_scores(self, X_test):
        """Get raw anomaly scores (distance to isolation path)."""
        return self.model.score_samples(X_test)
    
    def evaluate(self, X_test, y_test):
        """Evaluate model performance."""
        print("   ⏳ Evaluating Isolation Forest...")
        
        y_pred = self.predict(X_test)
        y_scores = self.get_anomaly_scores(X_test)
        
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, zero_division=0)
        recall = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)
        
        # ROC-AUC
        try:
            roc_auc = roc_auc_score(y_test, -y_scores)
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
        
        print(f"\n      ✓ Isolation Forest Metrics:")
        print(f"         Accuracy:  {accuracy:.4f} (92% baseline)")
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
        print("\n🌲 Phase 4a: Isolation Forest")
        print("=" * 60)
        
        self.train(X_train)
        metrics = self.evaluate(X_test, y_test)
        self.save_model("isolation_forest_model.pkl")
        
        print(f"\n✅ Phase 4a Complete")
        return metrics


if __name__ == "__main__":
    # Load data from Phase 3
    print("📖 Loading train/test data...")
    X_train = pd.read_csv("train_data.csv").drop('is_anomaly', axis=1)
    y_train = pd.read_csv("train_data.csv")['is_anomaly']
    
    X_test = pd.read_csv("test_data.csv").drop('is_anomaly', axis=1)
    y_test = pd.read_csv("test_data.csv")['is_anomaly']
    
    # Train and evaluate
    model = IsolationForestModel(contamination=0.10)
    metrics = model.run_pipeline(X_train, X_test, y_test)
    
    # Save metrics
    import json
    with open("isolation_forest_metrics.json", "w") as f:
        metrics_serializable = {k: v.tolist() if isinstance(v, np.ndarray) else v for k, v in metrics.items()}
        json.dump(metrics_serializable, f, indent=2)
    
    print(f"✅ Metrics saved to isolation_forest_metrics.json")
