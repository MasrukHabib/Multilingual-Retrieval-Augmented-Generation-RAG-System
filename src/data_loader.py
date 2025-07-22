import PyPDF2
import os

def load_pdf_text(pdf_path: str) -> str:
    """
    Loads text content from a PDF file.

    Args:
        pdf_path (str): The path to the PDF file.

    Returns:
        str: The extracted text content from the PDF.
             Returns an empty string if the file is not found or an error occurs.
    """
    if not os.path.exists(pdf_path):
        print(f"Error: PDF file not found at {pdf_path}")
        return ""

    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text() + "\n" # Add newline between pages
    except Exception as e:
        print(f"Error reading PDF {pdf_path}: {e}")
        return ""
    return text

if __name__ == '__main__':
    # Example usage (for testing purposes)
    # Create a dummy PDF file for testing if you don't have one
    # You would replace 'path/to/your/HSC26_Bangla_1st_paper.pdf' with the actual path
    dummy_pdf_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'knowledge_base', 'dummy_bangla.pdf')
    # This is a placeholder. In a real scenario, you'd have your actual PDF here.
    # If you want to test, you'd need to create a simple PDF with some text.
    # For now, let's assume the PDF exists in the knowledge_base folder.
    
    # To run this example, ensure you have a PDF named 'dummy_bangla.pdf'
    # in the 'knowledge_base' folder relative to your project root.
    # For a real run, change 'dummy_bangla.pdf' to 'HSC26_Bangla_1st_paper.pdf'
    
    # For demonstration, let's just print a message if the file doesn't exist
    # and assume the user will replace it with the actual file.
    
    # For actual testing, you'd call load_pdf_text with your real PDF path:
    # pdf_content = load_pdf_text(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'knowledge_base', 'HSC26_Bangla_1st_paper.pdf'))
    # print(f"First 500 characters of PDF content:\n{pdf_content[:500]}...")
    print("To test data_loader.py, place a PDF in the 'knowledge_base' folder and run this file directly.")
    print("Example: python src/data_loader.py")

