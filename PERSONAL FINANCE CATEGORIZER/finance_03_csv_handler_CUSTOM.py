"""
Personal Finance Categorizer - Custom CSV Handler for Bank Statement Format
Handles: date, DrCr, amount, balance, mode, name format
Author: RAze
Date: 2026-07-16
"""

import csv
import pandas as pd
from pathlib import Path
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CustomBankStatementHandler:
    """Handle custom Indian bank statement format."""
    
    def __init__(self):
        self.transactions = []
        self.currency = 'INR'
    
    def load_custom_format(self, csv_path):
        """
        Load transactions from custom format CSV.
        
        Expected columns:
        - date: Transaction date (YYYY-MM-DD)
        - DrCr: Debit (Db) or Credit (Cr)
        - amount: Transaction amount (always positive)
        - balance: Account balance
        - mode: Transaction type (ATM, UPI, NEFT, etc.)
        - name: Recipient/Sender name (optional)
        - Day, Month, Year: Date components
        - Tday: Transaction day number
        
        Returns:
            List of transactions with format: {date, description, amount}
        """
        csv_path = Path(csv_path)
        
        if not csv_path.exists():
            logger.error(f"File not found: {csv_path}")
            return []
        
        logger.info(f"📂 Loading Custom Bank Statement: {csv_path.name}")
        
        try:
            df = pd.read_csv(csv_path)
            logger.info(f"   ✅ Loaded {len(df)} rows from CSV")
            
            transactions = []
            
            for idx, row in df.iterrows():
                try:
                    # Extract data
                    date = str(row.get('date', ''))
                    dr_cr = str(row.get('DrCr', 'Db')).strip()
                    amount = float(row.get('amount', 0))
                    mode = str(row.get('mode', 'OTHER')).strip()
                    name = str(row.get('name', '')).strip() if pd.notna(row.get('name')) else ''
                    
                    # Create description
                    if name and name.upper() != 'NAN':
                        description = f"{mode} - {name}"
                    else:
                        description = mode
                    
                    # Determine sign (negative for debit, positive for credit)
                    if dr_cr == 'Db':
                        signed_amount = -amount
                    else:
                        signed_amount = amount
                    
                    # Format date
                    try:
                        parsed_date = pd.to_datetime(date).strftime('%Y-%m-%d')
                    except:
                        parsed_date = date
                    
                    transaction = {
                        'date': parsed_date,
                        'description': description,
                        'amount': signed_amount
                    }
                    
                    transactions.append(transaction)
                
                except Exception as e:
                    logger.warning(f"   ⚠️  Row {idx}: Error parsing: {e}")
                    continue
            
            logger.info(f"   ✅ Converted {len(transactions)} transactions")
            logger.info(f"   💱 Currency: {self.currency}")
            
            self.transactions = transactions
            return transactions
        
        except Exception as e:
            logger.error(f"Error loading CSV: {e}")
            return []
    
    def get_currency_symbol(self):
        """Get currency symbol for display."""
        symbols = {
            'INR': '₹',
            'USD': '$',
            'EUR': '€',
            'GBP': '£'
        }
        return symbols.get(self.currency, '₹')


def main():
    """Test the custom handler."""
    print("\n" + "="*80)
    print("📂 CUSTOM BANK STATEMENT HANDLER - Test")
    print("="*80)
    
    handler = CustomBankStatementHandler()
    
    # Create test CSV with your format
    test_csv = Path('test_bank_statement.csv')
    
    print("\n📝 Creating test CSV...")
    with open(test_csv, 'w') as f:
        f.write("date,DrCr,amount,balance,mode,name,Day,Month,Year,Tday\n")
        f.write("2022-01-01,Db,10000.0,473292.87,ATM,,01,01,2022,1\n")
        f.write("2022-01-02,Db,930.0,462362.87,UPI,AYUBRAJE,02,01,2022,2\n")
        f.write("2022-01-07,Db,2000.0,460362.87,UPI,ABUTALAH,07,01,2022,3\n")
        f.write("2022-01-10,Cr,5000.0,465362.87,NEFT,,10,01,2022,4\n")
    
    print("✅ Test CSV created")
    
    # Load
    print("\n🧪 Loading with custom handler...")
    txns = handler.load_custom_format(test_csv)
    
    # Display
    print(f"\n📋 Loaded Transactions:")
    symbol = handler.get_currency_symbol()
    for txn in txns:
        print(f"   {txn['date']} | {txn['description']:20} | {symbol}{txn['amount']:10.2f}")
    
    print("\n✅ TEST COMPLETE!")
    print("="*80)
    
    # Cleanup
    test_csv.unlink()


if __name__ == "__main__":
    main()
