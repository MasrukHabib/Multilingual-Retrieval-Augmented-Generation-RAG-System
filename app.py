# import streamlit as st
# import os
# import sys

# # Add the parent directory to the system path to allow imports from src
# sys.path.append(os.path.dirname(__file__))

# # Import modules from src and config
# from src.data_loader import load_pdf_text
# from src.chunker import recursive_character_text_splitter
# from src.vectorizer import Vectorizer
# from src.retriever import Retriever
# from src.llm_integration import LLMIntegration
# import config

# # --- Streamlit App Setup ---
# st.set_page_config(page_title="RAG System", layout="centered")

# st.title("Multilingual Retrieval-Augmented Generation (RAG) System")
# st.markdown("Ask questions in English or Bangla about the book content.")

# # --- Initialize Components (Cached to avoid re-running on every interaction) ---
# @st.cache_resource
# def initialize_rag_components():
#     """
#     Initializes and caches the RAG components: Vectorizer, Retriever, LLMIntegration.
#     Loads and processes the PDF knowledge base only once.
#     """
#     st.write("Initializing RAG system... This might take a moment.")
    
#     # 1. Load PDF Text
#     pdf_full_path = config.PDF_PATH
#     if not os.path.exists(pdf_full_path):
#         st.error(f"Error: PDF file not found at {pdf_full_path}. Please ensure it's in the 'knowledge_base' folder.")
#         return None, None, None

#     with st.spinner(f"Loading text from {config.PDF_FILE_NAME}..."):
#         text_content = load_pdf_text(pdf_full_path)
#         if not text_content:
#             st.error("Failed to load text from PDF. Please check the PDF file.")
#             return None, None, None
#         st.success("PDF text loaded successfully!")

#     # 2. Chunk Text
#     with st.spinner("Chunking document..."):
#         chunks = recursive_character_text_splitter(
#             text_content,
#             chunk_size=config.CHUNK_SIZE,
#             chunk_overlap=config.CHUNK_OVERLAP
#         )
#         if not chunks:
#             st.error("Failed to chunk document. The document might be empty or chunking parameters are too restrictive.")
#             return None, None, None
#         st.success(f"Document chunked into {len(chunks)} parts!")

#     # 3. Initialize Vectorizer and Embed Chunks
#     if not config.OPENAI_API_KEY or config.OPENAI_API_KEY == "your_openai_api_key_here":
#         st.error("OpenAI API key is not set in config.py. Please update it to proceed.")
#         return None, None, None

#     vectorizer = Vectorizer(api_key=config.OPENAI_API_KEY)
#     with st.spinner("Vectorizing chunks (this may take some time for large documents)..."):
#         vectorizer.vectorize_chunks(chunks)
#         if not vectorizer.get_knowledge_base_data():
#             st.error("Failed to vectorize chunks. Check your OpenAI API key and internet connection.")
#             return None, None, None
#         st.success("Chunks vectorized and knowledge base built!")

#     # 4. Initialize Retriever
#     retriever = Retriever(vectorizer)

#     # 5. Initialize LLM Integration
#     llm_integrator = LLMIntegration(api_key=config.OPENAI_API_KEY)
    
#     st.success("RAG System ready!")
#     return retriever, llm_integrator, vectorizer # Return vectorizer to check if KB is empty

# retriever, llm_integrator, vectorizer_instance = initialize_rag_components()

# if retriever and llm_integrator and vectorizer_instance and vectorizer_instance.get_knowledge_base_data():
   
#     # --- User Input ---
#     query = st.text_input("Enter your question (English or Bangla):", key="user_query")

#     if query:
#         with st.spinner("Searching for relevant information..."):
#             # 1. Retrieve relevant chunks
#             relevant_chunks = retriever.retrieve_relevant_chunks(query, top_k=config.TOP_K_RETRIEVAL)
            
#             if not relevant_chunks:
#                 st.warning("Could not find highly relevant information in the knowledge base.")
#                 # Attempt to answer without context if no relevant chunks found
#                 st.info("Attempting to answer without specific context from the document (may be less accurate)...")
#                 answer = llm_integrator.generate_answer(query, [])
#             else:
#                 st.subheader("Retrieved Context (for debugging/info):")
#                 for i, chunk in enumerate(relevant_chunks):
#                     st.text_area(f"Chunk {i+1}", chunk, height=100, disabled=True)
                
#                 # 2. Generate answer using LLM
#                 with st.spinner("Generating answer..."):
#                     answer = llm_integrator.generate_answer(query, relevant_chunks)
            
#             st.subheader("Generated Answer:")
#             st.write(answer)
# else:
#     st.warning("RAG system could not be fully initialized. Please check the errors above.")

import streamlit as st
import os
import sys

# Add the current directory and src directory to the system path
current_dir = os.path.dirname(__file__)
src_dir = os.path.join(current_dir, 'src')
sys.path.append(current_dir)
sys.path.append(src_dir)

# Import modules from src directory
from src.data_loader import load_pdf_text
from src.chunker import recursive_character_text_splitter
from src.vectorizer import Vectorizer
from src.retriever import Retriever
from src.llm_integration import LLMIntegration
import config

# --- Streamlit App Setup ---
st.set_page_config(page_title="RAG System", layout="centered")

st.title("Multilingual Retrieval-Augmented Generation (RAG) System")
st.markdown("Ask questions in English or Bangla about the book content.")

# --- Initialize Components (Cached to avoid re-running on every interaction) ---
@st.cache_resource
def initialize_rag_components():
    """
    Initializes and caches the RAG components: Vectorizer, Retriever, LLMIntegration.
    Loads and processes the PDF knowledge base only once.
    """
    st.write("Initializing RAG system... This might take a moment.")
    
    # 1. Load PDF Text
    pdf_full_path = config.PDF_PATH
    if not os.path.exists(pdf_full_path):
        st.error(f"Error: PDF file not found at {pdf_full_path}. Please ensure it's in the 'knowledge_base' folder.")
        return None, None, None

    with st.spinner(f"Loading text from {config.PDF_FILE_NAME}..."):
        text_content = load_pdf_text(pdf_full_path)
        if not text_content:
            st.error("Failed to load text from PDF. Please check the PDF file.")
            return None, None, None
        st.success("PDF text loaded successfully!")

    # 2. Chunk Text
    with st.spinner("Chunking document..."):
        chunks = recursive_character_text_splitter(
            text_content,
            chunk_size=config.CHUNK_SIZE,
            chunk_overlap=config.CHUNK_OVERLAP
        )
        if not chunks:
            st.error("Failed to chunk document. The document might be empty or chunking parameters are too restrictive.")
            return None, None, None
        st.success(f"Document chunked into {len(chunks)} parts!")

    # 3. Initialize Vectorizer and Embed Chunks
    if not config.OPENAI_API_KEY or config.OPENAI_API_KEY == "your_openai_api_key_here":
        st.error("OpenAI API key is not set in config.py. Please update it to proceed.")
        return None, None, None

    vectorizer = Vectorizer(api_key=config.OPENAI_API_KEY)
    with st.spinner("Vectorizing chunks (this may take some time for large documents)..."):
        vectorizer.vectorize_chunks(chunks)
        if not vectorizer.get_knowledge_base_data():
            st.error("Failed to vectorize chunks. Check your OpenAI API key and internet connection.")
            return None, None, None
        st.success("Chunks vectorized and knowledge base built!")

    # 4. Initialize Retriever
    retriever = Retriever(vectorizer)

    # 5. Initialize LLM Integration
    llm_integrator = LLMIntegration(api_key=config.OPENAI_API_KEY)
    
    st.success("RAG System ready!")
    return retriever, llm_integrator, vectorizer # Return vectorizer to check if KB is empty

retriever, llm_integrator, vectorizer_instance = initialize_rag_components()

if retriever and llm_integrator and vectorizer_instance and vectorizer_instance.get_knowledge_base_data():
   
    # --- User Input ---
    query = st.text_input("Enter your question (English or Bangla):", key="user_query")

    if query:
        with st.spinner("Searching for relevant information..."):
            # 1. Retrieve relevant chunks
            relevant_chunks = retriever.retrieve_relevant_chunks(query, top_k=config.TOP_K_RETRIEVAL)
            
            if not relevant_chunks:
                st.warning("Could not find highly relevant information in the knowledge base.")
                # Attempt to answer without context if no relevant chunks found
                st.info("Attempting to answer without specific context from the document (may be less accurate)...")
                answer = llm_integrator.generate_answer(query, [])
            else:
                st.subheader("Retrieved Context (for debugging/info):")
                for i, chunk in enumerate(relevant_chunks):
                    st.text_area(f"Chunk {i+1}", chunk, height=100, disabled=True)
                
                # 2. Generate answer using LLM
                with st.spinner("Generating answer..."):
                    answer = llm_integrator.generate_answer(query, relevant_chunks)
            
            st.subheader("Generated Answer:")
            st.write(answer)
else:
    st.warning("RAG system could not be fully initialized. Please check the errors above.")