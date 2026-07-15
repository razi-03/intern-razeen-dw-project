"""
Personal Finance Categorizer - Main Categorization Engine
Uses Google Gemini API to categorize transactions
Author: RAze
Date: 2026-07-08
"""

import google.generativeai as genai
import json
from pathlib import Path
import os
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FinanceCategorizer:
    """Categorize transactions using Gemini API."""
    
    def __init__(self, api_key=None):
        """Initialize with Gemini API key."""
        api_key = api_key or os.getenv('GEMINI_API_KEY')
        
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found. Set it as env variable or pass it.")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        self.learned_categories = self._load_learned_categories()
        logger.info("✅ Gemini API initialized")
    
    def _load_learned_categories(self):
        """Load learned categories from corrections."""
        learn_file = Path('data/learned_categories.json')
        if learn_file.exists():
            with open(learn_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_learned_categories(self):
        """Save learned categories."""
        Path('data').mkdir(exist_ok=True)
        learn_file = Path('data/learned_categories.json')
        with open(learn_file, 'w') as f:
            json.dump(self.learned_categories, f, indent=2)
    
    def _check_learned_category(self, description):
        """Check if we've learned this before."""
        desc_lower = description.lower()
        for learned_desc, category in self.learned_categories.items():
            if learned_desc in desc_lower or description in learned_desc:
                return category
        return None
    
    def categorize_transaction(self, amount, description, date=None):
        """
        Categorize a single transaction.
        
        Args:
            amount: Transaction amount (float)
            description: Transaction description (str)
            date: Transaction date (optional)
        
        Returns:
            dict with category, confidence, reasoning
        """
        # Check if we've learned this before
        learned = self._check_learned_category(description)
        if learned:
            return {
                'description': description,
                'amount': amount,
                'category': learned,
                'confidence': 1.0,
                'source': 'learned',
                'reasoning': f'Learned from previous corrections'
            }
        
        # Use Gemini to categorize
        prompt = f"""Categorize this transaction strictly.

Transaction:
- Amount: {amount}
- Description: {description}
- Date: {date or 'Unknown'}

Common categories: Food, Transportation, Utilities, Entertainment, Shopping, Healthcare, Education, Subscription, Transfer, Other

Respond ONLY with valid JSON:
{{
    "category": "category_name",
    "confidence": 0.0-1.0,
    "reasoning": "brief reason"
}}

Must use one of the common categories above."""
        
        try:
            response = self.model.generate_content(prompt)
            result = json.loads(response.text)
            result['description'] = description
            result['amount'] = amount
            result['source'] = 'gemini'
            return result
        except Exception as e:
            logger.error(f"Categorization error: {e}")
            return {
                'category': 'Other',
                'confidence': 0.0,
                'reasoning': f'Error: {str(e)}',
                'description': description,
                'amount': amount,
                'source': 'error'
            }
    
    def categorize_batch(self, transactions):
        """
        Categorize multiple transactions.
        
        Args:
            transactions: List of dicts with 'amount', 'description', 'date'
        
        Returns:
            List of categorized transactions
        """
        logger.info(f"📊 Categorizing {len(transactions)} transactions...")
        
        categorized = []
        for i, txn in enumerate(transactions, 1):
            if i % max(1, len(transactions) // 5) == 0:
                logger.info(f"   Progress: {i}/{len(transactions)}")
            
            result = self.categorize_transaction(
                amount=txn.get('amount'),
                description=txn.get('description'),
                date=txn.get('date')
            )
            categorized.append(result)
        
        logger.info(f"   ✅ Categorized {len(categorized)} transactions")
        return categorized
    
    def learn_correction(self, description, correct_category):
        """
        Learn from user corrections.
        
        Args:
            description: Transaction description
            correct_category: The correct category user provided
        """
        self.learned_categories[description.lower()] = correct_category
        self._save_learned_categories()
        logger.info(f"✅ Learned: {description} → {correct_category}")
    
    def get_learned_stats(self):
        """Get statistics about learned categories."""
        return {
            'total_learned': len(self.learned_categories),
            'learned_items': self.learned_categories
        }


def main():
    """Test categorizer."""
    print("\n" + "="*80)
    print("💰 PERSONAL FINANCE CATEGORIZER - Engine Test")
    print("="*80)
    
    # Initialize
    try:
        categorizer = FinanceCategorizer()
    except ValueError as e:
        print(f"❌ Error: {e}")
        print("\n⚠️  Set Gemini API key:")
        print("   export GEMINI_API_KEY='your-key'")
        return
    
    # Test transactions
    test_txns = [
        {'amount': 45.50, 'description': 'Starbucks Coffee Shop', 'date': '2024-07-08'},
        {'amount': 12.00, 'description': 'Uber Ride', 'date': '2024-07-08'},
        {'amount': 89.99, 'description': 'Amazon Purchase', 'date': '2024-07-07'},
        {'amount': 150.00, 'description': 'Netflix Subscription', 'date': '2024-07-06'},
    ]
    
    print("\n🧪 Testing with sample transactions...")
    results = categorizer.categorize_batch(test_txns)
    
    print("\n📋 Results:")
    for result in results:
        print(f"\n   {result['description']}")
        print(f"   Amount: ${result['amount']}")
        print(f"   Category: {result['category']} ({result['confidence']:.0%})")
        print(f"   Reasoning: {result['reasoning']}")
    
    print("\n✅ TEST COMPLETE!")
    print("="*80)


if __name__ == "__main__":
    main()
