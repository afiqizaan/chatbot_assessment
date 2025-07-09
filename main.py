from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import logging

# Import our modules
from chatbot.agent import EnhancedChatbotAgent
from chatbot.calculator import calculate
from chatbot.rag import enhanced_rag
from database.outlets_db import text2sql, outlets_db

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="ZUS Coffee Chatbot API",
    description="AI Chatbot with Product RAG, Text2SQL Outlets, and Calculator Integration",
    version="4.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Initialize the enhanced chatbot agent
agent = EnhancedChatbotAgent()

# Pydantic models for API requests/responses
class QueryInput(BaseModel):
    query: str

class ProductResponse(BaseModel):
    query: str
    answer: str
    success: bool

class OutletResponse(BaseModel):
    query: str
    sql_query: str
    results: List[Dict[str, Any]]
    count: int
    success: bool

class ChatResponse(BaseModel):
    response: str
    conversation_state: Dict[str, Any]

# Product-KB Retrieval Endpoint
@app.get("/products", response_model=ProductResponse)
async def products(query: str = Query(..., description="Product search query")):
    """
    Product-KB Retrieval Endpoint
    
    Ingest ZUS product docs into a vector store and retrieve top-k results with AI-generated summary.
    Source: ZUS Coffee drinkware products
    """
    try:
        logger.info(f"Product query received: {query}")
        
        # Use enhanced RAG system with AI summary
        answer = enhanced_rag.query_products(query)
        
        return ProductResponse(
            query=query,
            answer=answer,
            success=True
        )
        
    except Exception as e:
        logger.error(f"Product query error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Outlets Text2SQL Endpoint
@app.get("/outlets", response_model=OutletResponse)
async def outlets(query: str = Query(..., description="Natural language query about outlets")):
    """
    Outlets Text2SQL Endpoint
    
    Maintain a SQL DB of ZUS outlets (location, hours, services).
    Source: ZUS Coffee outlets in Kuala Lumpur/Selangor
    """
    try:
        logger.info(f"Outlet query received: {query}")
        
        # Convert NL query to SQL and execute
        sql_query = text2sql.convert_to_sql(query)
        results = text2sql.query_outlets(query)
        
        return OutletResponse(
            query=query,
            sql_query=sql_query,
            results=results,
            count=len(results),
            success=True
        )
        
    except Exception as e:
        logger.error(f"Outlet query error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Enhanced Chatbot Endpoint
@app.post("/chat", response_model=ChatResponse)
async def chat(input: QueryInput):
    """
    Enhanced Chatbot with integration to all three endpoints:
    - Calculator tool
    - Product RAG system
    - Outlets Text2SQL system
    """
    try:
        logger.info(f"Chat query received: {input.query}")
        
        # Use enhanced agent that can call all tools
        response = agent.respond(input.query)
        
        # Get current conversation state
        conversation_state = agent.get_conversation_state()
        
        return ChatResponse(
            response=response,
            conversation_state=conversation_state
        )
        
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Calculator Endpoint (for tool integration)
@app.get("/calc")
async def calculator(
    a: float = Query(..., description="First number"),
    b: float = Query(..., description="Second number"),
    op: str = Query(..., description="Operation: add, sub, mul, div")
):
    """
    Calculator endpoint for mathematical operations
    Used by the chatbot agent for arithmetic queries
    """
    try:
        result = calculate(a, b, op)
        return {"result": result, "operation": f"{a} {op} {b}"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Root Endpoint - Serve the web UI
@app.get("/")
async def root():
    """Root endpoint - Serve the web UI"""
    return FileResponse("static/index.html")

# API Info Endpoint
@app.get("/api")
async def api_info():
    """API information endpoint"""
    return {
        "message": "ZUS Coffee Chatbot API",
        "version": "4.0.0",
        "endpoints": {
            "chat": "/chat",
            "products": "/products",
            "outlets": "/outlets",
            "calculator": "/calc",
            "health": "/health",
            "docs": "/docs"
        },
        "description": "AI Chatbot with Product RAG, Text2SQL Outlets, and Calculator Integration"
    }

# Health Check Endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "services": {
            "chatbot": "EnhancedChatbotAgent",
            "products": "EnhancedProductRAG",
            "outlets": "Text2SQLConverter",
            "calculator": "CalculatorTool"
        },
        "version": "4.0.0"
    }

# Database Schema Endpoint
@app.get("/schema")
async def get_schema():
    """Get database schema information"""
    return {
        "outlets_table": {
            "columns": ["id", "name", "location", "address", "opening_hours", "phone", "services", "latitude", "longitude"],
            "description": "ZUS Coffee outlets with location, hours, and services information"
        },
        "products": {
            "source": "ZUS Coffee drinkware products",
            "vector_store": "FAISS with OpenAI embeddings",
            "summary": "AI-generated summaries using GPT-3.5-turbo"
        }
    }

# Conversation State Management
@app.get("/chat/state")
async def get_conversation_state():
    """Get current conversation state for debugging"""
    try:
        state = agent.get_conversation_state()
        return state
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat/reset")
async def reset_conversation():
    """Reset conversation state"""
    try:
        agent.reset_conversation()
        return {"message": "Conversation state reset successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Sample Data Endpoints
@app.get("/outlets/sample")
async def get_sample_outlets():
    """Get sample outlet data"""
    try:
        outlets = outlets_db.get_all_outlets()
        return {"outlets": outlets, "count": len(outlets)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/products/sample")
async def get_sample_products():
    """Get sample product data"""
    try:
        # Return a sample product query result
        result = enhanced_rag.query_products("coffee cup")
        return {"sample_query": "coffee cup", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 