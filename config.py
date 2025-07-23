import os

# OpenAI API Key
OPENAI_API_KEY = "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" # Make sure this is your actual API key


# OpenAI Model Names
EMBEDDING_MODEL = "text-embedding-ada-002"
GENERATION_MODEL = "gpt-3.5-turbo" 

# Document Chunking Parameters
CHUNK_SIZE = 700  
CHUNK_OVERLAP = 150 
# Retrieval Parameters
TOP_K_RETRIEVAL = 5 

# Paths
KNOWLEDGE_BASE_DIR = "knowledge_base"
PDF_FILE_NAME = "HSC26_Bangla_1st_paper.pdf"

# Full path to the PDF file
PDF_PATH = os.path.join(os.path.dirname(__file__), KNOWLEDGE_BASE_DIR, PDF_FILE_NAME)

# Vector Database Settings
VECTOR_DB_TYPE = "firestore"
FIRESTORE_COLLECTION_NAME = "rag_chunks"


