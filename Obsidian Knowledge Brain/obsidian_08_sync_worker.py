"""
Obsidian AI Brain - Phase 8: Vault Sync Worker
Purpose: Keep vector store in sync with Obsidian vault
Author: RAze
Date: 2026-07-08
"""

import json
from pathlib import Path
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import logging
from datetime import datetime
import hashlib

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VaultSyncWorker:
    """Keep vault and vector store in sync."""
    
    def __init__(self):
        self.vault_path = Path('obsidian_vault')
        self.hash_file = Path('data/.vault_hashes.json')
        self.vault_hashes = self._load_hashes()
        
        # Load vector store
        settings = Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory='vector_store',
            anonymized_telemetry=False
        )
        self.client = chromadb.Client(settings)
        self.collection = self.client.get_collection('obsidian_notes')
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
    
    def _load_hashes(self):
        """Load file hashes."""
        if self.hash_file.exists():
            with open(self.hash_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_hashes(self):
        """Save file hashes."""
        with open(self.hash_file, 'w') as f:
            json.dump(self.vault_hashes, f)
    
    def _get_file_hash(self, file_path):
        """Get hash of file."""
        with open(file_path, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    
    def detect_changes(self):
        """Detect changed, new, and deleted notes."""
        md_files = list(self.vault_path.rglob('*.md'))
        
        current_files = {f.name: f for f in md_files}
        current_hashes = {}
        
        changed = []
        new = []
        
        for file_path in md_files:
            file_hash = self._get_file_hash(file_path)
            current_hashes[file_path.name] = file_hash
            
            if file_path.name not in self.vault_hashes:
                new.append(file_path)
            elif self.vault_hashes[file_path.name] != file_hash:
                changed.append(file_path)
        
        deleted = [f for f in self.vault_hashes.keys() if f not in current_hashes]
        
        self.vault_hashes = current_hashes
        self._save_hashes()
        
        return changed, new, deleted
    
    def sync(self):
        """Sync vault with vector store."""
        logger.info(f"\n🔄 SYNCING VAULT")
        logger.info("=" * 80)
        
        changed, new, deleted = self.detect_changes()
        
        logger.info(f"   Changes detected: {len(changed)} modified, {len(new)} new, {len(deleted)} deleted")
        
        # Handle deleted
        for deleted_file in deleted:
            note_id = Path(deleted_file).stem
            try:
                self.collection.delete(ids=[note_id])
                logger.info(f"   ✅ Deleted: {deleted_file}")
            except:
                pass
        
        # Handle changed and new
        for file_path in changed + new:
            note_id = file_path.stem
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                embedding = self.embedder.encode(content[:2000]).tolist()
                
                # Upsert
                self.collection.upsert(
                    ids=[note_id],
                    documents=[content],
                    embeddings=[embedding],
                    metadatas=[{
                        'title': file_path.stem,
                        'modified': datetime.now().isoformat()
                    }]
                )
                
                status = "Updated" if file_path in changed else "Added"
                logger.info(f"   ✅ {status}: {file_path.name}")
            
            except Exception as e:
                logger.error(f"   ❌ Error: {file_path.name} - {e}")
        
        # Persist
        self.client.persist()
        
        logger.info(f"   ✅ Sync complete")
        return len(changed) + len(new) + len(deleted)


def main():
    """Run sync."""
    print("\n" + "="*80)
    print("🔄 OBSIDIAN AI BRAIN - VAULT SYNC")
    print("="*80)
    
    try:
        worker = VaultSyncWorker()
        changes = worker.sync()
        
        print(f"\n✅ SYNC COMPLETE!")
        print(f"   Total changes: {changes}")
        print("="*80)
    
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
