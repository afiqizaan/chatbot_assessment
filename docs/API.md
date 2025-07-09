# API Specification

## Overview
The ZUS Coffee AI Chatbot API provides a comprehensive set of endpoints for conversational AI, product search, outlet information, and calculations. Built with FastAPI, it includes RAG-powered product search and Text2SQL outlet queries.

## Base URL
- **Production**: `https://chatbot-engineer-demo.onrender.com/`

## Authentication
Currently, no authentication is required. All endpoints are publicly accessible.

## Endpoints

### 1. Chat Endpoint

**POST** `/chat`

Main conversational endpoint that integrates all chatbot capabilities.

#### Request Body
```json
{
  "query": "string"
}
```

#### Example Request
```bash
curl -X POST "https://chatbot-engineer-demo.onrender.com/chat" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is 15 plus 27?"}'
```

#### Example Response
```json
{
  "response": "The answer is 42.",
  "conversation_state": {
    "location": null,
    "outlet": null,
    "current_state": "initial",
    "conversation_history": [
      {
        "user_input": "What is 15 plus 27?",
        "bot_response": "The answer is 42.",
        "intent": "calculation",
        "timestamp": "2024-01-15T10:30:00"
      }
    ],
    "confidence_score": 0.9
  }
}
```

#### Supported Query Types
- **Calculations**: "What is 5 plus 3?", "Calculate 10 times 5"
- **Product Search**: "Show me coffee cups", "I want to buy a mug"
- **Outlet Queries**: "Outlets in KL", "What time does SS2 open?"
- **General Chat**: "Hello", "How are you?"

---

### 2. Product Search (RAG)

**GET** `/products`

RAG-powered product search using FAISS vector store and Google Gemini embeddings.

#### Query Parameters
- `query` (string, required): Product search query

#### Example Request
```bash
curl "https://chatbot-engineer-demo.onrender.com/products?query=coffee%20cup"
```

#### Example Response
```json
{
  "query": "coffee cup",
  "answer": "We have several ZUS drinkware options, like the All Day Cup (from RM55) and the OG Ceramic Mug (RM39).",
  "success": true
}
```

#### Technical Details
- **Vector Store**: FAISS with Google Gemini embedding-001
- **LLM**: Google Gemini 2.0 Flash for summarization
- **Data Source**: ZUS Coffee drinkware catalog
- **Search Method**: Semantic similarity search with AI-generated summaries

---

### 3. Outlet Information (Text2SQL)

**GET** `/outlets`

Natural language to SQL conversion for outlet queries.

#### Query Parameters
- `query` (string, required): Natural language outlet query

#### Example Request
```bash
curl "https://chatbot-engineer-demo.onrender.com/outlets?query=outlets%20in%20Petaling%20Jaya"
```

#### Example Response
```json
{
  "query": "outlets in Petaling Jaya",
  "sql_query": "SELECT * FROM outlets WHERE LOWER(location) LIKE '%petaling jaya%'",
  "results": [
    {
      "id": 1,
      "name": "ZUS Coffee SS2",
      "location": "Petaling Jaya",
      "address": "No. 1, Jalan SS2/24, SS2, 47300 Petaling Jaya",
      "opening_hours": "7:00 AM - 11:00 PM",
      "phone": "+603-1234-5678",
      "services": "Coffee, Food, WiFi",
      "latitude": 3.1077,
      "longitude": 101.6067
    }
  ],
  "count": 3,
  "success": true
}
```

#### Supported Query Types
- **Location-based**: "outlets in KL", "stores in Petaling Jaya"
- **Service-based**: "outlets with drive-thru", "stores with WiFi"
- **Time-based**: "outlets open at 9 AM"
- **Specific outlets**: "SS2 outlet", "Damansara store"

#### Technical Details
- **Database**: SQLite with 8 sample ZUS outlets
- **Text2SQL**: Pattern-based conversion (production would use LLM)
- **Schema**: id, name, location, address, opening_hours, phone, services, coordinates

---

### 4. Calculator

**GET** `/calc`

Simple arithmetic operations.

#### Query Parameters
- `a` (float, required): First number
- `b` (float, required): Second number
- `op` (string, required): Operation (add, sub, mul, div)

#### Example Request
```bash
curl "https://chatbot-engineer-demo.onrender.com/calc?a=10&b=5&op=add"
```

#### Example Response
```json
{
  "result": 15.0,
  "operation": "10 add 5"
}
```

#### Supported Operations
- `add`: Addition
- `sub`: Subtraction
- `mul`: Multiplication
- `div`: Division (with zero division protection)

---

### 5. Health Check

**GET** `/health`

System health and service status.

#### Example Request
```bash
curl "https://chatbot-engineer-demo.onrender.com/health"
```

#### Example Response
```json
{
  "status": "healthy",
  "services": {
    "chatbot": "EnhancedChatbotAgent",
    "products": "EnhancedProductRAG",
    "outlets": "Text2SQLConverter",
    "calculator": "CalculatorTool"
  },
  "version": "4.0.0"
}
```

---

### 6. API Information

**GET** `/api`

API overview and endpoint information.

#### Example Response
```json
{
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
```

---

### 7. Conversation State Management

**GET** `/chat/state`

Get current conversation state for debugging.

#### Example Response
```json
{
  "location": "petaling jaya",
  "outlet": "ss 2",
  "current_state": "outlet_confirmed",
  "conversation_history": [...],
  "confidence_score": 0.9
}
```

**POST** `/chat/reset`

Reset conversation state.

#### Example Response
```json
{
  "message": "Conversation state reset successfully"
}
```

---

### 8. Sample Data Endpoints

**GET** `/outlets/sample`

Get all sample outlet data.

**GET** `/products/sample`

Get sample product search result.

---

## Error Handling

### HTTP Status Codes
- `200`: Success
- `400`: Bad Request (invalid parameters)
- `500`: Internal Server Error

### Error Response Format
```json
{
  "detail": "Error message description"
}
```

### Common Error Scenarios
1. **Missing Parameters**: Required query parameters not provided
2. **Invalid Operations**: Unsupported calculator operations
3. **API Downtime**: External service failures (Gemini API, database)
4. **Malicious Input**: SQL injection attempts, oversized payloads

### Error Handling Strategy
- **Graceful Degradation**: Services fail independently
- **User-Friendly Messages**: No technical error leaks
- **Logging**: Comprehensive error logging for debugging
- **Fallbacks**: Default responses when services unavailable

---

## Rate Limiting
Currently, no rate limiting is implemented. Consider implementing for production use.

## CORS
CORS is enabled for web UI integration. All origins are allowed in development.

## OpenAPI Documentation
Interactive API documentation is available at `/docs` (Swagger UI) and `/redoc` (ReDoc).

## Testing
Run the test suite to verify API functionality:
```bash
python -m pytest tests/ -v
```

## Deployment
See `DEPLOYMENT.md` for deployment instructions on Render.