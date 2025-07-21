from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
import logging
from main import BengaliRAGApp

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Bengali RAG System API",
    description="A multilingual RAG system for Bengali and English queries",
    version="1.0.0"
)

# Initialize RAG system
rag_app = None

class QueryRequest(BaseModel):
    question: str
    session_id: Optional[str] = None

class QueryResponse(BaseModel):
    answer: str
    language: str
    confidence: float
    sources: List[Dict]
    conversation_context: Optional[str] = None

class HealthResponse(BaseModel):
    status: str
    message: str
    documents_count: int

@app.on_event("startup")
async def startup_event():
    """
    Initialize the RAG system on startup
    """
    global rag_app
    try:
        rag_app = BengaliRAGApp()
        
        # Setup knowledge base if not exists
        pdf_path = "data/HSC26_Bangla_1st_paper.pdf"
        success = rag_app.setup_knowledge_base(pdf_path)
        
        if success:
            logger.info("RAG system initialized successfully")
        else:
            logger.error("Failed to initialize RAG system")
            
    except Exception as e:
        logger.error(f"Startup error: {str(e)}")

@app.get("/", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint
    """
    if rag_app is None:
        raise HTTPException(status_code=500, detail="RAG system not initialized")
    
    try:
        doc_count = rag_app.vector_store.get_collection_count()
        return HealthResponse(
            status="healthy",
            message="Bengali RAG system is running",
            documents_count=doc_count
        )
    except Exception as e:
        logger.error(f"Health check error: {str(e)}")
        raise HTTPException(status_code=500, detail="System health check failed")

@app.post("/query", response_model=QueryResponse)
async def query_rag_system(request: QueryRequest):
    """
    Query the RAG system
    """
    if rag_app is None:
        raise HTTPException(status_code=500, detail="RAG system not initialized")
    
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    try:
        # Process the query
        response = rag_app.query(request.question)
        
        return QueryResponse(
            answer=response['answer'],
            language=response['language'],
            confidence=response['confidence'],
            sources=response['sources'],
            conversation_context=response.get('conversation_context', '')
        )
        
    except Exception as e:
        logger.error(f"Query processing error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to process query: {str(e)}")

@app.post("/clear-conversation")
async def clear_conversation():
    """
    Clear conversation history
    """
    if rag_app is None:
        raise HTTPException(status_code=500, detail="RAG system not initialized")
    
    try:
        rag_app.rag_system.clear_conversation()
        return {"message": "Conversation history cleared successfully"}
    except Exception as e:
        logger.error(f"Clear conversation error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to clear conversation")

@app.get("/test")
async def run_test_cases():
    """
    Run the predefined test cases
    """
    if rag_app is None:
        raise HTTPException(status_code=500, detail="RAG system not initialized")
    
    test_cases = [
        {
            "question": "অনুপমের ভাষায় সুপুরুষ কাকে বলা হয়েছে?",
            "expected": "শুম্ভুনাথ"
        },
        {
            "question": "কাকে অনুপমের ভাগ্য দেবতা বলে উল্লেখ করা হয়েছে?",
            "expected": "মামাকে"
        },
        {
            "question": "বিয়ের সময় কল্যাণীর প্রকৃত বয়স কত ছিল?",
            "expected": "১৫ বছর"
        }
    ]
    
    results = []
    
    try:
        for test_case in test_cases:
            response = rag_app.query(test_case["question"])
            
            # Check if expected answer is in response
            is_correct = test_case["expected"].lower() in response["answer"].lower()
            
            results.append({
                "question": test_case["question"],
                "expected": test_case["expected"],
                "got": response["answer"],
                "correct": is_correct,
                "confidence": response["confidence"],
                "language": response["language"]
            })
        
        return {
            "test_results": results,
            "summary": {
                "total": len(results),
                "passed": sum(1 for r in results if r["correct"]),
                "failed": sum(1 for r in results if not r["correct"])
            }
        }
        
    except Exception as e:
        logger.error(f"Test execution error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to run tests: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)