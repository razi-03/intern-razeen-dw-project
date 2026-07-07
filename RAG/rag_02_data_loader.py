"""
RAG Project - Phase 2: PDF Data Loader
Purpose: Load and process research papers (PDFs)
Author: RAze
Date: 2026-07-07
Runtime: ~30 seconds per paper
"""

import os
import json
from pathlib import Path
import PyPDF2
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class PDFProcessor:
    """Extract text and metadata from PDF files."""
    
    def __init__(self, papers_directory='data/papers'):
        self.papers_dir = Path(papers_directory)
        self.papers_dir.mkdir(parents=True, exist_ok=True)
        self.documents = []
        self.metadata = {}
    
    def extract_text_from_pdf(self, pdf_path):
        """Extract text from PDF file."""
        logger.info(f"📖 Processing: {pdf_path.name}")
        
        text_content = ""
        page_count = 0
        
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                page_count = len(reader.pages)
                
                # Extract text from each page
                for page_num, page in enumerate(reader.pages, 1):
                    page_text = page.extract_text()
                    if page_text:
                        # Add page number for reference
                        text_content += f"\n[Page {page_num}]\n{page_text}\n"
                
                # Try to extract metadata
                metadata = {
                    'title': reader.metadata.title if reader.metadata else pdf_path.stem,
                    'author': reader.metadata.author if reader.metadata else 'Unknown',
                    'pages': page_count,
                    'creation_date': str(reader.metadata.creation_date) if reader.metadata else 'Unknown'
                }
            
            logger.info(f"   ✅ Extracted {page_count} pages")
            return text_content, metadata
        
        except Exception as e:
            logger.error(f"   ❌ Error processing {pdf_path.name}: {e}")
            return None, None
    
    def clean_text(self, text):
        """Clean extracted text."""
        # Remove excessive whitespace
        text = ' '.join(text.split())
        # Remove special characters that might interfere
        text = text.replace('\x00', '')
        return text
    
    def load_all_pdfs(self):
        """Load all PDFs from directory."""
        print("\n" + "="*80)
        print("📚 LOADING RESEARCH PAPERS")
        print("="*80)
        
        pdf_files = list(self.papers_dir.glob('*.pdf'))
        
        if not pdf_files:
            print(f"\n   ⚠️  No PDFs found in {self.papers_dir}/")
            print("   📝 Add PDFs to load research papers")
            return []
        
        print(f"\n   Found {len(pdf_files)} PDF(s)\n")
        
        for pdf_path in pdf_files:
            text, metadata = self.extract_text_from_pdf(pdf_path)
            
            if text:
                text = self.clean_text(text)
                
                document = {
                    'source': pdf_path.name,
                    'content': text,
                    'metadata': metadata,
                    'loaded_at': datetime.now().isoformat()
                }
                
                self.documents.append(document)
                self.metadata[pdf_path.stem] = metadata
                
                # Stats
                word_count = len(text.split())
                print(f"   ✅ {pdf_path.name}")
                print(f"      Words: {word_count:,}")
                print(f"      Pages: {metadata['pages']}")
        
        return self.documents
    
    def chunk_documents(self, chunk_size=500, overlap=100):
        """Split documents into chunks for embedding."""
        logger.info(f"\n✂️  Chunking documents (size={chunk_size}, overlap={overlap})")
        
        chunks = []
        
        for doc in self.documents:
            text = doc['content']
            words = text.split()
            
            # Create overlapping chunks
            for i in range(0, len(words), chunk_size - overlap):
                chunk_words = words[i:i + chunk_size]
                chunk_text = ' '.join(chunk_words)
                
                if len(chunk_text.strip()) > 50:  # Only keep substantial chunks
                    chunks.append({
                        'text': chunk_text,
                        'source': doc['source'],
                        'metadata': doc['metadata'],
                        'chunk_index': len([c for c in chunks if c['source'] == doc['source']])
                    })
            
            logger.info(f"   {doc['source']}: {len(chunks)} chunks created")
        
        print(f"\n   ✅ Total chunks created: {len(chunks)}")
        return chunks
    
    def save_metadata(self, output_path='data/metadata/papers_metadata.json'):
        """Save extracted metadata."""
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w') as f:
            json.dump(self.metadata, f, indent=2)
        
        logger.info(f"   ✅ Metadata saved to {output_file}")
        return output_file
    
    def get_documents_summary(self):
        """Print summary of loaded documents."""
        print("\n" + "="*80)
        print("📊 DOCUMENTS SUMMARY")
        print("="*80)
        
        total_words = sum(len(doc['content'].split()) for doc in self.documents)
        
        print(f"\n   📁 Papers loaded: {len(self.documents)}")
        print(f"   📝 Total words: {total_words:,}")
        
        for doc in self.documents:
            words = len(doc['content'].split())
            print(f"\n   📄 {doc['metadata']['title']}")
            print(f"      Source: {doc['source']}")
            print(f"      Pages: {doc['metadata']['pages']}")
            print(f"      Words: {words:,}")


class DataValidator:
    """Validate loaded data."""
    
    @staticmethod
    def validate_documents(documents):
        """Check if documents are valid."""
        logger.info("\n🔍 Validating documents...")
        
        issues = []
        
        for doc in documents:
            if not doc.get('content') or len(doc['content'].strip()) < 100:
                issues.append(f"   ⚠️  {doc['source']}: Too short")
            
            if not doc.get('metadata'):
                issues.append(f"   ⚠️  {doc['source']}: Missing metadata")
        
        if issues:
            print("   ⚠️  Issues found:")
            for issue in issues:
                print(issue)
        else:
            print("   ✅ All documents valid!")
        
        return len(issues) == 0


def main():
    """Load and prepare PDF data."""
    print("\n" + "="*80)
    print("📚 RESEARCH PAPER DATA LOADER")
    print("="*80)
    
    # Load PDFs
    processor = PDFProcessor()
    documents = processor.load_all_pdfs()
    
    if not documents:
        print("\n⚠️  No documents loaded. Add PDFs to data/papers/ and try again.")
        return
    
    # Get summary
    processor.get_documents_summary()
    
    # Validate
    validator = DataValidator()
    validator.validate_documents(documents)
    
    # Chunk documents
    chunks = processor.chunk_documents(chunk_size=500, overlap=100)
    
    # Save metadata
    processor.save_metadata()
    
    # Save chunks for next phase
    print("\n💾 Saving chunks for embedding...")
    chunks_file = Path('data/metadata/chunks.json')
    chunks_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(chunks_file, 'w') as f:
        json.dump(chunks, f, indent=2)
    
    print(f"   ✅ Saved {len(chunks)} chunks to {chunks_file}")
    
    # Summary
    print("\n" + "="*80)
    print("✅ DATA LOADING COMPLETE!")
    print("="*80)
    print(f"""
✅ Loaded:
   • {len(documents)} research papers
   • {len(chunks)} text chunks
   • Metadata extracted and validated

📁 Output files:
   • data/metadata/chunks.json (for embedding)
   • data/metadata/papers_metadata.json (metadata)

🔄 Next step:
   Run: python rag_03_vector_database.py
""")
    print("="*80)


if __name__ == "__main__":
    main()
