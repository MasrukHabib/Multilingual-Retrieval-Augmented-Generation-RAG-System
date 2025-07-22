import os

# OpenAI API Key
# It is highly recommended to load this from an environment variable for security.
# Example: OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your_openai_api_key_here")
# For this basic setup, you can directly paste it, but be cautious with sharing.
OPENAI_API_KEY = "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" # Make sure this is your actual API key

# OpenAI Model Names
EMBEDDING_MODEL = "text-embedding-ada-002"
GENERATION_MODEL = "gpt-3.5-turbo" # You can change this to "gpt-4" or other models if available

# Document Chunking Parameters
# Reduced CHUNK_SIZE to help manage overall context length
CHUNK_SIZE = 700  # Maximum number of characters per chunk (reduced from 1000)
CHUNK_OVERLAP = 150 # Number of characters to overlap between consecutive chunks (reduced from 200)

# Retrieval Parameters
# Reduced TOP_K_RETRIEVAL to send fewer chunks to the LLM
TOP_K_RETRIEVAL = 5 # Number of top relevant chunks to retrieve for LLM context (reduced from 10/15)

# Paths
# Adjust these paths if your file structure changes
KNOWLEDGE_BASE_DIR = "knowledge_base"
PDF_FILE_NAME = "HSC26_Bangla_1st_paper.pdf"

# Full path to the PDF file
# This assumes config.py is in the root directory and knowledge_base is a sibling directory.
# Adjust os.path.join if your project structure is different.
PDF_PATH = os.path.join(os.path.dirname(__file__), KNOWLEDGE_BASE_DIR, PDF_FILE_NAME)

# Vector Database Settings
# Using Firestore as the vector database for storing chunks and embeddings.
VECTOR_DB_TYPE = "firestore"
# Collection name for storing the document chunks and their embeddings in Firestore.
# This will be stored under /artifacts/{appId}/public/data/rag_chunks
FIRESTORE_COLLECTION_NAME = "rag_chunks"

# Firebase config and app ID are provided by the Canvas environment at runtime.
# You do not need to define them here.
