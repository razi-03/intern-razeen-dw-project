"""
Anomaly Detection Phase 4B: Alert Engine
Purpose: Alert generation, escalation, and management
Author: RAze
Date: 2026-07-01
Runtime: ~30 seconds
"""

import json
import pandas as pd
from datetime import datetime
from collections import defaultdict

class AlertEngine:
    """Alert generation and escalation system."""
    
    def __init__(self, sensitivity='medium'):
        """
        Args:
            sensitivity: 'low', 'medium', or 'high'
                - low: threshold=0.7 (fewer alerts, may miss some)
                - medium: threshold=0.6 (balanced)
                - high: threshold=0.5 (more alerts, more false positives)
        """
        self.sensitivities = {
            'low': {'threshold': 0.7, 'severity': 'low'},
            'medium': {'threshold': 0.6, 'severity': 'medium'},
            'high': {'threshold': 0.5, 'severity': 'high'}
        }
        self.sensitivity = sensitivity
        self.threshold = self.sensitivities[sensitivity]['threshold']
        
        self.alerts = []
        self.false_alarms = []
        self.alert_count = defaultdict(int)
        
        print(f"🔔 Alert Engine Initialized")
        print(f"   Sensitivity: {sensitivity}")
        print(f"   Threshold: {self.threshold:.1f}")
    
    def should_alert(self, confidence):
        """Determine if alert should be triggered based on confidence."""
        return confidence >= self.threshold
    
    def determine_severity(self, confidence, anomaly_type):
        """
        Determine alert severity based on confidence and anomaly type.
        
        Returns: 'low', 'medium', or 'high'
        """
        if anomaly_type == 'ddos':
            # DDoS is always high severity
            return 'high'
        elif anomaly_type == 'congestion':
            if confidence > 0.85:
                return 'high'
            else:
                return 'medium'
        elif anomaly_type == 'server_overload':
            return 'high' if confidence > 0.80 else 'medium'
        else:
            # traffic_spike, others
            return 'medium' if confidence > 0.75 else 'low'
    
    def escalate(self, severity):
        """
        Determine escalation action based on severity.
        
        Returns: escalation action
        - 'log': Only log (no action)
        - 'slack': Send to ops Slack channel
        - 'pagerduty': Page on-call engineer
        """
        if severity == 'high':
            return 'pagerduty'
        elif severity == 'medium':
            return 'slack'
        else:
            return 'log'
    
    def create_alert(self, timestamp, metric_values, anomaly_type, confidence, model_votes):
        """Create and record an alert."""
        severity = self.determine_severity(confidence, anomaly_type)
        escalation = self.escalate(severity)
        
        alert = {
            'timestamp': str(timestamp),
            'anomaly_type': anomaly_type,
            'confidence': float(confidence),
            'severity': severity,
            'escalation': escalation,
            'metrics': {
                'packets_per_sec': float(metric_values.get('packets_per_sec', 0)),
                'bandwidth_mbps': float(metric_values.get('bandwidth_mbps', 0)),
                'latency_ms': float(metric_values.get('latency_ms', 0)),
                'cpu_usage': float(metric_values.get('cpu_usage', 0)),
                'error_rate': float(metric_values.get('error_rate', 0)),
            },
            'model_votes': model_votes,
            'created_at': datetime.now().isoformat()
        }
        
        self.alerts.append(alert)
        self.alert_count[anomaly_type] += 1
        
        return alert
    
    def mark_false_alarm(self, alert_idx):
        """Mark an alert as a false alarm for model retraining."""
        if alert_idx < len(self.alerts):
            alert = self.alerts[alert_idx]
            alert['is_false_alarm'] = True
            self.false_alarms.append(alert)
            print(f"   ⚠️  Marked as false alarm: {alert['anomaly_type']}")
    
    def get_statistics(self):
        """Get alert statistics."""
        total_alerts = len(self.alerts)
        false_alarm_count = len(self.false_alarms)
        false_alarm_rate = false_alarm_count / max(total_alerts, 1)
        
        stats = {
            'total_alerts': total_alerts,
            'false_alarms': false_alarm_count,
            'false_alarm_rate': float(false_alarm_rate),
            'alerts_by_type': dict(self.alert_count),
            'alerts_by_severity': {
                'high': sum(1 for a in self.alerts if a['severity'] == 'high'),
                'medium': sum(1 for a in self.alerts if a['severity'] == 'medium'),
                'low': sum(1 for a in self.alerts if a['severity'] == 'low'),
            },
            'escalations': {
                'pagerduty': sum(1 for a in self.alerts if a['escalation'] == 'pagerduty'),
                'slack': sum(1 for a in self.alerts if a['escalation'] == 'slack'),
                'log': sum(1 for a in self.alerts if a['escalation'] == 'log'),
            }
        }
        
        return stats
    
    def print_statistics(self):
        """Print alert statistics."""
        stats = self.get_statistics()
        
        print("\n" + "="*80)
        print("📊 ALERT ENGINE STATISTICS")
        print("="*80)
        
        print(f"\n🚨 Alert Summary:")
        print(f"   Total Alerts: {stats['total_alerts']:,}")
        print(f"   False Alarms: {stats['false_alarms']:,}")
        print(f"   False Alarm Rate: {stats['false_alarm_rate']:.2%}")
        
        print(f"\n📂 Alerts by Type:")
        for atype, count in stats['alerts_by_type'].items():
            print(f"   {atype:20}: {count:6,}")
        
        print(f"\n⚠️  Alerts by Severity:")
        for severity, count in stats['alerts_by_severity'].items():
            print(f"   {severity:20}: {count:6,}")
        
        print(f"\n🔔 Escalations:")
        for action, count in stats['escalations'].items():
            print(f"   {action:20}: {count:6,}")
        
        print("="*80)
        
        return stats


class AlertSimulator:
    """Simulate alert processing from streaming predictions."""
    
    def __init__(self, engine):
        self.engine = engine
        self.alerts_triggered = 0
    
    def process_prediction(self, row, prediction, confidence, model_votes):
        """Process a single prediction and create alert if needed."""
        if self.engine.should_alert(confidence):
            alert = self.engine.create_alert(
                timestamp=row['timestamp'],
                metric_values={
                    'packets_per_sec': row['packets_per_sec'],
                    'bandwidth_mbps': row['bandwidth_mbps'],
                    'latency_ms': row['latency_ms'],
                    'cpu_usage': row['cpu_usage'],
                    'error_rate': row['error_rate'],
                },
                anomaly_type=row['anomaly_type'],
                confidence=confidence,
                model_votes=model_votes
            )
            
            self.alerts_triggered += 1
            return alert
        
        return None


if __name__ == "__main__":
    # Load test data
    print("📂 Loading test data...")
    df = pd.read_csv('/home/claude/network_traffic_processed.csv')
    print(f"   Loaded {len(df):,} records")
    
    print("\n" + "="*80)
    print("🔔 ALERT ENGINE TEST")
    print("="*80)
    
    # Create alert engines with different sensitivities
    engines = {
        'low': AlertEngine(sensitivity='low'),
        'medium': AlertEngine(sensitivity='medium'),
        'high': AlertEngine(sensitivity='high'),
    }
    
    # Simulate alerts
    print("\n🚀 Simulating alerts on test data...\n")
    
    for sensitivity_level, engine in engines.items():
        simulator = AlertSimulator(engine)
        
        # Simulate predictions (use is_anomaly as proxy)
        for idx, (_, row) in enumerate(df.iterrows()):
            if idx % 50000 == 0:
                print(f"   [{sensitivity_level}] Processing: {idx:,} / {len(df):,}")
            
            # Simulate confidence based on anomaly type
            if row['is_anomaly']:
                confidence = 0.8 if row['anomaly_type'] != 'traffic_spike' else 0.65
            else:
                confidence = 0.3
            
            # Simple model votes (2 out of 3)
            model_votes = {
                'isolation_forest': row['is_anomaly'],
                'lof': row['is_anomaly'],
                'arima': row['is_anomaly'] if confidence > 0.7 else False
            }
            
            alert = simulator.process_prediction(
                row,
                prediction=row['is_anomaly'],
                confidence=confidence,
                model_votes=model_votes
            )
        
        print(f"   [{sensitivity_level}] Complete: {simulator.alerts_triggered:,} alerts triggered\n")
    
    # Print statistics
    for sensitivity_level, engine in engines.items():
        print(f"\n{'='*80}")
        print(f"SENSITIVITY: {sensitivity_level.upper()}")
        stats = engine.get_statistics()
        print(f"{'='*80}")
        print(f"Total Alerts: {stats['total_alerts']:,}")
        print(f"False Alarm Rate: {stats['false_alarm_rate']:.2%}")
        print(f"High Severity: {stats['alerts_by_severity']['high']:,}")
        print(f"Medium Severity: {stats['alerts_by_severity']['medium']:,}")
        print(f"Low Severity: {stats['alerts_by_severity']['low']:,}")
    
    # Save alert engine configuration
    alert_config = {
        'timestamp': datetime.now().isoformat(),
        'sensitivities': {
            'low': {'threshold': 0.7, 'description': 'Few alerts, may miss some anomalies'},
            'medium': {'threshold': 0.6, 'description': 'Balanced approach'},
            'high': {'threshold': 0.5, 'description': 'Many alerts, more false positives'},
        },
        'escalation_matrix': {
            'high': 'PagerDuty (page on-call)',
            'medium': 'Slack (notify ops)',
            'low': 'Log only',
        },
        'anomaly_severity': {
            'ddos': 'Always high (revenue threat)',
            'congestion': 'Medium-High (service degradation)',
            'server_overload': 'High (potential outage)',
            'traffic_spike': 'Low-Medium (may be legitimate)',
        }
    }
    
    with open('/home/claude/alert_configuration.json', 'w') as f:
        json.dump(alert_config, f, indent=2)
    print("\n✅ Saved alert configuration to alert_configuration.json")
    
    print("\n🎉 Phase 4B Complete!")
