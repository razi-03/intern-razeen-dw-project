"""
Phase 1: Network Traffic Anomaly Detection - Synthetic Data Generator
Purpose: Generate 500K realistic network metrics with injected anomalies
Author: RAze
Date: 2026-07-01
Runtime: ~30 seconds
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

# Set seed for reproducibility
np.random.seed(42)

class NetworkTrafficGenerator:
    """Generate realistic network traffic data with injected anomalies."""
    
    def __init__(self, num_rows=500000, anomaly_rate=0.10):
        """
        Args:
            num_rows: Total number of records to generate (500K = 30 days @ 10-sec intervals)
            anomaly_rate: Percentage of anomalies to inject (10%)
        """
        self.num_rows = num_rows
        self.anomaly_rate = anomaly_rate
        self.num_anomalies = int(num_rows * anomaly_rate)
        
        # Anomaly types and their properties
        self.anomaly_types = {
            'ddos': {'freq': 0.30, 'duration_range': (30, 300)},           # DDoS attack
            'traffic_spike': {'freq': 0.25, 'duration_range': (60, 600)},   # Legitimate spike
            'congestion': {'freq': 0.25, 'duration_range': (300, 1200)},    # Network congestion
            'server_overload': {'freq': 0.20, 'duration_range': (120, 600)} # Server overload
        }
        
        print(f"📊 Initializing Network Traffic Generator")
        print(f"   Total records: {num_rows:,}")
        print(f"   Anomaly rate: {anomaly_rate:.0%}")
        print(f"   Expected anomalies: {self.num_anomalies:,}")
    
    def generate_baseline_metrics(self):
        """Generate normal (non-anomalous) network metrics."""
        # Time range: 30 days of data
        start_time = datetime(2026, 6, 1, 0, 0, 0)
        timestamps = [start_time + timedelta(seconds=10*i) for i in range(self.num_rows)]
        
        # Normal traffic patterns (daily + weekly seasonality)
        hours = np.array([ts.hour for ts in timestamps])
        days = np.array([ts.weekday() for ts in timestamps])
        
        # Base traffic (varies by hour of day)
        base_packets = 1000 + 500 * np.sin(2 * np.pi * hours / 24)
        base_bandwidth = 500 + 200 * np.sin(2 * np.pi * hours / 24)
        
        # Add weekly seasonality (higher on weekdays)
        weekday_factor = np.where(days < 5, 1.2, 0.8)
        base_packets *= weekday_factor
        base_bandwidth *= weekday_factor
        
        # Add noise to make it realistic
        packets = base_packets + np.random.normal(0, 50, self.num_rows)
        packets = np.maximum(packets, 50)  # Minimum baseline
        
        bandwidth = base_bandwidth + np.random.normal(0, 20, self.num_rows)
        bandwidth = np.maximum(bandwidth, 50)
        
        # Other metrics (correlated with traffic)
        latency = 10 + 2 * (packets / 1000) + np.random.normal(0, 1, self.num_rows)
        latency = np.maximum(latency, 1)
        
        connections = np.random.normal(5000, 500, self.num_rows)
        connections = np.maximum(connections, 100)
        
        error_rate = 0.01 + 0.001 * (packets / 1000) + np.random.normal(0, 0.002, self.num_rows)
        error_rate = np.clip(error_rate, 0, 0.1)
        
        cpu_usage = 20 + 15 * np.sin(2 * np.pi * hours / 24) + np.random.normal(0, 3, self.num_rows)
        cpu_usage = np.clip(cpu_usage, 5, 95)
        
        memory_usage = 40 + 10 * np.random.randn(self.num_rows)
        memory_usage = np.clip(memory_usage, 10, 90)
        
        return {
                'timestamp': timestamps,
                'packets_per_sec': packets,
                'bandwidth_mbps': bandwidth,
                'latency_ms': latency,
                'active_connections': connections,  # keep as float until final DataFrame step
                'error_rate': error_rate,
                'cpu_usage': cpu_usage,
                'memory_usage': memory_usage
                }
    
    def inject_anomalies(self, data):
        """Inject realistic anomalies into the dataset."""
        is_anomaly = np.zeros(self.num_rows, dtype=bool)
        anomaly_type = np.full(self.num_rows, 'normal', dtype=object)
        
        # Randomly select anomaly indices
        anomaly_indices = np.random.choice(
            self.num_rows, 
            size=self.num_anomalies, 
            replace=False
        )
        
        # Assign anomaly types based on frequency
        types = list(self.anomaly_types.keys())
        type_counts = [int(self.num_anomalies * self.anomaly_types[t]['freq']) for t in types]
        type_counts[-1] += self.num_anomalies - sum(type_counts)  # Adjust for rounding
        
        type_assignments = []
        for atype, count in zip(types, type_counts):
            type_assignments.extend([atype] * count)
        
        np.random.shuffle(type_assignments)
        
        modified = np.zeros(self.num_rows, dtype=bool)  # tracks rows already scaled
        total_marked = 0  # tracks how many rows have been flagged anomalous so far
        
        # Inject anomalies
        for idx, anom_type in zip(anomaly_indices, type_assignments):
            # Stop once we've hit the intended overall anomaly budget
            if total_marked >= self.num_anomalies:
                break
            
            # Create anomaly clusters (multiple consecutive points)
            duration = np.random.randint(*self.anomaly_types[anom_type]['duration_range'])
            cluster_start = max(0, idx - duration // 2)
            cluster_end = min(self.num_rows, idx + duration // 2)
            
            # Skip if this region overlaps one already modified, to avoid
            # compounding multipliers on the same rows
            if modified[cluster_start:cluster_end].any():
                continue
            
            # Trim the cluster so it doesn't push the total past the
            # intended anomaly_rate budget (e.g. ~10% of rows)
            remaining_budget = self.num_anomalies - total_marked
            if (cluster_end - cluster_start) > remaining_budget:
                cluster_end = cluster_start + remaining_budget
                if cluster_end <= cluster_start:
                    continue
            
            modified[cluster_start:cluster_end] = True
            total_marked += (cluster_end - cluster_start)
            is_anomaly[idx] = True
            anomaly_type[idx] = anom_type
            
            if anom_type == 'ddos':
                # 2-5x traffic spike
                multiplier = np.random.uniform(2, 5)
                data['packets_per_sec'][cluster_start:cluster_end] *= multiplier
                data['bandwidth_mbps'][cluster_start:cluster_end] *= multiplier
                data['latency_ms'][cluster_start:cluster_end] *= 1.5
                data['error_rate'][cluster_start:cluster_end] *= 2
                data['cpu_usage'][cluster_start:cluster_end] += 30
                is_anomaly[cluster_start:cluster_end] = True
                anomaly_type[cluster_start:cluster_end] = anom_type
            
            elif anom_type == 'traffic_spike':
                # Legitimate spike (1.5-2.5x)
                multiplier = np.random.uniform(1.5, 2.5)
                data['packets_per_sec'][cluster_start:cluster_end] *= multiplier
                data['bandwidth_mbps'][cluster_start:cluster_end] *= multiplier
                is_anomaly[cluster_start:cluster_end] = True
                anomaly_type[cluster_start:cluster_end] = anom_type
            
            elif anom_type == 'congestion':
                # High latency with errors
                data['latency_ms'][cluster_start:cluster_end] *= np.random.uniform(3, 5)
                data['error_rate'][cluster_start:cluster_end] *= 3
                data['packets_per_sec'][cluster_start:cluster_end] *= 0.5  # Dropped packets
                is_anomaly[cluster_start:cluster_end] = True
                anomaly_type[cluster_start:cluster_end] = anom_type
            
            elif anom_type == 'server_overload':
                # CPU/memory spike with correlated metrics
                data['cpu_usage'][cluster_start:cluster_end] += 40
                data['memory_usage'][cluster_start:cluster_end] += 30
                data['latency_ms'][cluster_start:cluster_end] *= 2
                data['active_connections'][cluster_start:cluster_end] *= 0.7
                is_anomaly[cluster_start:cluster_end] = True
                anomaly_type[cluster_start:cluster_end] = anom_type
        
        return is_anomaly, anomaly_type
    
    def generate(self):
        """Generate complete dataset with anomalies."""
        print("\n🔄 Generating baseline metrics...")
        data = self.generate_baseline_metrics()
        
        print("💉 Injecting anomalies...")
        is_anomaly, anomaly_type = self.inject_anomalies(data)
        
        print("📦 Creating DataFrame...")
        df = pd.DataFrame({
            'timestamp': data['timestamp'],
            'packets_per_sec': np.maximum(data['packets_per_sec'], 1),
            'bandwidth_mbps': np.maximum(data['bandwidth_mbps'], 1),
            'latency_ms': np.maximum(data['latency_ms'], 0.1),
            'active_connections': np.maximum(data['active_connections'].astype(int), 1),
            'error_rate': np.clip(data['error_rate'], 0, 1),
            'cpu_usage': np.clip(data['cpu_usage'], 0, 100),
            'memory_usage': np.clip(data['memory_usage'], 0, 100),
            'is_anomaly': is_anomaly,
            'anomaly_type': anomaly_type
        })
        
        return df


class DataValidator:
    """Validate generated network traffic data."""
    
    @staticmethod
    def validate(df):
        """Perform validation checks."""
        print("\n🔍 Validating data...")
        issues = []
        
        # Check shape
        if len(df) != 500000:
            issues.append(f"⚠️  Expected 500K rows, got {len(df)}")
        
        # Check columns
        required_cols = [
            'timestamp', 'packets_per_sec', 'bandwidth_mbps', 'latency_ms',
            'active_connections', 'error_rate', 'cpu_usage', 'memory_usage',
            'is_anomaly', 'anomaly_type'
        ]
        missing = [col for col in required_cols if col not in df.columns]
        if missing:
            issues.append(f"⚠️  Missing columns: {missing}")
        
        # Check nulls
        nulls = df.isnull().sum().sum()
        if nulls > 0:
            issues.append(f"⚠️  Found {nulls} null values")
        
        # Check value ranges
        if (df['error_rate'] < 0).any() or (df['error_rate'] > 1).any():
            issues.append("⚠️  error_rate out of [0, 1] range")
        
        if (df['cpu_usage'] < 0).any() or (df['cpu_usage'] > 100).any():
            issues.append("⚠️  cpu_usage out of [0, 100] range")
        
        if (df['packets_per_sec'] < 0).any():
            issues.append("⚠️  packets_per_sec has negative values")
        
        # Check anomaly rate
        anomaly_count = df['is_anomaly'].sum()
        actual_rate = anomaly_count / len(df)
        print(f"   Anomalies: {anomaly_count:,} ({actual_rate:.1%})")
        
        if issues:
            print("\n❌ Validation Issues:")
            for issue in issues:
                print(issue)
            return False
        
        print("✅ All validation checks passed!")
        return True


class DataSummary:
    """Generate summary statistics for the dataset."""
    
    @staticmethod
    def print_summary(df):
        """Print human-readable summary."""
        print("\n" + "="*70)
        print("📊 NETWORK TRAFFIC DATASET SUMMARY")
        print("="*70)
        
        print(f"\n📈 Dataset Size: {len(df):,} records")
        print(f"📅 Time Range: {df['timestamp'].min().date()} to {df['timestamp'].max().date()}")
        print(f"⏱️  Duration: 30 days (10-second intervals)")
        
        print("\n📊 Metrics Summary:")
        metrics = ['packets_per_sec', 'bandwidth_mbps', 'latency_ms', 'active_connections', 'error_rate', 'cpu_usage', 'memory_usage']
        for metric in metrics:
            print(f"   {metric:25} min:{df[metric].min():8.2f}  avg:{df[metric].mean():8.2f}  max:{df[metric].max():8.2f}")
        
        print("\n🚨 Anomaly Distribution:")
        for atype in ['normal', 'ddos', 'traffic_spike', 'congestion', 'server_overload']:
            count = (df['anomaly_type'] == atype).sum()
            pct = (count / len(df)) * 100
            bar = '█' * int(pct / 2)
            print(f"   {atype:20} {count:8,} ({pct:5.1f}%) {bar}")
        
        print("\n🔗 Correlation Analysis:")
        print(f"   packets ↔ bandwidth: {df['packets_per_sec'].corr(df['bandwidth_mbps']):.3f}")
        print(f"   traffic ↔ latency:   {df['packets_per_sec'].corr(df['latency_ms']):.3f}")
        print(f"   error_rate ↔ cpu:    {df['error_rate'].corr(df['cpu_usage']):.3f}")
        print(f"   connections ↔ cpu:   {df['active_connections'].corr(df['cpu_usage']):.3f}")
        
        print("\n⏰ Temporal Statistics:")
        hourly_avg = df.groupby(df['timestamp'].dt.hour)['packets_per_sec'].mean()
        print(f"   Peak hour: {hourly_avg.idxmax()}:00 ({hourly_avg.max():.0f} pps)")
        print(f"   Quiet hour: {hourly_avg.idxmin()}:00 ({hourly_avg.min():.0f} pps)")
        
        print("="*70)
    
    @staticmethod
    def generate_report(df):
        """Generate JSON report."""
        report = {
            'timestamp': datetime.now().isoformat(),
            'dataset_info': {
                'total_rows': len(df),
                'total_features': len(df.columns) - 1,  # Exclude timestamp
                'date_range': f"{df['timestamp'].min().date()} to {df['timestamp'].max().date()}",
                'interval_seconds': 10,
                'total_days': 30
            },
            'metrics_summary': {
                metric: {
                    'min': float(df[metric].min()),
                    'max': float(df[metric].max()),
                    'mean': float(df[metric].mean()),
                    'std': float(df[metric].std()),
                    'median': float(df[metric].median())
                }
                for metric in ['packets_per_sec', 'bandwidth_mbps', 'latency_ms', 'active_connections', 'error_rate', 'cpu_usage', 'memory_usage']
            },
            'anomalies': {
                'total_anomalies': int(df['is_anomaly'].sum()),
                'anomaly_rate': float(df['is_anomaly'].mean()),
                'distribution': {
                    atype: int((df['anomaly_type'] == atype).sum())
                    for atype in df['anomaly_type'].unique()
                }
            },
            'correlations': {
                'packets_vs_bandwidth': float(df['packets_per_sec'].corr(df['bandwidth_mbps'])),
                'packets_vs_latency': float(df['packets_per_sec'].corr(df['latency_ms'])),
                'error_rate_vs_cpu': float(df['error_rate'].corr(df['cpu_usage'])),
                'connections_vs_cpu': float(df['active_connections'].corr(df['cpu_usage']))
            }
        }
        
        return report


if __name__ == "__main__":
    # Generate data
    print("🚀 Starting Network Traffic Data Generation\n")
    
    generator = NetworkTrafficGenerator(num_rows=500000, anomaly_rate=0.10)
    df = generator.generate()
    
    # Validate
    validator = DataValidator()
    validator.validate(df)
    
    # Summary
    summary = DataSummary()
    summary.print_summary(df)
    
    # Save data
    print("\n💾 Saving data...")
    df.to_csv('network_traffic_raw.csv', index=False)
    print("✅ Saved to network_traffic_raw.csv")
    
    # Save report
    report = summary.generate_report(df)
    with open('network_traffic_eda.json', 'w') as f:
        json.dump(report, f, indent=2, default=str)
    print("✅ Saved EDA report to network_traffic_eda.json")
    
    # Show sample
    print("\n📋 Sample Data (first 10 rows):")
    print(df.head(10).to_string())
    
    print("\n🎉 Phase 1 Complete!")