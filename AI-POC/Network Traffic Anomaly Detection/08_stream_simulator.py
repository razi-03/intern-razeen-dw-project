"""
Anomaly Detection Phase 4A: Stream Simulator
Purpose: Simulate real-time data flow for production testing
Author: RAze
Date: 2026-07-01
Runtime: ~60 seconds (can simulate faster)
"""

import pandas as pd
import numpy as np
import pickle
import time
import json
from datetime import datetime
from collections import deque

class StreamSimulator:
    """Simulate real-time data streaming."""
    
    def __init__(self, df, delay_ms=10):
        """
        Args:
            df: DataFrame with all features
            delay_ms: Delay between events in milliseconds (10ms = fast simulation)
        """
        self.df = df.sort_values('timestamp').reset_index(drop=True)
        self.delay_ms = delay_ms
        self.current_idx = 0
        
        # Statistics for tracking
        self.predictions_made = 0
        self.anomalies_detected = 0
        self.true_positives = 0
        self.false_positives = 0
        self.false_negatives = 0
        self.true_negatives = 0
        self.latencies = deque(maxlen=1000)  # Track last 1000 latencies
        
        print(f"📊 Initializing Stream Simulator")
        print(f"   Total records: {len(df):,}")
        print(f"   Simulated delay: {delay_ms}ms per event")
        print(f"   Simulated throughput: {1000/delay_ms:.0f} events/sec")
    
    def stream_data(self):
        """
        Generator that yields data points one at a time.
        Simulates real-time data arrival.
        """
        for idx, (_, row) in enumerate(self.df.iterrows()):
            if idx % 10000 == 0:
                print(f"   Streaming progress: {idx:,} / {len(self.df):,}")
            
            yield row
            time.sleep(self.delay_ms / 1000)  # Convert ms to seconds
    
    def stream_with_predictions(self, ensemble):
        """
        Stream data and make predictions in real-time.
        
        Args:
            ensemble: Trained EnsembleAnomalyDetector
        """
        print("\n🚨 STARTING REAL-TIME STREAM SIMULATION")
        print("="*80)
        
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
        
        rolling_cols = [col for col in self.df.columns if 'rolling_std' in col]
        feature_cols.extend(rolling_cols[:7])
        
        rate_cols = [col for col in self.df.columns if 'rate_change' in col and 'lag' not in col]
        feature_cols.extend(rate_cols[:7])
        
        available_cols = [col for col in feature_cols if col in self.df.columns]
        
        start_time = time.time()
        
        for idx, row in enumerate(self.stream_data()):
            # Prepare features
            X = row[available_cols].values.reshape(1, -1)
            
            # Make prediction
            pred_start = time.time()
            pred, score, _, _ = ensemble.predict(X)
            pred_latency = (time.time() - pred_start) * 1000  # Convert to ms
            
            # Track latency
            self.latencies.append(pred_latency)
            
            # Increment counters
            self.predictions_made += 1
            
            is_anomaly_pred = pred[0]
            is_anomaly_true = row['is_anomaly']
            confidence = float(score[0])
            
            if is_anomaly_pred:
                self.anomalies_detected += 1
            
            # Confusion matrix
            if is_anomaly_true and is_anomaly_pred:
                self.true_positives += 1
            elif is_anomaly_true and not is_anomaly_pred:
                self.false_negatives += 1
            elif not is_anomaly_true and is_anomaly_pred:
                self.false_positives += 1
            else:
                self.true_negatives += 1
            
            # Print alerts
            if is_anomaly_pred:
                emoji = "🚨" if is_anomaly_true else "⚠️"
                print(f"{emoji} [{idx:6d}] ALERT: {row['anomaly_type']:15} | Conf: {confidence:.2f} | Latency: {pred_latency:.1f}ms")
            
            # Print status every 50K predictions
            if (idx + 1) % 50000 == 0:
                elapsed = time.time() - start_time
                rate = self.predictions_made / elapsed
                avg_latency = np.mean(list(self.latencies))
                print(f"\n   Progress: {idx+1:,} predictions | Rate: {rate:.0f} pred/sec | Avg Latency: {avg_latency:.2f}ms\n")
        
        return self.get_statistics()
    
    def get_statistics(self):
        """Calculate and return streaming statistics."""
        total = self.true_positives + self.false_positives + self.false_negatives + self.true_negatives
        
        stats = {
            'total_predictions': self.predictions_made,
            'anomalies_detected': self.anomalies_detected,
            'detection_rate': self.anomalies_detected / max(self.predictions_made, 1),
            'latency_stats': {
                'min_ms': float(np.min(list(self.latencies))) if self.latencies else 0,
                'max_ms': float(np.max(list(self.latencies))) if self.latencies else 0,
                'mean_ms': float(np.mean(list(self.latencies))) if self.latencies else 0,
                'median_ms': float(np.median(list(self.latencies))) if self.latencies else 0,
                'p95_ms': float(np.percentile(list(self.latencies), 95)) if self.latencies else 0,
                'p99_ms': float(np.percentile(list(self.latencies), 99)) if self.latencies else 0,
            },
            'confusion_matrix': {
                'true_positives': self.true_positives,
                'false_positives': self.false_positives,
                'false_negatives': self.false_negatives,
                'true_negatives': self.true_negatives,
            },
            'metrics': {
                'accuracy': (self.true_positives + self.true_negatives) / max(total, 1),
                'precision': self.true_positives / max((self.true_positives + self.false_positives), 1),
                'recall': self.true_positives / max((self.true_positives + self.false_negatives), 1),
                'false_alarm_rate': self.false_positives / max((self.false_positives + self.true_negatives), 1),
            }
        }
        
        return stats
    
    def print_summary(self, stats):
        """Print summary statistics."""
        print("\n" + "="*80)
        print("📊 STREAMING SIMULATION SUMMARY")
        print("="*80)
        
        print(f"\n📈 Streaming Statistics:")
        print(f"   Total Predictions: {stats['total_predictions']:,}")
        print(f"   Anomalies Detected: {stats['anomalies_detected']:,}")
        print(f"   Detection Rate: {stats['detection_rate']:.1%}")
        
        print(f"\n⏱️  Latency Statistics:")
        lat = stats['latency_stats']
        print(f"   Min:     {lat['min_ms']:.2f}ms")
        print(f"   Max:     {lat['max_ms']:.2f}ms")
        print(f"   Mean:    {lat['mean_ms']:.2f}ms")
        print(f"   Median:  {lat['median_ms']:.2f}ms")
        print(f"   P95:     {lat['p95_ms']:.2f}ms")
        print(f"   P99:     {lat['p99_ms']:.2f}ms")
        
        print(f"\n🎯 Performance Metrics:")
        met = stats['metrics']
        print(f"   Accuracy:  {met['accuracy']:.3f}")
        print(f"   Precision: {met['precision']:.3f}")
        print(f"   Recall:    {met['recall']:.3f}")
        print(f"   False Alarm Rate: {met['false_alarm_rate']:.3f}")
        
        print(f"\n✅ Confusion Matrix:")
        cm = stats['confusion_matrix']
        print(f"   TP (Correctly detected anomalies): {cm['true_positives']:,}")
        print(f"   FP (False alarms): {cm['false_positives']:,}")
        print(f"   FN (Missed anomalies): {cm['false_negatives']:,}")
        print(f"   TN (Correctly identified normal): {cm['true_negatives']:,}")
        
        print("="*80)


if __name__ == "__main__":
    # Load ensemble
    print("📂 Loading ensemble model...")
    try:
        with open('/home/claude/ensemble_comparison.json', 'r') as f:
            json.load(f)
        print("   ✓ Ensemble found")
    except:
        print("   ⚠️  Run 07_algorithm_comparison.py first!")
        exit(1)
    
    # Load data
    print("📂 Loading data...")
    df = pd.read_csv('/home/claude/network_traffic_processed.csv')
    print(f"   Loaded {len(df):,} records")
    
    # Load individual models to create ensemble
    print("📂 Loading individual models...")
    try:
        with open('/home/claude/isolation_forest_model.pkl', 'rb') as f:
            if_model = pickle.load(f)
        with open('/home/claude/lof_model.pkl', 'rb') as f:
            lof_model = pickle.load(f)
        with open('/home/claude/arima_model.pkl', 'rb') as f:
            arima_model = pickle.load(f)
        
        # Create simple ensemble class for streaming
        class SimpleEnsemble:
            def __init__(self, if_m, lof_m, arima_m):
                self.if_model = if_m
                self.lof_model = lof_m
                self.arima_model = arima_m
            
            def predict(self, X):
                # Get individual predictions
                if_pred, if_score = self.if_model.predict(X)
                lof_pred, lof_score = self.lof_model.predict(X)
                arima_pred = self.arima_model.predict(X)
                
                # Ensemble vote
                vote = if_pred + lof_pred + arima_pred
                ensemble_pred = (vote >= 2).astype(int)
                
                # Average score
                avg_score = np.mean([if_score, lof_score], axis=0)
                
                return ensemble_pred, avg_score, {}, {}
        
        ensemble = SimpleEnsemble(if_model, lof_model, arima_model)
        print("   ✓ All models loaded")
        
    except Exception as e:
        print(f"   ✗ Error: {str(e)}")
        print("   Run 04, 05, 06 scripts first!")
        exit(1)
    
    # Start streaming simulation
    print("\n" + "="*80)
    print("🚀 STREAM SIMULATOR")
    print("="*80)
    
    simulator = StreamSimulator(df, delay_ms=5)  # 5ms delay = fast simulation
    stats = simulator.stream_with_predictions(ensemble)
    
    # Print summary
    simulator.print_summary(stats)
    
    # Save statistics
    with open('/home/claude/streaming_statistics.json', 'w') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'statistics': stats
        }, f, indent=2, default=str)
    print("\n✅ Saved streaming statistics to streaming_statistics.json")
    
    print("\n🎉 Phase 4A Complete!")
