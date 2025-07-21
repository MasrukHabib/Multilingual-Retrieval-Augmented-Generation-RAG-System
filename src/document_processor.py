import PyPDF2
import re
from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DocumentProcessor:
    def __init__(self):
        self.text_content = ""
        
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Extract text from PDF using PyPDF2
        """
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text() + "\n"
                
                self.text_content = text
                logger.info(f"Extracted {len(text)} characters from PDF")
                return text
                
        except Exception as e:
            logger.error(f"Error extracting PDF: {str(e)}")
            return ""
    
    def clean_text(self, text: str) -> str:
        """
        Clean and preprocess Bengali and English text
        """
        # Remove extra whitespaces
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep Bengali characters
        # Bengali Unicode range: \u0980-\u09FF
        text = re.sub(r'[^\w\s\u0980-\u09FF।,;:!?.\-]', '', text)
        
        # Fix common OCR issues
        text = text.replace('।।', '।')  # Fix double danda
        text = text.replace('  ', ' ')   # Fix double spaces
        
        return text.strip()
    
    def chunk_text(self, text: str, chunk_size: int = 500, overlap: int = 50) -> List[Dict]:
        """
        Split text into chunks with overlap for better context preservation
        """
        # Clean text first
        clean_text = self.clean_text(text)
        
        # Split by sentences (both English and Bengali)
        sentences = re.split(r'[।.!?]+', clean_text)
        
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
                
            # If adding this sentence exceeds chunk size, save current chunk
            if len(current_chunk) + len(sentence) > chunk_size and current_chunk:
                chunks.append({
                    'content': current_chunk.strip(),
                    'length': len(current_chunk),
                    'id': len(chunks)
                })
                
                # Start new chunk with overlap
                words = current_chunk.split()
                overlap_text = ' '.join(words[-overlap:]) if len(words) > overlap else current_chunk
                current_chunk = overlap_text + " " + sentence
            else:
                current_chunk += " " + sentence
        
        # Add the last chunk
        if current_chunk.strip():
            chunks.append({
                'content': current_chunk.strip(),
                'length': len(current_chunk),
                'id': len(chunks)
            })
        
        logger.info(f"Created {len(chunks)} chunks")
        return chunks
    
    def process_document(self, pdf_path: str) -> List[Dict]:
        """
        Complete document processing pipeline
        """
        # Extract text
        text = self.extract_text_from_pdf(pdf_path)
        
        if not text:
            return []
        
        # Create chunks
        chunks = self.chunk_text(text)
        
        return chunks