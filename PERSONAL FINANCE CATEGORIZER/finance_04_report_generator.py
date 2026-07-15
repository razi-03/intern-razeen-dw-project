"""
Personal Finance Categorizer - Report Generator
Generates CSV reports and dashboard data
Author: RAze
Date: 2026-07-08
"""

import csv
import json
from pathlib import Path
from datetime import datetime
import statistics
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ReportGenerator:
    """Generate reports from categorized transactions."""
    
    def __init__(self, currency='USD'):
        self.currency = currency
        self.reports_dir = Path('reports')
        self.reports_dir.mkdir(exist_ok=True)
    
    def get_currency_symbol(self):
        """Get currency symbol."""
        symbols = {'USD': '$', 'EUR': '€', 'GBP': '£', 'INR': '₹', 'JPY': '¥'}
        return symbols.get(self.currency, '$')
    
    def export_to_csv(self, transactions, filename='categorized_transactions.csv'):
        """
        Export categorized transactions to CSV.
        
        Args:
            transactions: List of categorized transactions
            filename: Output filename
        
        Returns:
            Path to exported file
        """
        logger.info(f"\n📊 Exporting to CSV...")
        
        output_path = self.reports_dir / filename
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Headers
            writer.writerow([
                'Date',
                'Description',
                'Amount',
                'Category',
                'Confidence',
                'Flagged as Unusual'
            ])
            
            # Rows
            for txn in transactions:
                flagged = txn.get('flagged', False)
                writer.writerow([
                    txn.get('date', ''),
                    txn.get('description', ''),
                    txn.get('amount', ''),
                    txn.get('category', 'Other'),
                    f"{txn.get('confidence', 0):.0%}",
                    'Yes' if flagged else 'No'
                ])
        
        logger.info(f"   ✅ Exported to {output_path}")
        return output_path
    
    def get_category_summary(self, transactions):
        """
        Get spending by category.
        
        Args:
            transactions: List of transactions
        
        Returns:
            Dict with category totals and percentages
        """
        logger.info(f"\n📈 Calculating category summary...")
        
        by_category = {}
        
        for txn in transactions:
            cat = txn.get('category', 'Other')
            amount = abs(txn.get('amount', 0))
            
            if cat not in by_category:
                by_category[cat] = {'total': 0, 'count': 0, 'transactions': []}
            
            by_category[cat]['total'] += amount
            by_category[cat]['count'] += 1
            by_category[cat]['transactions'].append(txn)
        
        # Calculate percentages
        total_spent = sum(c['total'] for c in by_category.values())
        
        summary = {}
        for cat, data in by_category.items():
            summary[cat] = {
                'total': round(data['total'], 2),
                'count': data['count'],
                'percentage': round(data['total'] / max(total_spent, 1) * 100, 1),
                'avg': round(data['total'] / data['count'], 2)
            }
        
        # Sort by total
        summary = dict(sorted(summary.items(), key=lambda x: x[1]['total'], reverse=True))
        
        return summary
    
    def get_top_merchants(self, transactions, top_n=10):
        """Get top merchants by spending."""
        logger.info(f"\n💳 Finding top merchants...")
        
        by_merchant = {}
        
        for txn in transactions:
            desc = txn.get('description', 'Unknown')
            amount = abs(txn.get('amount', 0))
            
            if desc not in by_merchant:
                by_merchant[desc] = {'total': 0, 'count': 0}
            
            by_merchant[desc]['total'] += amount
            by_merchant[desc]['count'] += 1
        
        # Sort and limit
        sorted_merchants = sorted(
            by_merchant.items(),
            key=lambda x: x[1]['total'],
            reverse=True
        )[:top_n]
        
        return {desc: data for desc, data in sorted_merchants}
    
    def get_spending_stats(self, transactions):
        """Get statistical summary of spending."""
        logger.info(f"\n📊 Calculating spending statistics...")
        
        amounts = [abs(t.get('amount', 0)) for t in transactions]
        
        if not amounts:
            return {}
        
        return {
            'total_transactions': len(transactions),
            'total_spent': round(sum(amounts), 2),
            'average_transaction': round(statistics.mean(amounts), 2),
            'median_transaction': round(statistics.median(amounts), 2),
            'min_transaction': round(min(amounts), 2),
            'max_transaction': round(max(amounts), 2),
            'std_deviation': round(statistics.stdev(amounts), 2) if len(amounts) > 1 else 0
        }
    
    def generate_dashboard_data(self, transactions, anomalies):
        """
        Generate data for dashboard display.
        
        Args:
            transactions: List of categorized transactions
            anomalies: List of anomalies
        
        Returns:
            Dict with all dashboard data
        """
        logger.info(f"\n🎨 Generating dashboard data...")
        
        symbol = self.get_currency_symbol()
        
        data = {
            'currency': self.currency,
            'currency_symbol': symbol,
            'timestamp': datetime.now().isoformat(),
            'transactions': transactions,
            'statistics': self.get_spending_stats(transactions),
            'by_category': self.get_category_summary(transactions),
            'top_merchants': self.get_top_merchants(transactions),
            'anomalies': anomalies,
            'anomaly_count': len(anomalies),
            'high_severity_count': len([a for a in anomalies if a.get('severity') == 'high']),
            'medium_severity_count': len([a for a in anomalies if a.get('severity') == 'medium']),
            'low_severity_count': len([a for a in anomalies if a.get('severity') == 'low'])
        }
        
        return data
    
    def save_dashboard_data(self, data, filename='dashboard_data.json'):
        """Save dashboard data to JSON."""
        output_path = self.reports_dir / filename
        
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        logger.info(f"   ✅ Saved to {output_path}")
        return output_path
    
    def print_summary(self, data):
        """Print text summary."""
        symbol = data['currency_symbol']
        stats = data['statistics']
        categories = data['by_category']
        
        print("\n" + "="*80)
        print("💰 SPENDING SUMMARY")
        print("="*80)
        
        print(f"\n📊 Overall Statistics:")
        print(f"   Total Transactions: {stats['total_transactions']}")
        print(f"   Total Spent: {symbol}{stats['total_spent']:.2f}")
        print(f"   Average: {symbol}{stats['average_transaction']:.2f}")
        print(f"   Median: {symbol}{stats['median_transaction']:.2f}")
        print(f"   Range: {symbol}{stats['min_transaction']:.2f} - {symbol}{stats['max_transaction']:.2f}")
        
        print(f"\n📈 By Category:")
        for cat, info in categories.items():
            print(f"   {cat}: {symbol}{info['total']:.2f} ({info['percentage']:.1f}%)")
            print(f"      {info['count']} transactions, avg {symbol}{info['avg']:.2f}")
        
        if data['anomaly_count'] > 0:
            print(f"\n⚠️  Anomalies Detected: {data['anomaly_count']}")
            print(f"   High severity: {data['high_severity_count']}")
            print(f"   Medium severity: {data['medium_severity_count']}")
            print(f"   Low severity: {data['low_severity_count']}")


def main():
    """Test report generator."""
    print("\n" + "="*80)
    print("📊 REPORT GENERATOR - Test")
    print("="*80)
    
    gen = ReportGenerator(currency='USD')
    
    # Test data
    test_txns = [
        {
            'date': '2024-07-08',
            'description': 'Starbucks',
            'amount': 45.50,
            'category': 'Food',
            'confidence': 0.95,
            'flagged': False
        },
        {
            'date': '2024-07-08',
            'description': 'Uber',
            'amount': 12.00,
            'category': 'Transportation',
            'confidence': 0.98,
            'flagged': False
        },
        {
            'date': '2024-07-07',
            'description': 'Amazon',
            'amount': 89.99,
            'category': 'Shopping',
            'confidence': 0.92,
            'flagged': True
        },
    ]
    
    test_anomalies = [
        {
            'type': 'amount_outlier',
            'reason': 'High amount for category',
            'severity': 'medium'
        }
    ]
    
    print("\n🧪 Testing report generation...")
    
    # Generate
    data = gen.generate_dashboard_data(test_txns, test_anomalies)
    
    # Export
    gen.export_to_csv(test_txns)
    gen.save_dashboard_data(data)
    
    # Print
    gen.print_summary(data)
    
    print("\n✅ TEST COMPLETE!")
    print("="*80)


if __name__ == "__main__":
    main()
