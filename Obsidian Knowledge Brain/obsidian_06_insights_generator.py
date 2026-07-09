"""
Obsidian AI Brain - Phase 6: AI Insights Generator
Purpose: Generate insights using local LLM
Author: RAze
Date: 2026-07-08
"""

import json
from pathlib import Path
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class InsightsGenerator:
    """Generate insights from notes using AI."""
    
    def __init__(self, model='mistral:7b-instruct-q4_K_M'):
        logger.info(f"🤖 Initializing Ollama with {model}...")
        
        try:
            self.llm = Ollama(
                model=model,
                temperature=0.3,
                top_k=10,
                top_p=0.9
            )
            logger.info(f"   ✅ Ready")
        except Exception as e:
            logger.error(f"   ❌ Error: {e}")
            logger.info("   Make sure: ollama serve is running")
            raise
        
        # Setup prompts
        self.insight_prompt = PromptTemplate(
            input_variables=['notes_summary'],
            template="""You are a knowledge synthesis expert. Analyze these notes:

{notes_summary}

Provide 3 key insights in clear, concise format:
1. Main theme or pattern
2. Unique combination of ideas
3. Actionable takeaway

Be specific and reference the content."""
        )
        
        self.summary_prompt = PromptTemplate(
            input_variables=['content'],
            template="""Summarize this note in 2-3 sentences, highlighting the main idea:

{content}

Summary:"""
        )
    
    def generate_note_summary(self, note):
        """Generate summary for a single note."""
        try:
            # Use modern LCEL: prompt | llm
            chain = self.summary_prompt | self.llm
            summary = chain.invoke({"content": note['content'][:1000]})
            return summary.strip()
        except Exception as e:
            logger.error(f"Error: {e}")
            return "Unable to generate summary"
    
    def generate_vault_insights(self, notes, sample_size=10):
        """Generate insights from vault."""
        logger.info(f"\n💡 GENERATING INSIGHTS")
        logger.info("=" * 80)
        
        # Select sample notes
        import random
        sample = random.sample(notes, min(sample_size, len(notes)))
        
        summary = "\n---\n".join([
            f"{n['title']}: {n['important_concepts']}"
            for n in sample
        ])
        
        try:
            # Use modern LCEL: prompt | llm
            chain = self.insight_prompt | self.llm
            insights = chain.invoke({"notes_summary": summary})
            logger.info(f"   ✅ Generated insights")
            return insights.strip()
        except Exception as e:
            logger.error(f"Error: {e}")
            return "Unable to generate insights"
    
    def analyze_learning_topics(self, notes):
        """Identify learning topics."""
        all_concepts = []
        for note in notes:
            all_concepts.extend(note['important_concepts'])
        
        # Count frequency
        concept_freq = {}
        for concept in all_concepts:
            concept_freq[concept] = concept_freq.get(concept, 0) + 1
        
        # Sort
        sorted_concepts = sorted(
            concept_freq.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return {
            'top_topics': [c[0] for c in sorted_concepts[:10]],
            'topic_frequency': sorted_concepts[:10]
        }


def main():
    """Generate insights."""
    print("\n" + "="*80)
    print("💡 OBSIDIAN AI BRAIN - INSIGHTS GENERATOR")
    print("="*80)
    
    # Load notes with defensive handling
    with open('data/enriched_notes.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Extract notes from any format
    if isinstance(data, list):
        notes = data
    elif isinstance(data, dict):
        if 'notes' in data:
            notes = data['notes']
        else:
            notes = list(data.values()) if data else []
    else:
        notes = []
    
    if not notes:
        print("❌ No notes loaded from enriched_notes.json")
        return
    
    print(f"\n   ✅ Loaded {len(notes)} notes")
    
    # Initialize
    try:
        generator = InsightsGenerator()
    except Exception as e:
        print(f"❌ {e}")
        return
    
    # Generate summaries for first 5 notes
    print(f"\n📝 Generating summaries...")
    for note in notes[:3]:
        print(f"\n   {note['title']}:")
        summary = generator.generate_note_summary(note)
        print(f"   {summary[:150]}...")
    
    # Generate vault insights
    print(f"\n💭 Generating vault insights...")
    vault_insights = generator.generate_vault_insights(notes)
    print(f"\n{vault_insights}")
    
    # Analyze topics
    print(f"\n📊 Learning Topics:")
    topics = generator.analyze_learning_topics(notes)
    for i, (topic, freq) in enumerate(topics['topic_frequency'][:5], 1):
        print(f"   {i}. {topic} (mentioned {freq} times)")
    
    # Save insights
    insights_data = {
        'vault_insights': vault_insights,
        'top_topics': topics['top_topics']
    }
    
    with open('data/insights.json', 'w', encoding='utf-8') as f:
        json.dump(insights_data, f, indent=2)
    
    logger.info(f"✅ Saved insights")
    print("\n✅ INSIGHTS COMPLETE!")
    print("   Next: Run: python obsidian_07_streamlit_ui.py")
    print("="*80)


if __name__ == "__main__":
    main()