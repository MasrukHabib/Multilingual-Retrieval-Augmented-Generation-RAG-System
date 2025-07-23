import openai
import numpy as np
import os
from typing import List, Dict, Tuple

# LangChain imports
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.docstore.document import Document

# Assuming config.py is in the parent directory
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import config

class Vectorizer:
    def __init__(self, api_key: str, model_name: str = config.EMBEDDING_MODEL):
        """
        Initializes the Vectorizer with an OpenAI API key and embedding model.

        Args:
            api_key (str): Your OpenAI API key.
            model_name (str): The name of the OpenAI embedding model to use.
        """
        self.api_key = api_key
        self.model_name = model_name
        self.knowledge_base_embeddings = [] # Keep for backward compatibility
        self.faiss_db = None  # FAISS vector store
        self.embedding_model = OpenAIEmbeddings(
            openai_api_key=api_key,
            model=model_name
        )

    def get_embedding(self, text: str) -> List[float]:
        """
        Generates an embedding for a given text using the OpenAI API.
        """
        try:
            embedding = self.embedding_model.embed_query(text)
            return embedding
        except Exception as e:
            print(f"Error during embedding: {e}")
            return []

    def vectorize_chunks(self, chunks: List[str]) -> None:
        """
        Generates embeddings for a list of text chunks using FAISS.
        """
        print(f"Vectorizing {len(chunks)} chunks using FAISS...")
        
        # Convert text chunks to Document format
        documents = [Document(page_content=chunk) for chunk in chunks]
        
        try:
            # Create FAISS vector store
            self.faiss_db = FAISS.from_documents(documents, self.embedding_model)
            
            # Save vector store locally
            faiss_index_path = os.path.join(os.path.dirname(__file__), "..", "faiss_index")
            self.faiss_db.save_local(faiss_index_path)
            
            # Also populate the legacy format for backward compatibility
            self.knowledge_base_embeddings = []
            for chunk in chunks:
                embedding = self.get_embedding(chunk)
                if embedding:
                    self.knowledge_base_embeddings.append((np.array(embedding), chunk))
            
            print("Vectorization complete and saved to FAISS index.")
            
        except Exception as e:
            print(f"Error during vectorization: {e}")

    def load_faiss_index(self, index_path: str = None):
        """
        Load existing FAISS index from disk.
        """
        if index_path is None:
            index_path = os.path.join(os.path.dirname(__file__), "..", "faiss_index")
        
        try:
            self.faiss_db = FAISS.load_local(index_path, self.embedding_model)
            print("FAISS index loaded successfully.")
        except Exception as e:
            print(f"Error loading FAISS index: {e}")

    def get_knowledge_base_data(self) -> List[Tuple[np.ndarray, str]]:
        """
        Returns the stored knowledge base embeddings and their corresponding chunks.
        """
        return self.knowledge_base_embeddings
    
    def get_faiss_db(self):
        """
        Returns the FAISS vector store.
        """
        return self.faiss_db

    def similarity_search(self, query: str, k: int = 5) -> List[str]:
        """
        Perform similarity search using FAISS.
        """
        if self.faiss_db is None:
            print("FAISS database not initialized. Call vectorize_chunks first.")
            return []
        
        try:
            docs = self.faiss_db.similarity_search(query, k=k)
            return [doc.page_content for doc in docs]
        except Exception as e:
            print(f"Error during similarity search: {e}")
            return []

if __name__ == '__main__':
    
    # Dummy chunks for testing
    test_chunks = [
        "কজলকাল পর্িপূণিরূকপ আত্মপ্রকাি কিল।",
        "অনুপমের ভাষায় সুপুরুষ কাকে বলা হয়েছে?",
        "কাকে অনুপমের ভাগ্য দেবতা বলে উল্লেখ করা হয়েছে?",
        "বিয়ের সময় কল্যাণীর প্রকৃত বয়স কত ছিল?",
        "The quick brown fox jumps over the lazy dog.",
        "সূর্য পূর্ব দিকে ওঠে এবং পশ্চিম দিকে অস্ত যায়।"
    ]

    # Initialize Vectorizer
    # Make sure config.OPENAI_API_KEY is set correctly
    if not config.OPENAI_API_KEY or config.OPENAI_API_KEY == "your_openai_api_key_here":
        print("Please set your OpenAI API key in config.py or as an environment variable to run this example.")
    else:
        vectorizer = Vectorizer(api_key=config.OPENAI_API_KEY)
        
        # Vectorize the dummy chunks
        vectorizer.vectorize_chunks(test_chunks)
        
        # Retrieve and print some vectorized data
        kb_data = vectorizer.get_knowledge_base_data()
        print(f"\nStored {len(kb_data)} embeddings.")
        if kb_data:
            print(f"First chunk: '{kb_data[0][1]}'")
            print(f"First embedding (first 5 values): {kb_data[0][0][:5]}...")
        else:
            print("No embeddings were generated. Check API key and network connection.")

