# Multilingual-Retrieval-Augmented-Generation-RAG-System

A multilingual Retrieval-Augmented Generation (RAG) system that can understand and respond to both English and Bengali queries using HSC Bangla 1st paper content.

## Features

- 🔍 **Multilingual Support**: Handles both Bengali and English queries
- 📚 **PDF Processing**: Extracts and processes text from Bengali PDF documents
- 🧠 **Smart Chunking**: Intelligent text chunking with overlap for better context
- 🔤 **Vector Search**: Uses multilingual embeddings for semantic search
- 💬 **Conversation Memory**: Maintains short-term conversation context
- 🚀 **REST API**: Simple API for integration
- ✅ **Built-in Testing**: Automated test cases for validation

## Quick Start

### 1. Clone and Setup

```bash
git clone <your-repo-url>
cd bengali-rag-system
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Add PDF Document

Place your `HSC26_Bangla_1st_paper.pdf` file in the `data/` folder.

### 3. Run the System

```bash
cd src
python main.py
```

### 4. Start the API (Optional)

```bash
cd src
python -m uvicorn api:app --reload
```

## Architecture
