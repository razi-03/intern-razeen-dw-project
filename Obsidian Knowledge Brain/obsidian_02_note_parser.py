"""
Obsidian AI Brain - Phase 2: Note Parser
Purpose: Parse note content and extract rich information
Author: RAze
Date: 2026-07-08
Runtime: ~30 seconds per 1000 notes
"""

import json
from pathlib import Path
from datetime import datetime
import logging
from typing import List, Dict
import re

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class NoteParser:
    """Parse and enrich note content."""
    
    def __init__(self, scan_file='data/vault_scan.json'):
        self.scan_file = Path(scan_file)
        self.vault_path = Path('obsidian_vault')
        self.notes = []
        self.enriched_notes = []
        
        # Load scan results
        self._load_scan_results()
    
    def _load_scan_results(self):
        """Load vault scan results."""
        if not self.scan_file.exists():
            logger.error(f"Scan file not found: {self.scan_file}")
            logger.info("Run obsidian_01_vault_scanner.py first")
            return
        
        with open(self.scan_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.notes = data.get('notes', [])
        logger.info(f"✅ Loaded {len(self.notes)} notes from scan")
    
    def read_note_content(self, note: Dict) -> str:
        """Read full content of a note."""
        try:
            file_path = self.vault_path / note['file_metadata']['file_path']
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return content
        except Exception as e:
            logger.error(f"Error reading {note['id']}: {e}")
            return ""
    
    def extract_headers(self, content: str) -> Dict:
        """Extract header structure from note."""
        headers = {
            'h1': [],
            'h2': [],
            'h3': [],
            'all': []
        }
        
        lines = content.split('\n')
        for line in lines:
            if line.startswith('# ') and not line.startswith('# '):
                h1 = line.replace('# ', '').strip()
                headers['h1'].append(h1)
                headers['all'].append(('h1', h1))
            elif line.startswith('## '):
                h2 = line.replace('## ', '').strip()
                headers['h2'].append(h2)
                headers['all'].append(('h2', h2))
            elif line.startswith('### '):
                h3 = line.replace('### ', '').strip()
                headers['h3'].append(h3)
                headers['all'].append(('h3', h3))
        
        return headers
    
    def extract_code_blocks(self, content: str) -> List[Dict]:
        """Extract code blocks from note."""
        code_blocks = []
        
        # Match ```language\ncode```
        pattern = r'```(\w*)\n(.*?)```'
        matches = re.finditer(pattern, content, re.DOTALL)
        
        for match in matches:
            language = match.group(1) or 'plain'
            code = match.group(2).strip()
            
            code_blocks.append({
                'language': language,
                'code': code,
                'lines': len(code.split('\n'))
            })
        
        return code_blocks
    
    def extract_quotes(self, content: str) -> List[str]:
        """Extract blockquotes from note."""
        quotes = []
        
        lines = content.split('\n')
        for line in lines:
            if line.startswith('> '):
                quote = line.replace('> ', '').strip()
                if quote:
                    quotes.append(quote)
        
        return quotes
    
    def extract_lists(self, content: str) -> Dict:
        """Extract lists from note."""
        lists = {
            'unordered': [],
            'ordered': [],
            'checkbox': []
        }
        
        lines = content.split('\n')
        for line in lines:
            stripped = line.strip()
            
            # Unordered lists
            if stripped.startswith('- ') or stripped.startswith('* '):
                lists['unordered'].append(stripped[2:].strip())
            
            # Ordered lists
            elif re.match(r'^\d+\. ', stripped):
                lists['ordered'].append(re.sub(r'^\d+\. ', '', stripped).strip())
            
            # Checkboxes
            elif re.match(r'^- \[[ xX]\]', stripped):
                lists['checkbox'].append(stripped)
        
        return lists
    
    def extract_bold_text(self, content: str) -> List[str]:
        """Extract bold text (likely important concepts)."""
        bold_pattern = r'\*\*([^*]+)\*\*'
        bold_text = re.findall(bold_pattern, content)
        
        return [text.strip() for text in bold_text if text.strip()]
    
    def calculate_readability(self, content: str) -> Dict:
        """Calculate readability metrics."""
        lines = content.split('\n')
        
        # Remove empty lines
        non_empty_lines = [l for l in lines if l.strip()]
        
        words = content.split()
        sentences = re.split(r'[.!?]+', content)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        metrics = {
            'total_lines': len(lines),
            'non_empty_lines': len(non_empty_lines),
            'total_words': len(words),
            'total_sentences': len(sentences),
            'avg_words_per_line': len(words) / max(len(non_empty_lines), 1),
            'avg_words_per_sentence': len(words) / max(len(sentences), 1)
        }
        
        return metrics
    
    def parse_note(self, note: Dict) -> Dict:
        """Fully parse a single note."""
        try:
            # Read full content
            content = self.read_note_content(note)
            
            if not content:
                return None
            
            # Extract components
            headers = self.extract_headers(content)
            code_blocks = self.extract_code_blocks(content)
            quotes = self.extract_quotes(content)
            lists = self.extract_lists(content)
            bold_text = self.extract_bold_text(content)
            readability = self.calculate_readability(content)
            
            # Create enriched note
            enriched = {
                'id': note['id'],
                'title': note['title'],
                'file_metadata': note['file_metadata'],
                'frontmatter': note['frontmatter'],
                'content': content,
                'content_length': len(content),
                'headers': headers,
                'code_blocks': code_blocks,
                'code_block_count': len(code_blocks),
                'quotes': quotes,
                'quote_count': len(quotes),
                'lists': lists,
                'bold_text': bold_text,
                'important_concepts': bold_text[:10],  # Top 10 bold texts
                'links': note['links'],
                'tags': note['tags'],
                'readability': readability,
                'parsed_at': datetime.now().isoformat()
            }
            
            return enriched
        
        except Exception as e:
            logger.error(f"Error parsing {note['id']}: {e}")
            return None
    
    def parse_all_notes(self) -> List[Dict]:
        """Parse all notes."""
        logger.info(f"\n📖 PARSING {len(self.notes)} NOTES")
        logger.info("=" * 80)
        
        self.enriched_notes = []
        
        for i, note in enumerate(self.notes, 1):
            if i % max(1, len(self.notes) // 10) == 0:
                logger.info(f"   Progress: {i}/{len(self.notes)}")
            
            enriched = self.parse_note(note)
            if enriched:
                self.enriched_notes.append(enriched)
        
        logger.info(f"   ✅ Successfully parsed {len(self.enriched_notes)} notes")
        
        return self.enriched_notes
    
    def print_summary(self):
        """Print parsing summary."""
        print("\n" + "=" * 80)
        print("📊 PARSING SUMMARY")
        print("=" * 80)
        
        if not self.enriched_notes:
            print("⚠️  No notes parsed")
            return
        
        # Content statistics
        total_content = sum(n['content_length'] for n in self.enriched_notes)
        avg_content = total_content // len(self.enriched_notes)
        
        print(f"\n📝 Content Stats:")
        print(f"   Total characters: {total_content:,}")
        print(f"   Average per note: {avg_content:,}")
        
        # Headers
        total_headers = sum(
            len(n['headers']['h1']) + len(n['headers']['h2']) + len(n['headers']['h3'])
            for n in self.enriched_notes
        )
        print(f"   Total headers: {total_headers}")
        
        # Code blocks
        total_code = sum(n['code_block_count'] for n in self.enriched_notes)
        print(f"   Code blocks: {total_code}")
        
        # Quotes
        total_quotes = sum(n['quote_count'] for n in self.enriched_notes)
        print(f"   Quotes: {total_quotes}")
        
        # Important concepts
        all_concepts = []
        for note in self.enriched_notes:
            all_concepts.extend(note['important_concepts'])
        
        print(f"\n🎯 Top 10 Important Concepts:")
        concept_freq = {}
        for concept in all_concepts:
            concept_freq[concept] = concept_freq.get(concept, 0) + 1
        
        sorted_concepts = sorted(concept_freq.items(), key=lambda x: x[1], reverse=True)
        for i, (concept, freq) in enumerate(sorted_concepts[:10], 1):
            print(f"   {i}. {concept} (mentioned {freq} times)")
        
        # Readability
        avg_readability = {
            'avg_words_per_sentence': sum(
                n['readability']['avg_words_per_sentence']
                for n in self.enriched_notes
            ) / len(self.enriched_notes)
        }
        
        print(f"\n📖 Readability:")
        print(f"   Avg words per sentence: {avg_readability['avg_words_per_sentence']:.1f}")
        
        print("\n" + "=" * 80)
    
    def save_enriched_notes(self, output_path='data/enriched_notes.json'):
        """Save enriched notes."""
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        data = {
            'metadata': {
                'total_notes': len(self.enriched_notes),
                'parsed_at': datetime.now().isoformat()
            },
            'notes': self.enriched_notes
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ Saved enriched notes to {output_file}")
        return output_file


def main():
    """Run note parser."""
    print("\n" + "=" * 80)
    print("🧠 OBSIDIAN AI BRAIN - NOTE PARSER")
    print("=" * 80)
    
    parser = NoteParser()
    
    if not parser.notes:
        print("⚠️  No notes loaded. Run obsidian_01_vault_scanner.py first")
        return
    
    # Parse notes
    enriched = parser.parse_all_notes()
    
    if not enriched:
        print("⚠️  No notes parsed successfully")
        return
    
    # Print summary
    parser.print_summary()
    
    # Save results
    parser.save_enriched_notes()
    
    print(f"\n✅ PARSING COMPLETE!")
    print(f"   Next: Run: python obsidian_03_embedding_generator.py")
    print("=" * 80)


if __name__ == "__main__":
    main()
