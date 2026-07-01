"""
Phase 1: Generate Synthetic Support Ticket Dataset
Purpose: Create realistic support tickets for classifier training/demo
Author: RAze
Date: 2026-07-01
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

class SyntheticTicketGenerator:
    """Generate realistic support tickets for POC testing."""
    
    def __init__(self, num_tickets=500):
        self.num_tickets = num_tickets
        
        # Define ticket taxonomy
        self.categories = ['Bug', 'Feature Request', 'Billing', 'Technical Support', 'Account', 'Other']
        self.priorities = ['Low', 'Medium', 'High', 'Critical']
        self.sentiments = ['Positive', 'Neutral', 'Negative']
        
        # Sample ticket templates by category
        self.templates = {
            'Bug': [
                "Cannot login to my account. Getting 500 error on login page.",
                "Dashboard widgets not loading. Tried refreshing, still broken.",
                "Export to CSV feature crashes when I select more than 1000 rows.",
                "Mobile app freezes when uploading files larger than 50MB.",
                "Search function returns no results even though records exist."
            ],
            'Feature Request': [
                "Can we add dark mode to the platform?",
                "Would love to see integration with Slack for notifications.",
                "Please add bulk edit functionality for records.",
                "We need API access for custom integrations.",
                "Can you implement two-factor authentication?"
            ],
            'Billing': [
                "Why was I charged twice this month?",
                "I need an invoice for my payment on July 1st.",
                "Can I upgrade to the enterprise plan?",
                "Do you offer annual subscription discounts?",
                "I was charged but didn't confirm the transaction."
            ],
            'Technical Support': [
                "How do I connect my database to the platform?",
                "What's the maximum file size I can upload?",
                "How do I reset my API key?",
                "Can you help me configure LDAP authentication?",
                "How do I backup my data?"
            ],
            'Account': [
                "How do I change my email address?",
                "I forgot my password, please reset it.",
                "Can you update my billing address?",
                "How do I delete my account?",
                "I need to add team members to my workspace."
            ],
            'Other': [
                "Just wanted to say thanks for great support!",
                "Your platform has transformed our workflow.",
                "Question about your roadmap priorities.",
                "Is there a community forum?",
                "Can you recommend best practices for scaling?"
            ]
        }
    
    def generate_ticket(self, ticket_id):
        """Generate a single realistic ticket."""
        category = random.choice(self.categories)
        
        # Correlate priority with category
        if category == 'Bug':
            priority = random.choices(
                self.priorities, 
                weights=[0.1, 0.3, 0.4, 0.2]  # Bugs tend to be higher priority
            )[0]
        elif category == 'Billing':
            priority = random.choices(
                self.priorities,
                weights=[0.2, 0.5, 0.2, 0.1]
            )[0]
        else:
            priority = random.choices(
                self.priorities,
                weights=[0.4, 0.35, 0.15, 0.1]
            )[0]
        
        # Correlate sentiment with priority
        if priority == 'Critical':
            sentiment = random.choices(
                self.sentiments,
                weights=[0.05, 0.15, 0.8]
            )[0]
        elif priority == 'High':
            sentiment = random.choices(
                self.sentiments,
                weights=[0.1, 0.3, 0.6]
            )[0]
        else:
            sentiment = random.choices(
                self.sentiments,
                weights=[0.3, 0.5, 0.2]
            )[0]
        
        # Get ticket text from template
        description = random.choice(self.templates[category])
        
        # Add some variation
        if random.random() > 0.7:
            description += " " + random.choice([
                "This is urgent!",
                "Thanks in advance.",
                "Been waiting 3 days.",
                "Please help ASAP.",
                "Losing money on this."
            ])
        
        # Generate timestamp (last 30 days)
        days_ago = random.randint(0, 30)
        hours_ago = random.randint(0, 23)
        created_at = datetime.now() - timedelta(days=days_ago, hours=hours_ago)
        
        return {
            'ticket_id': ticket_id,
            'created_at': created_at.isoformat(),
            'description': description,
            'true_category': category,
            'true_priority': priority,
            'true_sentiment': sentiment,
            'customer_name': f"Customer_{random.randint(1000, 9999)}",
            'ticket_length': len(description.split())
        }
    
    def generate_dataset(self):
        """Generate full dataset."""
        print(f"🔄 Generating {self.num_tickets} synthetic tickets...")
        tickets = [self.generate_ticket(i) for i in range(1, self.num_tickets + 1)]
        
        df = pd.DataFrame(tickets)
        return df

if __name__ == "__main__":
    # Generate dataset
    generator = SyntheticTicketGenerator(num_tickets=500)
    df = generator.generate_dataset()
    
    # Save to CSV
    df.to_csv('data_raw_tickets.csv', index=False)
    print(f"✅ Saved {len(df)} tickets to data_raw_tickets.csv")
    
    # Print sample
    print("\n📊 Sample Tickets:")
    print(df.head(10))
    
    # Print summary statistics
    print("\n📈 Dataset Summary:")
    print(f"Total tickets: {len(df)}")
    print(f"\nCategory distribution:")
    print(df['true_category'].value_counts())
    print(f"\nPriority distribution:")
    print(df['true_priority'].value_counts())
    print(f"\nSentiment distribution:")
    print(df['true_sentiment'].value_counts())
    print(f"\nAverage ticket length: {df['ticket_length'].mean():.0f} words")
