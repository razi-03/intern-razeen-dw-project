"""
Phase 7: Alert Engine & Incident Reporting
Generates alerts, logs incidents, and creates actionable reports.
FIXED: Updated anomaly type vocabulary to match actual data (ddos, traffic_spike, congestion, server_overload).
"""

import pandas as pd
import json
from datetime import datetime
import pickle

class AlertEngine:
    """Alert and incident management system."""
    
    def __init__(self, sensitivity_level='medium'):
        self.sensitivity_level = sensitivity_level
        self.thresholds = self._set_thresholds()
        self.incidents = []
        self.alerts = []
    
    def _set_thresholds(self):
        """Set detection thresholds based on sensitivity level."""
        thresholds = {
            'high': {'anomaly_score': 0.7, 'consecutive_anomalies': 3},
            'medium': {'anomaly_score': 0.5, 'consecutive_anomalies': 5},
            'low': {'anomaly_score': 0.3, 'consecutive_anomalies': 10}
        }
        return thresholds.get(self.sensitivity_level, thresholds['medium'])
    
    def classify_alert(self, anomaly_data):
        """Classify alert severity."""
        anomaly_score = anomaly_data.get('anomaly_score', 0)
        anomaly_type = anomaly_data.get('anomaly_type', 'Unknown')
        
        # FIXED: Updated severity map to match actual anomaly types from Phase 1
        # Phase 1 generates: ddos, traffic_spike, congestion, server_overload
        severity_map = {
            'ddos': 'CRITICAL',
            'traffic_spike': 'HIGH',
            'congestion': 'MEDIUM',
            'server_overload': 'HIGH'
        }
        
        severity = severity_map.get(str(anomaly_type).lower(), 'MEDIUM')
        
        # Adjust based on score
        if anomaly_score > 0.8:
            severity = 'CRITICAL'
        elif anomaly_score > 0.6 and severity == 'MEDIUM':
            severity = 'HIGH'
        
        return severity
    
    def generate_alert(self, timestamp, anomaly_data, incident_id):
        """Generate an alert message."""
        severity = self.classify_alert(anomaly_data)
        
        alert = {
            'timestamp': str(timestamp),
            'incident_id': incident_id,
            'severity': severity,
            'anomaly_type': anomaly_data.get('anomaly_type', 'Unknown'),
            'anomaly_score': anomaly_data.get('anomaly_score', 0),
            'affected_metric': anomaly_data.get('metric', 'N/A'),
            'description': f"{severity} severity anomaly detected: {anomaly_data.get('anomaly_type')}",
            'recommended_action': self._get_recommended_action(anomaly_data.get('anomaly_type'))
        }
        
        self.alerts.append(alert)
        return alert
    
    def _get_recommended_action(self, anomaly_type):
        """Get recommended mitigation action."""
        # FIXED: Updated actions to match actual anomaly types
        actions = {
            'ddos': 'Activate DDoS protection, enable rate limiting, contact ISP',
            'traffic_spike': 'Monitor bandwidth utilization, check for unusual activity sources',
            'congestion': 'Increase capacity, optimize traffic routing, investigate bottlenecks',
            'server_overload': 'Scale up resources, redistribute load, investigate process utilization'
        }
        return actions.get(str(anomaly_type).lower(), 'Review logs and investigate')
    
    def create_incident(self, start_time, anomaly_count, anomaly_types):
        """Create an incident report."""
        incident_id = f"INC-{len(self.incidents) + 1:05d}"
        
        incident = {
            'incident_id': incident_id,
            'start_time': str(start_time),
            'anomaly_count': anomaly_count,
            'anomaly_types': anomaly_types,
            'severity': 'CRITICAL' if anomaly_count > 10 else 'HIGH' if anomaly_count > 5 else 'MEDIUM',
            'status': 'OPEN',
            'alerts': len(self.alerts),
            'created_at': datetime.now().isoformat()
        }
        
        self.incidents.append(incident)
        return incident
    
    def process_detections(self, detections_df, ground_truth=None):
        """Process detections and generate alerts."""
        print("   ⏳ Processing detections and generating alerts...")
        
        incident_count = 0
        alert_count = 0
        anomaly_cluster = []
        
        for idx, row in detections_df.iterrows():
            # Check if this is an anomaly
            is_anomaly = row.get('is_anomaly', 0) == 1
            if ground_truth is not None and idx < len(ground_truth):
                is_anomaly = ground_truth[idx] == 1
            
            if is_anomaly:
                anomaly_cluster.append(row)
                
                # Generate alert for each anomaly
                # FIXED: Handle missing columns gracefully with .get() and defaults
                alert = self.generate_alert(
                    row.get('timestamp', datetime.now()),
                    {
                        'anomaly_score': row.get('anomaly_score', 0.5),
                        'anomaly_type': row.get('anomaly_type', 'Unknown'),
                        'metric': 'network_traffic'
                    },
                    f"INC-{incident_count + 1:05d}"
                )
                alert_count += 1
            else:
                # Create incident if cluster ends
                if anomaly_cluster:
                    incident = self.create_incident(
                        anomaly_cluster[0].get('timestamp', datetime.now()),
                        len(anomaly_cluster),
                        list(set([a.get('anomaly_type', 'Unknown') for a in anomaly_cluster]))
                    )
                    incident_count += 1
                    anomaly_cluster = []
        
        # Handle final cluster
        if anomaly_cluster:
            incident = self.create_incident(
                anomaly_cluster[0].get('timestamp', datetime.now()),
                len(anomaly_cluster),
                list(set([a.get('anomaly_type', 'Unknown') for a in anomaly_cluster]))
            )
            incident_count += 1
        
        print(f"      ✓ Generated {alert_count} alerts and {incident_count} incidents")
        return alert_count, incident_count
    
    def generate_report(self):
        """Generate comprehensive incident report."""
        print("   ⏳ Generating incident report...")
        
        report = {
            'report_generated': datetime.now().isoformat(),
            'sensitivity_level': self.sensitivity_level,
            'total_incidents': len(self.incidents),
            'total_alerts': len(self.alerts),
            'incidents': self.incidents,
            'alerts': self.alerts[:100],  # Sample of alerts
            'summary': {
                'critical_count': len([a for a in self.alerts if a['severity'] == 'CRITICAL']),
                'high_count': len([a for a in self.alerts if a['severity'] == 'HIGH']),
                'medium_count': len([a for a in self.alerts if a['severity'] == 'MEDIUM']),
                'low_count': len([a for a in self.alerts if a['severity'] == 'LOW'])
            }
        }
        
        print(f"      ✓ Report generated:")
        print(f"         Total incidents: {report['total_incidents']}")
        print(f"         Total alerts: {report['total_alerts']}")
        print(f"         Critical: {report['summary']['critical_count']}")
        print(f"         High: {report['summary']['high_count']}")
        print(f"         Medium: {report['summary']['medium_count']}")
        
        return report
    
    def run_pipeline(self, test_data, ground_truth=None):
        """Execute full alert engine pipeline."""
        print("\n🚨 Phase 7: Alert Engine & Reporting")
        print("=" * 60)
        
        alert_count, incident_count = self.process_detections(test_data, ground_truth)
        report = self.generate_report()
        
        print(f"\n✅ Phase 7 Complete")
        
        return report


if __name__ == "__main__":
    # Load test data
    print("📖 Loading test data...")
    test_data = pd.read_csv("test_data.csv")
    
    # Run alert engine
    engine = AlertEngine(sensitivity_level='medium')
    report = engine.run_pipeline(test_data)
    
    # Save report
    with open("alert_engine_report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"✅ Report saved: alert_engine_report.json")
