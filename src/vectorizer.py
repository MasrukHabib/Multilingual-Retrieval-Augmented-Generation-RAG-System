import openai
import numpy as np
import os
from typing import List, Dict, Tuple

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
        openai.api_key = api_key
        self.model_name = model_name
        self.knowledge_base_embeddings = [] # Stores (embedding, chunk_text) tuples

    def get_embedding(self, text: str) -> List[float]:
        """
        Generates an embedding for a given text using the OpenAI API.

        Args:
            text (str): The input text to embed.

        Returns:
            List[float]: The embedding vector as a list of floats.
                         Returns an empty list if an error occurs.
        """
        try:
            response = openai.embeddings.create(
                input=text,
                model=self.model_name
            )
            return response.data[0].embedding
        except openai.APIError as e:
            print(f"OpenAI API Error during embedding: {e}")
            return []
        except Exception as e:
            print(f"An unexpected error occurred during embedding: {e}")
            return []

    def vectorize_chunks(self, chunks: List[str]) -> None:
        """
        Generates embeddings for a list of text chunks and stores them
        in the knowledge base.

        Args:
            chunks (List[str]): A list of text chunks.
        """
        self.knowledge_base_embeddings = [] # Clear existing embeddings if re-vectorizing
        print(f"Vectorizing {len(chunks)} chunks...")
        for i, chunk in enumerate(chunks):
            embedding = self.get_embedding(chunk)
            if embedding:
                self.knowledge_base_embeddings.append((np.array(embedding), chunk))
            if (i + 1) % 10 == 0:
                print(f"Processed {i + 1}/{len(chunks)} chunks...")
        print("Vectorization complete.")

    def get_knowledge_base_data(self) -> List[Tuple[np.ndarray, str]]:
        """
        Returns the stored knowledge base embeddings and their corresponding chunks.

        Returns:
            List[Tuple[np.ndarray, str]]: A list of (embedding, chunk_text) tuples.
        """
        return self.knowledge_base_embeddings

if __name__ == '__main__':
    # Example usage for testing
    # Ensure you have your OpenAI API key set in config.py or as an environment variable
    # For testing, you can temporarily set it here if not using config.py
    # os.environ["OPENAI_API_KEY"] = "YOUR_TEST_API_KEY" # ONLY FOR LOCAL TESTING, NOT FOR PRODUCTION

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

