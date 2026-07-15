"""
Personal Finance Categorizer - CSV Handler & Currency Detection
Reads bank statements and detects currency automatically
Author: RAze
Date: 2026-07-08
"""

import csv
from pathlib import Path
import re
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CurrencyDetector:
    """Auto-detect currency from transactions."""
    
    CURRENCY_SYMBOLS = {
        '$': 'USD',
        '€': 'EUR',
        '£': 'GBP',
        '¥': 'JPY',
        '₹': 'INR',
        '₽': 'RUB',
        'C$': 'CAD',
        'A$': 'AUD',
    }
    
    CURRENCY_CODES = {
        'USD': '$',
        'EUR': '€',
        'GBP': '£',
        'JPY': '¥',
        'INR': '₹',
        'RUB': '₽',
        'CAD': 'C$',
        'AUD': 'A$',
    }
    
    @staticmethod
    def detect_currency(transactions):
        """
        Auto-detect currency from transactions.
        
        Args:
            transactions: List of dicts with 'amount' field
        
        Returns:
            Currency code (e.g., 'USD', 'EUR', 'INR')
        """
        logger.info("💱 Detecting currency...")
        
        if not transactions:
            return 'USD'  # Default
        
        # Check descriptions and amounts for currency hints
        amount_str = str(transactions[0].get('amount', ''))
        desc = transactions[0].get('description', '').upper()
        
        # Check for currency symbols
        for symbol, code in CurrencyDetector.CURRENCY_SYMBOLS.items():
            if symbol in amount_str or symbol in desc:
                logger.info(f"   ✅ Detected: {code}")
                return code
        
        # Check for country hints in description
        if 'INR' in desc or 'RUPEE' in desc or 'India' in desc:
            return 'INR'
        if 'GBP' in desc or 'POUND' in desc or 'UK' in desc:
            return 'GBP'
        if 'EUR' in desc or 'EURO' in desc or 'Europe' in desc:
            return 'EUR'
        
        # Check amount format (thousand separator hints)
        if ',' in amount_str and '.' in amount_str:
            # European format (1.234,56)
            return 'EUR'
        
        logger.info(f"   ℹ️  Default: USD")
        return 'USD'


class CSVHandler:
    """Handle CSV bank statement files."""
    
    def __init__(self):
        self.transactions = []
        self.currency = 'USD'
    
    def detect_csv_format(self, csv_path):
        """
        Detect CSV format automatically.
        Looks for common column names.
        """
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            headers = next(reader)
        
        headers_lower = [h.lower() for h in headers]
        
        # Find column indices
        date_idx = None
        desc_idx = None
        amount_idx = None
        
        for i, h in enumerate(headers_lower):
            if any(x in h for x in ['date', 'transaction date', 'posted']):
                date_idx = i
            if any(x in h for x in ['description', 'merchant', 'details', 'note']):
                desc_idx = i
            if any(x in h for x in ['amount', 'debit', 'credit', 'withdrawal', 'deposit']):
                amount_idx = i
        
        logger.info(f"📋 Detected CSV format:")
        logger.info(f"   Date column: {date_idx} ({headers[date_idx] if date_idx else 'unknown'})")
        logger.info(f"   Description column: {desc_idx} ({headers[desc_idx] if desc_idx else 'unknown'})")
        logger.info(f"   Amount column: {amount_idx} ({headers[amount_idx] if amount_idx else 'unknown'})")
        
        return date_idx, desc_idx, amount_idx
    
    def parse_amount(self, amount_str):
        """Parse amount from string."""
        # Remove currency symbols
        amount_str = str(amount_str).strip()
        for symbol in CurrencyDetector.CURRENCY_SYMBOLS.keys():
            amount_str = amount_str.replace(symbol, '')
        
        # Extract numbers
        match = re.search(r'[\d,.\-]+', amount_str)
        if match:
            num = match.group().replace(',', '')
            try:
                return float(num)
            except:
                return 0.0
        
        return 0.0
    
    def parse_date(self, date_str):
        """Parse date from string."""
        date_formats = [
            '%Y-%m-%d',
            '%m/%d/%Y',
            '%d/%m/%Y',
            '%Y/%m/%d',
            '%b %d, %Y',
            '%d %b %Y',
        ]
        
        for fmt in date_formats:
            try:
                return datetime.strptime(date_str.strip(), fmt).strftime('%Y-%m-%d')
            except:
                continue
        
        return date_str.strip()
    
    def load_csv(self, csv_path):
        """
        Load transactions from CSV.
        
        Args:
            csv_path: Path to CSV file
        
        Returns:
            List of transactions
        """
        csv_path = Path(csv_path)
        
        if not csv_path.exists():
            logger.error(f"File not found: {csv_path}")
            return []
        
        logger.info(f"📂 Loading CSV: {csv_path.name}")
        
        # Detect format
        date_idx, desc_idx, amount_idx = self.detect_csv_format(csv_path)
        
        if desc_idx is None or amount_idx is None:
            logger.error("Could not detect transaction columns")
            return []
        
        # Parse CSV
        transactions = []
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            headers = next(reader)  # Skip header
            
            for row in reader:
                if not row or not row[amount_idx].strip():
                    continue
                
                txn = {
                    'date': self.parse_date(row[date_idx]) if date_idx else 'Unknown',
                    'description': row[desc_idx].strip() if desc_idx else 'Unknown',
                    'amount': self.parse_amount(row[amount_idx])
                }
                
                if txn['amount'] != 0:
                    transactions.append(txn)
        
        logger.info(f"   ✅ Loaded {len(transactions)} transactions")
        
        # Detect currency
        self.currency = CurrencyDetector.detect_currency(transactions)
        self.transactions = transactions
        
        return transactions
    
    def get_currency_symbol(self):
        """Get currency symbol."""
        return CurrencyDetector.CURRENCY_CODES.get(self.currency, '$')


def main():
    """Test CSV handler."""
    print("\n" + "="*80)
    print("📂 CSV HANDLER - Test")
    print("="*80)
    
    handler = CSVHandler()
    
    # Create test CSV
    test_csv = Path('test_statement.csv')
    
    print("\n📝 Creating test CSV...")
    with open(test_csv, 'w') as f:
        f.write("Date,Description,Amount\n")
        f.write("2024-07-08,Starbucks Coffee,-45.50\n")
        f.write("2024-07-08,Salary Deposit,5000.00\n")
        f.write("2024-07-07,Amazon Purchase,-89.99\n")
        f.write("2024-07-06,Netflix,-15.99\n")
    
    print("✅ Test CSV created: test_statement.csv")
    
    # Load and test
    print("\n🧪 Loading CSV...")
    txns = handler.load_csv(test_csv)
    
    print(f"\n📋 Loaded Transactions:")
    for txn in txns:
        symbol = handler.get_currency_symbol()
        print(f"   {txn['date']} | {txn['description']} | {symbol}{abs(txn['amount']):.2f}")
    
    print(f"\n💱 Currency: {handler.currency}")
    
    # Clean up
    test_csv.unlink()
    print("\n✅ TEST COMPLETE!")
    print("="*80)


if __name__ == "__main__":
    main()
