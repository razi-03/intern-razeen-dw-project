"""
Personal Finance Categorizer - Anomaly Detection
Detects unusual spending patterns
Author: RAze
Date: 2026-07-08
"""

import statistics
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AnomalyDetector:
    """Detect unusual transactions."""
    
    def __init__(self, window_size=20):
        """
        Initialize anomaly detector.
        
        Args:
            window_size: Number of recent transactions to analyze
        """
        self.window_size = window_size
        self.anomalies = []
    
    def detect_amount_anomaly(self, transactions):
        """
        Detect transactions with unusual amounts.
        
        Flags if amount > avg + 2*stdev or < avg - 2*stdev
        """
        logger.info(f"🔍 Detecting amount anomalies...")
        
        anomalies = []
        
        # Group by category
        by_category = {}
        for txn in transactions:
            cat = txn.get('category', 'Other')
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(txn)
        
        # Analyze each category
        for category, txns in by_category.items():
            if len(txns) < 3:
                continue
            
            amounts = [abs(t.get('amount', 0)) for t in txns]
            
            try:
                avg = statistics.mean(amounts)
                stdev = statistics.stdev(amounts)
                
                for txn in txns:
                    amount = abs(txn.get('amount', 0))
                    
                    # Check if outlier
                    if stdev > 0:
                        z_score = abs((amount - avg) / stdev)
                        if z_score > 2:  # 2 standard deviations
                            anomalies.append({
                                'type': 'amount_outlier',
                                'transaction': txn,
                                'category': category,
                                'reason': f'Amount ${amount:.2f} is unusual for {category} (avg: ${avg:.2f})',
                                'severity': 'high' if z_score > 3 else 'medium'
                            })
            except:
                pass
        
        logger.info(f"   Found {len(anomalies)} amount anomalies")
        return anomalies
    
    def detect_category_anomalies(self, transactions):
        """
        Detect new or rare categories.
        """
        logger.info(f"🏷️  Detecting category anomalies...")
        
        anomalies = []
        category_counts = {}
        
        for txn in transactions:
            cat = txn.get('category', 'Other')
            category_counts[cat] = category_counts.get(cat, 0) + 1
        
        # Find rare categories (appear only once)
        for txn in transactions:
            cat = txn.get('category', 'Other')
            if category_counts[cat] == 1 and cat != 'Other':
                anomalies.append({
                    'type': 'new_category',
                    'transaction': txn,
                    'category': cat,
                    'reason': f'First time spending in {cat}',
                    'severity': 'low'
                })
        
        logger.info(f"   Found {len(anomalies)} category anomalies")
        return anomalies
    
    def detect_time_anomalies(self, transactions):
        """
        Detect unusual spending times.
        """
        logger.info(f"📅 Detecting time anomalies...")
        
        anomalies = []
        
        # Check for multiple large transactions on same day
        txn_by_date = {}
        for txn in transactions:
            date = txn.get('date', 'unknown')
            if date not in txn_by_date:
                txn_by_date[date] = []
            txn_by_date[date].append(txn)
        
        # Find dates with unusual activity
        for date, day_txns in txn_by_date.items():
            amounts = [abs(t.get('amount', 0)) for t in day_txns]
            
            if len(day_txns) > 3:  # More than 3 txns in a day
                total = sum(amounts)
                anomalies.append({
                    'type': 'high_frequency',
                    'date': date,
                    'transaction_count': len(day_txns),
                    'total_amount': total,
                    'reason': f'{len(day_txns)} transactions on {date} (total: ${total:.2f})',
                    'severity': 'medium'
                })
        
        logger.info(f"   Found {len(anomalies)} time anomalies")
        return anomalies
    
    def detect_all_anomalies(self, transactions):
        """
        Run all anomaly detection.
        
        Args:
            transactions: List of categorized transactions
        
        Returns:
            List of all anomalies found
        """
        logger.info(f"\n🔍 RUNNING ANOMALY DETECTION")
        logger.info("="*80)
        
        all_anomalies = []
        
        # Analyze recent transactions
        recent = transactions[-self.window_size:] if len(transactions) > self.window_size else transactions
        
        # Run detectors
        all_anomalies.extend(self.detect_amount_anomaly(recent))
        all_anomalies.extend(self.detect_category_anomalies(recent))
        all_anomalies.extend(self.detect_time_anomalies(recent))
        
        logger.info(f"   ✅ Total anomalies found: {len(all_anomalies)}")
        
        self.anomalies = all_anomalies
        return all_anomalies
    
    def get_anomaly_summary(self):
        """Get summary of anomalies."""
        if not self.anomalies:
            return "No anomalies detected"
        
        high_severity = len([a for a in self.anomalies if a.get('severity') == 'high'])
        medium_severity = len([a for a in self.anomalies if a.get('severity') == 'medium'])
        low_severity = len([a for a in self.anomalies if a.get('severity') == 'low'])
        
        return f"""
Anomalies Found:
- High severity: {high_severity}
- Medium severity: {medium_severity}
- Low severity: {low_severity}
        """


def main():
    """Test anomaly detector."""
    print("\n" + "="*80)
    print("🔍 ANOMALY DETECTOR - Test")
    print("="*80)
    
    detector = AnomalyDetector(window_size=20)
    
    # Test data
    test_txns = [
        {'amount': 45, 'category': 'Food', 'date': '2024-07-08'},
        {'amount': 50, 'category': 'Food', 'date': '2024-07-08'},
        {'amount': 48, 'category': 'Food', 'date': '2024-07-08'},
        {'amount': 250, 'category': 'Food', 'date': '2024-07-08'},  # Outlier
        {'amount': 89.99, 'category': 'Shopping', 'date': '2024-07-07'},
        {'amount': 150, 'category': 'New Category', 'date': '2024-07-06'},  # New category
    ]
    
    print("\n🧪 Testing anomaly detection...")
    anomalies = detector.detect_all_anomalies(test_txns)
    
    print("\n📋 Anomalies Found:")
    for anom in anomalies:
        print(f"\n   Type: {anom['type']}")
        print(f"   Severity: {anom['severity']}")
        print(f"   Reason: {anom['reason']}")
    
    print("\n" + detector.get_anomaly_summary())
    print("="*80)


if __name__ == "__main__":
    main()
