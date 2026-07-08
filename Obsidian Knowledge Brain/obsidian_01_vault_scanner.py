"""
Obsidian AI Brain - Phase 1: Vault Scanner
Purpose: Scan Obsidian vault and discover all notes
Author: RAze
Date: 2026-07-08
Runtime: ~5 seconds per 1000 notes
"""

import os
import json
from pathlib import Path
from datetime import datetime
import logging
from typing import List, Dict
import yaml

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class VaultScanner:
    """Scan Obsidian vault and discover notes."""
    
    def __init__(self, vault_path='obsidian_vault'):
        self.vault_path = Path(vault_path)
        self.notes = []
        self.vault_structure = {}
        self.metadata = {
            'total_notes': 0,
            'total_files': 0,
            'total_directories': 0,
            'scan_date': datetime.now().isoformat()
        }
        
        if not self.vault_path.exists():
            logger.warning(f"Vault path not found: {self.vault_path}")
            logger.info("Creating sample vault structure...")
            self.vault_path.mkdir(parents=True, exist_ok=True)
    
    def find_markdown_files(self) -> List[Path]:
        """Find all markdown files in vault."""
        logger.info(f"🔍 Scanning vault: {self.vault_path}")
        
        md_files = list(self.vault_path.rglob('*.md'))
        
        # Exclude common directories
        exclude_dirs = {'.obsidian', '.git', 'node_modules', '__pycache__'}
        md_files = [f for f in md_files if not any(
            part in f.parts for part in exclude_dirs
        )]
        
        logger.info(f"   ✅ Found {len(md_files)} markdown files")
        return sorted(md_files)
    
    def extract_file_metadata(self, file_path: Path) -> Dict:
        """Extract metadata from a note file."""
        try:
            stat = file_path.stat()
            
            relative_path = file_path.relative_to(self.vault_path)
            folder = str(relative_path.parent)
            
            metadata = {
                'file_name': file_path.name,
                'file_path': str(relative_path),
                'folder': folder if folder != '.' else 'root',
                'size_bytes': stat.st_size,
                'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                'modified': datetime.fromtimestamp(stat.st_mtime).isoformat()
            }
            
            return metadata
        except Exception as e:
            logger.error(f"Error extracting metadata from {file_path}: {e}")
            return {}
    
    def extract_frontmatter(self, content: str) -> Dict:
        """Extract YAML frontmatter from note."""
        try:
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    yaml_content = parts[1]
                    frontmatter = yaml.safe_load(yaml_content) or {}
                    body_start = len(parts[0]) + len(parts[1]) + 4  # Account for --- markers
                    return frontmatter, body_start
            return {}, 0
        except Exception as e:
            logger.warning(f"Error parsing frontmatter: {e}")
            return {}, 0
    
    def extract_links(self, content: str) -> List[str]:
        """Extract wiki-style links from note content."""
        import re
        
        # Match [[note]] and [[note|alias]] patterns
        link_pattern = r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]'
        links = re.findall(link_pattern, content)
        
        return [link.strip() for link in links]
    
    def extract_tags(self, content: str) -> List[str]:
        """Extract hashtags from note content."""
        import re
        
        # Match #tag pattern (must be preceded by space or start of line)
        tag_pattern = r'(?:^|\s)#([a-zA-Z0-9_-]+)'
        tags = re.findall(tag_pattern, content, re.MULTILINE)
        
        return list(set(tags))  # Remove duplicates
    
    def scan_note(self, file_path: Path) -> Dict:
        """Scan a single note and extract information."""
        try:
            # Read file
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract metadata
            file_metadata = self.extract_file_metadata(file_path)
            
            # Extract frontmatter
            frontmatter, body_start = self.extract_frontmatter(content)
            body = content[body_start:].strip()
            
            # Extract links and tags
            links = self.extract_links(content)
            tags = self.extract_tags(content)
            
            # Count words
            word_count = len(body.split())
            
            # Create note record
            note = {
                'id': file_path.stem,  # Note name without extension
                'title': frontmatter.get('title', file_path.stem),
                'file_metadata': file_metadata,
                'frontmatter': frontmatter,
                'content_preview': body[:200] + '...' if len(body) > 200 else body,
                'word_count': word_count,
                'links': links,
                'tags': tags,
                'linked_count': len(links),
                'tag_count': len(tags),
                'scanned_at': datetime.now().isoformat()
            }
            
            return note
        
        except Exception as e:
            logger.error(f"Error scanning {file_path}: {e}")
            return None
    
    def scan_vault(self) -> List[Dict]:
        """Scan entire vault."""
        logger.info(f"\n📚 SCANNING OBSIDIAN VAULT")
        logger.info("=" * 80)
        
        md_files = self.find_markdown_files()
        
        if not md_files:
            logger.warning("No markdown files found in vault")
            return []
        
        # Scan each file
        print(f"\n   Scanning {len(md_files)} notes...")
        for i, file_path in enumerate(md_files, 1):
            if i % max(1, len(md_files) // 10) == 0:
                logger.info(f"   Progress: {i}/{len(md_files)}")
            
            note = self.scan_note(file_path)
            if note:
                self.notes.append(note)
        
        # Update metadata
        self.metadata['total_notes'] = len(self.notes)
        
        logger.info(f"   ✅ Scanned {len(self.notes)} notes successfully")
        
        return self.notes
    
    def build_folder_structure(self):
        """Build vault folder structure."""
        logger.info("\n📁 Building folder structure...")
        
        structure = {}
        
        for note in self.notes:
            folder = note['file_metadata']['folder']
            
            if folder not in structure:
                structure[folder] = {
                    'notes': [],
                    'note_count': 0
                }
            
            structure[folder]['notes'].append(note['id'])
            structure[folder]['note_count'] += 1
        
        self.vault_structure = structure
        
        # Print structure
        for folder in sorted(structure.keys()):
            count = structure[folder]['note_count']
            logger.info(f"   📂 {folder}: {count} notes")
    
    def print_summary(self):
        """Print vault summary."""
        print("\n" + "=" * 80)
        print("📊 VAULT SCAN SUMMARY")
        print("=" * 80)
        
        if not self.notes:
            print("\n   ⚠️  No notes found in vault")
            return
        
        # Basic stats
        print(f"\n📈 Statistics:")
        print(f"   Total notes: {len(self.notes)}")
        print(f"   Total folders: {len(self.vault_structure)}")
        
        # Word count
        total_words = sum(n['word_count'] for n in self.notes)
        avg_words = total_words // len(self.notes) if self.notes else 0
        print(f"   Total words: {total_words:,}")
        print(f"   Average words per note: {avg_words}")
        
        # Links and tags
        total_links = sum(n['linked_count'] for n in self.notes)
        total_tags = sum(n['tag_count'] for n in self.notes)
        print(f"   Total links: {total_links}")
        print(f"   Total tags: {total_tags}")
        
        # Top notes
        print(f"\n📝 Top 5 notes by word count:")
        sorted_notes = sorted(self.notes, key=lambda x: x['word_count'], reverse=True)
        for i, note in enumerate(sorted_notes[:5], 1):
            print(f"   {i}. {note['title']} ({note['word_count']} words)")
        
        # Folder distribution
        print(f"\n📂 Folder distribution:")
        sorted_folders = sorted(
            self.vault_structure.items(),
            key=lambda x: x[1]['note_count'],
            reverse=True
        )
        for folder, data in sorted_folders[:5]:
            print(f"   • {folder}: {data['note_count']} notes")
        
        print("\n" + "=" * 80)
    
    def save_scan_results(self, output_path='data/vault_scan.json'):
        """Save scan results to file."""
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        data = {
            'metadata': self.metadata,
            'notes': self.notes,
            'vault_structure': self.vault_structure
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ Saved scan results to {output_file}")
        return output_file


def main():
    """Run vault scanner."""
    print("\n" + "=" * 80)
    print("🧠 OBSIDIAN AI BRAIN - VAULT SCANNER")
    print("=" * 80)
    
    # Initialize scanner
    scanner = VaultScanner(vault_path='obsidian_vault')
    
    # Scan vault
    notes = scanner.scan_vault()
    
    if not notes:
        print("\n⚠️  No notes found. Please:")
        print("   1. Create 'obsidian_vault' folder")
        print("   2. Add some markdown (.md) files")
        print("   3. Run this script again")
        return
    
    # Build structure
    scanner.build_folder_structure()
    
    # Print summary
    scanner.print_summary()
    
    # Save results
    scanner.save_scan_results()
    
    print(f"\n✅ VAULT SCAN COMPLETE!")
    print(f"   Next: Run: python obsidian_02_note_parser.py")
    print("=" * 80)


if __name__ == "__main__":
    main()
