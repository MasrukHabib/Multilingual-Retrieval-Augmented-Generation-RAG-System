### Multilingual RAG (Retrieval-Augmented Generation) system

## Architecture

PDF → Text Extraction → Chunking → Vectorization → Retrieval → LLM Generation

## File Structure & Purpose

**Core Application**

- `app.py`: Streamlit web interface - main entry point for users
- `config.py`: Configuration settings (API keys, model names, parameters)

**Data Pipeline (`src/` folder)**

- `data_loader.py`: Extracts and cleans text from PDF files
- `chunker.py`: Splits text into manageable chunks with Bangla-aware splitting
- `vectorizer.py`: Converts text chunks into embeddings using OpenAI + FAISS
- `retriever.py`: Finds most relevant chunks for user queries
- `llm_integration.py`: Generates answers using OpenAI GPT models

## How It Works

1.  **Setup:** Load PDF → Clean text → Split into chunks → Create embeddings
2.  **Query:** User asks question → Find similar chunks → Generate contextual answer
3.  **Response:** Returns answer in same language as question (English/Bangla)

## Key Features

- **Multilingual:** Handles both English and Bangla queries
- **Smart Chunking:** Respects sentence boundaries and Bangla punctuation
- **Vector Search:** Uses FAISS for fast similarity search
- **Context-Aware:** Only answers based on provided document content
- **Web Interface:** Easy-to-use Streamlit dashboard

## Technologies Used

- **Frontend:** Streamlit
- **ML/AI:** OpenAI API (embeddings + GPT)
- **Vector DB:** FAISS
- **PDF Processing:** PyPDF2
- **Text Processing:** Custom Bangla-aware splitters
