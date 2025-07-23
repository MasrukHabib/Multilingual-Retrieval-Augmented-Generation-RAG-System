import PyPDF2
import os
import re

def clean_extracted_text(text: str) -> str:
    """
    Cleans and formats the extracted text to handle common PDF extraction issues.
    
    Args:
        text (str): Raw extracted text from PDF
        
    Returns:
        str: Cleaned and formatted text
    """
    if not text:
        return ""
    
    # Remove excessive whitespace and normalize line breaks
    text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)  # Multiple newlines to double newline
    text = re.sub(r'[ \t]+', ' ', text)  # Multiple spaces/tabs to single space
    text = re.sub(r'\n ', '\n', text)  # Remove spaces at beginning of lines
    
    # Fix common OCR/extraction issues
    text = re.sub(r'([a-zA-Z])\n([a-z])', r'\1 \2', text)  # Join broken words
    text = re.sub(r'([।])\s*\n\s*', r'\1 ', text)  # Fix Bangla sentence breaks
    text = re.sub(r'([.!?])\s*\n\s*([A-Z])', r'\1 \2', text)  # Fix English sentence breaks
    
    # Remove page numbers and headers/footers (common patterns)
    text = re.sub(r'\n\d+\n', '\n', text)  # Remove standalone page numbers
    text = re.sub(r'\n[পৃষ্ঠা|Page]\s*\d+\n', '\n', text)  # Remove "Page X" patterns
    
    return text.strip()

def load_pdf_text(pdf_path: str) -> str: 
    """
    Loads text content from a PDF file with improved formatting handling.

    Args:
        pdf_path (str): The path to the PDF file.

    Returns:
        str: The extracted and cleaned text content from the PDF.
             Returns an empty string if the file is not found or an error occurs.
    """
    if not os.path.exists(pdf_path):
        print(f"Error: PDF file not found at {pdf_path}")
        return ""

    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            print(f"PDF has {len(reader.pages)} pages")
            
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                page_text = page.extract_text()
                
                if page_text.strip():  # Only add non-empty pages
                    # Clean individual page text
                    cleaned_page_text = clean_extracted_text(page_text)
                    text += cleaned_page_text + "\n\n"  # Double newline between pages
                    print(f"Extracted page {page_num + 1}: {len(page_text)} characters")
                else:
                    print(f"Warning: Page {page_num + 1} appears to be empty or unreadable")
                    
    except Exception as e:
        print(f"Error reading PDF {pdf_path}: {e}")
        print("This might be due to:")
        print("- Corrupted PDF file")
        print("- Password-protected PDF")
        print("- Scanned PDF (requires OCR)")
        print("- Unsupported PDF format")
        return ""
    
    # Final cleaning of the entire text
    final_text = clean_extracted_text(text)
    print(f"Final text length after cleaning: {len(final_text)} characters")
    
    return final_text

# Alternative function using different extraction method
def load_pdf_text_alternative(pdf_path: str) -> str:
    """
    Alternative PDF text extraction method that might work better for some PDFs.
    """
    if not os.path.exists(pdf_path):
        print(f"Error: PDF file not found at {pdf_path}")
        return ""

    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            
            for page_num, page in enumerate(reader.pages):
                try:
                    # Try different extraction methods
                    page_text = ""
                    
                    # Method 1: Standard extraction
                    page_text = page.extract_text()
                    
                    # Method 2: If standard fails, try with visitor pattern
                    if not page_text.strip():
                        def visitor_body(text, cm, tm, fontDict, fontSize):
                            return text
                        page_text = page.extract_text(visitor_text=visitor_body)
                    
                    if page_text.strip():
                        text += clean_extracted_text(page_text) + "\n\n"
                        
                except Exception as page_error:
                    print(f"Error extracting page {page_num + 1}: {page_error}")
                    continue
                    
    except Exception as e:
        print(f"Error reading PDF {pdf_path}: {e}")
        return ""
    
    return clean_extracted_text(text)

if __name__ == '__main__':
    pdf_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'knowledge_base', 'HSC26_Bangla_1st_paper.pdf')
    
    # Check if file exists and load it
    if os.path.exists(pdf_path):
        print("Attempting standard extraction...")
        pdf_content = load_pdf_text(pdf_path)
        
        # If standard extraction fails or gives poor results, try alternative
        if not pdf_content or len(pdf_content) < 100:
            print("Standard extraction failed or gave minimal content. Trying alternative method...")
            pdf_content = load_pdf_text_alternative(pdf_path)
        
        if pdf_content:
            print(f"Successfully loaded PDF. Content length: {len(pdf_content)} characters")
            print(f"First 500 characters:\n{pdf_content[:500]}...")
            
            # Save extracted text for debugging
            debug_file = os.path.join(os.path.dirname(pdf_path), 'extracted_text_debug.txt')
            try:
                with open(debug_file, 'w', encoding='utf-8') as f:
                    f.write(pdf_content)
                print(f"Debug: Extracted text saved to {debug_file}")
            except Exception as e:
                print(f"Could not save debug file: {e}")
        else:
            print("Failed to extract content from PDF")
            print("Consider using OCR tools like Tesseract for scanned PDFs")
    else:
        print(f"PDF file not found at: {pdf_path}")
        print("Please ensure the PDF file exists in the knowledge_base folder")
