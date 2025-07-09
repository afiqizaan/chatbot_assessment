# ZUS Coffee AI Chatbot

## 🚀 Project Overview
A production-ready multi-turn conversational AI chatbot for ZUS Coffee with:
- **Beautiful Web UI** - Modern chat interface with real-time responses
- **State management** and context awareness across conversations
- **Agentic planning** and intelligent tool integration
- **RAG-powered product search** using Google Gemini embeddings
- **FastAPI backend** with comprehensive API endpoints
- **Robust error handling** and security measures

## 🌐 Live Demo
- **Web Interface**: Visit the deployed URL for the interactive chat interface
- **API Documentation**: `/docs` for full API reference
- **API Endpoints**: `/api` for endpoint information

## 🏗️ Architecture Overview

### **Core Components**
- **Frontend**: Modern web UI (`static/index.html`) with real-time chat
- **Backend**: FastAPI application (`main.py`) with RESTful endpoints
- **Chatbot Engine**: `chatbot/agent.py` (stateful, multi-turn agent)
- **RAG System**: `chatbot/rag.py` (FAISS + Google Gemini embeddings)
- **Calculator Tool**: `chatbot/calculator.py` (arithmetic operations)
- **Outlet Database**: `database/outlets_db.py` (SQLite + Text2SQL)
- **Data Management**: `scripts/` for data ingestion

### **Key Features**
- **Multi-turn Conversations**: Maintains context across chat sessions
- **Intelligent Tool Selection**: Automatically chooses calculator, products, or outlets
- **Product Search**: AI-powered product recommendations with RAG
- **Outlet Information**: Natural language queries about ZUS Coffee locations
- **Real-time Chat**: Web interface with typing indicators and smooth UX

---

## ⚡️ Quick Start

### 1. **Clone & Setup**
```bash
git clone <your-repo-url>
cd chatbot_assessment
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
pip install -r requirements.txt
```

### 2. **Environment Variables**
Set your Google Gemini API key:
```bash
# Create .env file or set environment variable
export GEMINI_API_KEY=your-gemini-api-key
```

### 3. **Run the Application**
```bash
python main.py
```

### 4. **Access the Interface**
- **Web UI**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Interactive CLI**: `python chatbot_interactive.py`

---

## 🧩 Project Structure
```
chatbot_assessment/
├── main.py                  # FastAPI application with web UI
├── static/
│   └── index.html          # Modern web chat interface
├── chatbot/
│   ├── agent.py            # Main chatbot agent with tool integration
│   ├── rag.py              # RAG system (FAISS + Google Gemini)
│   └── calculator.py       # Calculator tool
├── database/
│   └── outlets_db.py       # Outlets database + Text2SQL converter
├── scripts/
│   ├── ingest_outlets.py   # Outlet data ingestion
│   └── ingest_products.py  # Product data ingestion
├── data/
│   ├── outlets.db          # SQLite database
│   └── products/           # Product data files
├── tests/
│   └── test_agent.py       # Comprehensive tests
├── chatbot_interactive.py  # Command-line interface
├── render.yaml            # Render deployment configuration
└── requirements.txt       # Python dependencies
```

---

## 🌐 API Endpoints

### **Core Endpoints**
- **GET /** - Web chat interface
- **POST /chat** - Chat with the AI agent
- **GET /products** - Product search with RAG
- **GET /outlets** - Outlet information queries
- **GET /calc** - Calculator operations

### **Utility Endpoints**
- **GET /health** - Health check
- **GET /docs** - Interactive API documentation
- **GET /api** - API information
- **GET /chat/state** - Current conversation state
- **POST /chat/reset** - Reset conversation

---

## 🚀 Deployment

### **Render.com (Recommended)**
1. Connect your GitHub repository to Render
2. Set environment variable: `GEMINI_API_KEY`
3. Deploy automatically on push
4. Get a public URL to share with others

### **Other Platforms**
- **Railway.app**: $5/month credit, excellent performance
- **Replit**: Free tier with instant deployment
- **Fly.io**: Free tier with global deployment
- **Vercel**: Free tier (may have size limitations)

---

## 🧪 Testing

### **Run Tests**
```bash
python -m pytest tests/ -v
```

### **Interactive Testing**
```bash
python chatbot_interactive.py
```

### **Example Queries**
- "What is 15 plus 27?"
- "Show me coffee cups"
- "Are there outlets in Petaling Jaya?"
- "What time does SS2 outlet open?"

---

## 🔧 Configuration

### **Environment Variables**
- `GEMINI_API_KEY`: Required for AI features (chat and embeddings)

### **Database**
- SQLite database with 8 sample ZUS Coffee outlets
- Product data from ZUS Coffee drinkware catalog

### **AI Models**
- **Chat**: Google Gemini 2.0 Flash
- **Embeddings**: Google Gemini embedding-001
- **Vector Store**: FAISS for fast similarity search

---

## 📝 Features

### **Chatbot Capabilities**
- ✅ Multi-turn conversations with context preservation
- ✅ Intent detection and entity extraction
- ✅ Tool integration (calculator, products, outlets)
- ✅ Error handling and fallback responses
- ✅ Conversation state management

### **Product Search**
- ✅ RAG-powered product recommendations
- ✅ AI-generated summaries
- ✅ Vector similarity search
- ✅ Natural language queries

### **Outlet Information**
- ✅ Text2SQL conversion
- ✅ Location-based queries
- ✅ Service-based filtering
- ✅ Operating hours information

### **Web Interface**
- ✅ Modern, responsive design
- ✅ Real-time chat experience
- ✅ Typing indicators
- ✅ Example query suggestions
- ✅ Mobile-friendly layout

---

## 🤝 Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

---

## 📄 License
This project is part of an AI Chatbot Engineer assessment.

---

## 🆘 Support
For issues or questions:
1. Check the API documentation at `/docs`
2. Review the test files for usage examples
3. Check the health endpoint at `/health`
