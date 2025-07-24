# Multilingual RAG (Retrieval-Augmented Generation) system

## Architecture

PDF → Text Extraction → Chunking → Vectorization → Retrieval → LLM Generation

## File Structure & Purpose

**Core Application**

- `app.py`: Streamlit web interface - main entry point for users.
- `config.py`: Configuration settings (API keys, model names, parameters).

**Data Pipeline (`src/` folder)**

- `data_loader.py`: Extracts and cleans text from PDF files.
- `chunker.py`: Splits text into manageable chunks with Bangla-aware splitting.
- `vectorizer.py`: Converts text chunks into embeddings using OpenAI + FAISS.
- `retriever.py`: Finds most relevant chunks for user queries.
- `llm_integration.py`: Generates answers using OpenAI GPT models.

## How It Works

1.  **Setup:** Load PDF → Clean text → Split into chunks → Create embeddings.
2.  **Query:** User asks question → Find similar chunks → Generate contextual answer.
3.  **Response:** Returns answer in same language as question (English/Bangla).

## Key Features

- **Multilingual:** Handles both English and Bangla queries.
- **Smart Chunking:** Respects sentence boundaries and Bangla punctuation.
- **Vector Search:** Uses FAISS for fast similarity search.
- **Context-Aware:** Only answers based on provided document content.
- **Web Interface:** Streamlit dashboard.

## Technologies Used

- **Frontend:** Streamlit
- **ML/AI:** OpenAI API (embeddings + GPT)
- **Vector DB:** FAISS
- **PDF Processing:** PyPDF2
- **Text Processing:** Custom Bangla-aware splitters

## Installation Process:
**step-0:** clone the repositories
**step-1:** Create a Virtual Environment 
        python -m venv venv
        Activate the virtual environment: .\venv\Scripts\activate (for windows), source venv/bin/activate (for macOS/Linux:)
**Step-3:** Install Dependencies
        pip install -r requirements.txt
**step-4:** Run the web application 
        streamlit run app.py
  

## Quenstion and Answer


1. What method or library did you use to extract the text, and why? Did you face any formatting challenges with the PDF content?
Answer: 
I chose PyPDF2 because it's a robust and widely used Python library for interacting with PDF documents. It's excellent for programmatic tasks like reading, splitting, merging, and, importantly for our case, extracting text from PDFs. Its simplicity and efficiency for direct text extraction make it a good fit for building a RAG system's initial data loading step.

2. What chunking strategy did you choose (e.g. paragraph-based, sentence-based, character limit)? Why do you think it works well for semantic retrieval?
Answer:
I used a recursive character splitting strategy that prioritizes semantic boundaries.
The chosen chunking strategy employs a recursive character splitting method that prioritizes semantic boundaries for optimal retrieval. It systematically breaks text using a hierarchy of separators, starting with Bangla sentence endings, then paragraph and single newlines, followed by spaces, and finally individual characters. This approach ensures semantic coherence, as each chunk is more likely to encapsulate a complete thought, leading to more accurate vector embeddings and improved similarity matching during retrieval. Furthermore, context preservation is achieved through chunk overlap, which prevents information loss for ideas spanning multiple chunks, while manageable chunk sizes ensure compatibility with LLM context windows and precise embedding focus.

3. What embedding model did you use? Why did you choose it? How does it capture the meaning of the text?
Answer: 
I used OpenAI's text-embedding-ada-002 model because it's cost-effective, performs well across various tasks including semantic search, and handles multiple languages like Bangla effectively. This model captures text meaning by converting it into high-dimensional numerical vectors. Texts with similar meanings are mapped to vectors that are close in this vector space. Through extensive training, it learns contextual understanding and semantic relationships, allowing us to find conceptually related document chunks to a user's query efficiently using cosine similarity.

4. How are you comparing the query with your stored chunks? Why did you choose this similarity method and storage setup?
Answer: 
I compare queries with stored chunks using Cosine Similarity within the FAISS vector database. FAISS is chosen for its highly efficient similarity search capabilities on large vector datasets, enabling rapid retrieval of relevant document chunks. Its ability to save and load indexes locally provides crucial persistence, speeding up subsequent application runs. This setup, seamlessly integrated via LangChain, leverages cosine similarity to identify semantically similar text, ensuring that the retrieved chunks accurately reflect the query's meaning.

5. Do the results seem relevant? If not, what might improve them (e.g. better chunking, better embedding model, larger document)?
Answer: 
It's not providing 100% accurate answers. We need to supply a larger document for better context. Additionally, we can improve the chunking strategy and experiment with different embedding models. Alternatively, we could fine-tune the model to better suit our specific requirements


