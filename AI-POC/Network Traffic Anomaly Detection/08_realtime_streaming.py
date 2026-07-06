"""
Phase 6: Real-Time Streaming Simulation
Simulates real-time network traffic processing with sliding window anomaly detection.
Expected latency: <2ms per packet.
"""

import pandas as pd
import numpy as np
import pickle
import time
from collections import deque
from datetime import datetime

class RealtimeAnomalyDetector:
    """Real-time anomaly detection using sliding window approach."""
    
    def __init__(self, window_size=100, model_path="isolation_forest_model.pkl"):
        self.window_size = window_size
        self.window = deque(maxlen=window_size)
        self.model = None
        self.load_model(model_path)
        self.stats = {
            'total_processed': 0,
            'anomalies_detected': 0,
            'processing_times': deque(maxlen=1000)
        }
    
    def load_model(self, model_path):
        """Load pre-trained model."""
        try:
            with open(model_path, "rb") as f:
                self.model = pickle.load(f)
            print(f"   ✓ Loaded model from {model_path}")
        except FileNotFoundError:
            print(f"   ⚠️  Model not found: {model_path}")
    
    def process_packet(self, packet_data):
        """Process a single packet through the detector."""
        start_time = time.time()
        
        # Add to window
        self.window.append(packet_data)
        
        # Perform detection if window is full
        anomaly_score = 0.0
        is_anomaly = False
        
        if len(self.window) == self.window_size and self.model is not None:
            window_array = np.array(list(self.window)).reshape(1, -1)
            try:
                anomaly_score = -self.model.score_samples(window_array)[0]
                is_anomaly = self.model.predict(window_array)[0] == -1
            except Exception as e:
                anomaly_score = 0.0
        
        # Update stats
        processing_time = (time.time() - start_time) * 1000  # Convert to ms
        self.stats['processing_times'].append(processing_time)
        self.stats['total_processed'] += 1
        
        if is_anomaly:
            self.stats['anomalies_detected'] += 1
        
        return {
            'is_anomaly': is_anomaly,
            'anomaly_score': anomaly_score,
            'processing_time_ms': processing_time,
            'window_full': len(self.window) == self.window_size
        }
    
    def get_stats(self):
        """Get real-time statistics."""
        if len(self.stats['processing_times']) == 0:
            return {}
        
        processing_times = list(self.stats['processing_times'])
        return {
            'total_processed': self.stats['total_processed'],
            'anomalies_detected': self.stats['anomalies_detected'],
            'anomaly_rate': self.stats['anomalies_detected'] / max(self.stats['total_processed'], 1),
            'avg_latency_ms': np.mean(processing_times),
            'max_latency_ms': np.max(processing_times),
            'min_latency_ms': np.min(processing_times),
            'p95_latency_ms': np.percentile(processing_times, 95),
            'p99_latency_ms': np.percentile(processing_times, 99)
        }
    
    def simulate_stream(self, data, delay_ms=10):
        """Simulate real-time stream processing."""
        print("   ⏳ Simulating real-time stream...")
        
        detections = []
        
        for idx, row in data.iterrows():
            # Extract features (simplified)
            features = row.values[:self.window_size] if len(row) >= self.window_size else np.pad(row.values, (0, self.window_size - len(row)))
            
            # Process packet
            result = self.process_packet(features)
            detections.append(result)
            
            # Simulate network delay
            if delay_ms > 0:
                time.sleep(delay_ms / 1000.0)
            
            if (idx + 1) % 100 == 0:
                print(f"      Processed {idx + 1} packets...")
        
        return pd.DataFrame(detections)
    
    def run_pipeline(self, test_data):
        """Execute full streaming pipeline."""
        print("\n⚡ Phase 6: Real-Time Streaming Simulation")
        print("=" * 60)
        
        # Run streaming simulation
        stream_results = self.simulate_stream(test_data, delay_ms=1)
        
        # Get statistics
        stats = self.get_stats()
        
        print(f"\n      ✓ Streaming Simulation Complete:")
        print(f"         Total packets processed: {stats.get('total_processed', 0)}")
        print(f"         Anomalies detected: {stats.get('anomalies_detected', 0)}")
        print(f"         Anomaly rate: {stats.get('anomaly_rate', 0):.2%}")
        print(f"\n      ✓ Latency Metrics:")
        print(f"         Average: {stats.get('avg_latency_ms', 0):.2f} ms (baseline: <2ms)")
        print(f"         P95: {stats.get('p95_latency_ms', 0):.2f} ms")
        print(f"         P99: {stats.get('p99_latency_ms', 0):.2f} ms")
        print(f"         Max: {stats.get('max_latency_ms', 0):.2f} ms")
        
        print(f"\n✅ Phase 6 Complete")
        
        return stream_results, stats


if __name__ == "__main__":
    # Load test data
    print("📖 Loading test data...")
    test_data = pd.read_csv("test_data.csv").drop('is_anomaly', axis=1)
    
    # Run streaming simulation
    detector = RealtimeAnomalyDetector(window_size=min(50, len(test_data.columns)))
    stream_results, stats = detector.run_pipeline(test_data.head(1000))  # Use first 1000 rows for speed
    
    # Save results
    stream_results.to_csv("streaming_results.csv", index=False)
    
    import json
    with open("streaming_stats.json", "w") as f:
        stats_serializable = {k: float(v) if isinstance(v, np.floating) else v for k, v in stats.items()}
        json.dump(stats_serializable, f, indent=2)
    
    print(f"✅ Results saved: streaming_results.csv, streaming_stats.json")
