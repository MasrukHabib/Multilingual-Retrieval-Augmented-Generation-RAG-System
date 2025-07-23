import numpy as np
from typing import List, Tuple
from sklearn.metrics.pairwise import cosine_similarity

# Assuming Vectorizer is in the same src directory
from src.vectorizer import Vectorizer

class Retriever:
    def __init__(self, vectorizer: Vectorizer):
        """
        Initializes the Retriever with a Vectorizer instance.
        Args:
            vectorizer (Vectorizer): An instance of the Vectorizer class,
                                     which holds the embedding model and knowledge base embeddings.
        """
        self.vectorizer = vectorizer

    def retrieve_relevant_chunks(self, query: str, top_k: int = 5) -> List[str]:
        """
        Retrieves the top_k most relevant document chunks for a given query.

        Args:
            query (str): The user's query.
            top_k (int): The number of top relevant chunks to retrieve.

        Returns:
            List[str]: A list of the retrieved relevant text chunks.
        """
        if not query:
            return []

        # 1. Get embedding for the query
        query_embedding = self.vectorizer.get_embedding(query)
        if not query_embedding:
            print("Could not generate embedding for the query.")
            return []
        query_embedding_np = np.array(query_embedding).reshape(1, -1)

        # 2. Get all knowledge base embeddings and chunks
        kb_data = self.vectorizer.get_knowledge_base_data()
        if not kb_data:
            print("Knowledge base is empty. Please vectorize chunks first.")
            return []

        # Separate embeddings and chunks
        kb_embeddings = np.array([item[0] for item in kb_data])
        kb_chunks = [item[1] for item in kb_data]

        # Ensure kb_embeddings is 2D
        if kb_embeddings.ndim == 1:
            kb_embeddings = kb_embeddings.reshape(1, -1)

        # 3. Calculate cosine similarity between query and all chunks
        # Handle cases where kb_embeddings might be empty after filtering or if an issue occurred
        if kb_embeddings.shape[0] == 0:
            print("No valid embeddings in knowledge base for similarity calculation.")
            return []

        similarities = cosine_similarity(query_embedding_np, kb_embeddings)[0]

        # 4. Get indices of top_k most similar chunks
        # Use argsort to get indices that would sort the array, then take the last 'top_k'
        # to get the indices of the largest values.
        top_k_indices = similarities.argsort()[-top_k:][::-1] # [::-1] to get in descending order of similarity

        # 5. Retrieve the actual chunks
        relevant_chunks = [kb_chunks[i] for i in top_k_indices]

        return relevant_chunks

if __name__ == '__main__':


    import os
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    import config
    from src.chunker import recursive_character_text_splitter
    from src.data_loader import load_pdf_text

    # Ensure OpenAI API key is set for Vectorizer
    if not config.OPENAI_API_KEY or config.OPENAI_API_KEY == "your_openai_api_key_here":
        print("Please set your OpenAI API key in config.py or as an environment variable to run this example.")
    else:
        # 1. Load dummy text (or actual PDF content)
        sample_text = """
        বাংলা ভাষার উদ্ভব ইন্দো-ইউরোপীয় ভাষা পরিবার থেকে। এটি একটি সমৃদ্ধ ভাষা।
        প্রাচীন ভারতীয় আর্য ভাষার তিনটি স্তর রয়েছে: বৈদিক, সংস্কৃত এবং প্রাকৃত।
        মাগধী প্রাকৃত থেকে বাংলা ভাষার জন্ম।

        চর্যাপদ বাংলা সাহিত্যের প্রাচীনতম নিদর্শন। এটি দশম থেকে দ্বাদশ শতাব্দীর মধ্যে রচিত।
        মধ্যযুগ শুরু হয় ত্রয়োদশ শতাব্দী থেকে এবং শেষ হয় আঠারো শতাব্দীর মাঝামাঝি।
        আধুনিক যুগ উনিশ শতকের শুরু থেকে বর্তমান পর্যন্ত বিস্তৃত।

        বাংলা ব্যাকরণ ভাষার নিয়মকানুন নিয়ে আলোচনা করে।
        এর প্রধান আলোচ্য বিষয়গুলো হলো ধ্বনিতত্ত্ব, রূপতত্ত্ব, বাক্যতত্ত্ব এবং অর্থতত্ত্ব।
        ধ্বনিতত্ত্বে ধ্বনি ও বর্ণ নিয়ে আলোচনা করা হয়।
        রূপতত্ত্বে শব্দ ও পদ নিয়ে আলোচনা করা হয়।
        """
        
        # For a real test, load from your PDF:
        # pdf_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'knowledge_base', 'HSC26_Bangla_1st_paper.pdf')
        # sample_text = load_pdf_text(pdf_path)
        # if not sample_text:
        #     print("Failed to load PDF text. Using dummy text for demonstration.")
        #     sample_text = """... (your dummy text) ..."""

        # 2. Chunk the text
        chunks = recursive_character_text_splitter(sample_text, chunk_size=config.CHUNK_SIZE, chunk_overlap=config.CHUNK_OVERLAP)
        print(f"Generated {len(chunks)} chunks.")

        # 3. Initialize Vectorizer and vectorize chunks
        vectorizer = Vectorizer(api_key=config.OPENAI_API_KEY)
        vectorizer.vectorize_chunks(chunks)
        
        # 4. Initialize Retriever
        retriever = Retriever(vectorizer)

        # 5. Test retrieval with a query
        query_bangla = "বাংলা ভাষার উৎস কি?"
        query_english = "What is the origin of Bengali language?"
        
        print(f"\n--- Testing Retrieval for: '{query_bangla}' ---")
        relevant_chunks_bangla = retriever.retrieve_relevant_chunks(query_bangla, top_k=config.TOP_K_RETRIEVAL)
        if relevant_chunks_bangla:
            print("\nRelevant Chunks (Bangla):")
            for i, chunk in enumerate(relevant_chunks_bangla):
                print(f"Chunk {i+1}:\n{chunk}\n---")
        else:
            print("No relevant chunks found for Bangla query.")

        print(f"\n--- Testing Retrieval for: '{query_english}' ---")
        relevant_chunks_english = retriever.retrieve_relevant_chunks(query_english, top_k=config.TOP_K_RETRIEVAL)
        if relevant_chunks_english:
            print("\nRelevant Chunks (English):")
            for i, chunk in enumerate(relevant_chunks_english):
                print(f"Chunk {i+1}:\n{chunk}\n---")
        else:
            print("No relevant chunks found for English query.")
