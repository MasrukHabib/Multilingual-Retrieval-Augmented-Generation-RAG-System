import os
import logging
from document_processor import DocumentProcessor
from vector_store import VectorStore
from rag_system import RAGSystem

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class BengaliRAGApp:
    def __init__(self):
        self.doc_processor = DocumentProcessor()
        self.vector_store = VectorStore()
        self.rag_system = RAGSystem(self.vector_store)
        
    def setup_knowledge_base(self, pdf_path: str):
        """
        Setup the knowledge base from PDF
        """
        logger.info("Starting knowledge base setup...")
        
        # Check if documents already exist
        if self.vector_store.get_collection_count() > 0:
            logger.info("Knowledge base already exists. Skipping setup.")
            return True
        
        # Process PDF
        chunks = self.doc_processor.process_document(pdf_path)
        
        if not chunks:
            logger.error("Failed to process PDF")
            return False
        
        # Add to vector store
        success = self.vector_store.add_documents(chunks)
        
        if success:
            logger.info("Knowledge base setup completed successfully!")
            return True
        else:
            logger.error("Failed to setup knowledge base")
            return False
    
    def query(self, question: str):
        """
        Query the RAG system
        """
        response = self.rag_system.generate_response(question)
        return response
    
    def run_test_cases(self):
        """
        Run the provided test cases
        """
        test_cases = [
            "অনুপমের ভাষায় সুপুরুষ কাকে বলা হয়েছে?",
            "কাকে অনুপমের ভাগ্য দেবতা বলে উল্লেখ করা হয়েছে?",
            "বিয়ের সময় কল্যাণীর প্রকৃত বয়স কত ছিল?"
        ]
        
        expected_answers = [
            "শুম্ভুনাথ",
            "মামাকে",
            "১৫ বছর"
        ]
        
        print("\n" + "="*50)
        print("RUNNING TEST CASES")
        print("="*50)
        
        for i, question in enumerate(test_cases):
            print(f"\nTest Case {i+1}:")
            print(f"Question: {question}")
            print(f"Expected: {expected_answers[i]}")
            
            response = self.query(question)
            print(f"Got: {response['answer']}")
            print(f"Confidence: {response['confidence']:.2f}")
            print(f"Language: {response['language']}")
            
            # Check if expected answer is in response
            if expected_answers[i].lower() in response['answer'].lower():
                print("✓ PASS")
            else:
                print("✗ FAIL")
            
            print("-" * 30)
    
    def interactive_mode(self):
        """
        Interactive chat mode
        """
        print("\n" + "="*50)
        print("BENGALI RAG SYSTEM - INTERACTIVE MODE")
        print("Type 'quit' to exit, 'clear' to clear conversation")
        print("="*50)
        
        while True:
            try:
                question = input("\nYour Question: ").strip()
                
                if question.lower() == 'quit':
                    break
                elif question.lower() == 'clear':
                    self.rag_system.clear_conversation()
                    print("Conversation cleared!")
                    continue
                elif not question:
                    continue
                
                response = self.query(question)
                
                print(f"\nAnswer: {response['answer']}")
                print(f"Language: {response['language']}")
                print(f"Confidence: {response['confidence']:.2f}")
                
                if response['sources']:
                    print("\nRelevant Sources:")
                    for i, source in enumerate(response['sources'], 1):
                        print(f"{i}. {source['content']} (similarity: {1-source['distance']:.2f})")
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error: {str(e)}")
        
        print("\nGoodbye!")

def main():
    app = BengaliRAGApp()
    
    # Setup knowledge base
    pdf_path = "data/HSC26_Bangla_1st_paper.pdf"  # Update path as needed
    
    if not os.path.exists(pdf_path):
        print(f"PDF file not found at: {pdf_path}")
        print("Please place the HSC26 Bangla 1st paper PDF in the data/ folder")
        return
    
    # Setup knowledge base
    if not app.setup_knowledge_base(pdf_path):
        print("Failed to setup knowledge base. Exiting.")
        return
    
    print(f"Knowledge base loaded with {app.vector_store.get_collection_count()} documents")
    
    # Run test cases
    app.run_test_cases()
    
    # Interactive mode
    app.interactive_mode()

if __name__ == "__main__":
    main()