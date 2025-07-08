# AI Chatbot Engineer Assessment

## 🚀 Project Overview
This project is a robust, production-ready multi-turn conversational AI chatbot. It features:
- State management and context awareness
- Agentic planning and tool integration
- Retrieval-augmented generation (RAG) for product search
- Custom API endpoints (FastAPI)
- Robust error handling and security

## 🏗️ Architecture Overview & Key Trade-offs

### **Architecture**
- **Entrypoint:** `main.py` (FastAPI app)
- **Chatbot Logic:** `chatbot/agent.py` (stateful, multi-turn agent)
- **RAG System:** `chatbot/rag.py` (FAISS + OpenAI embeddings)
- **Calculator Tool:** `chatbot/calculator.py` (arithmetic API)
- **Outlet Database:** `database/outlets_db.py` (SQLite + Text2SQL)
- **Data Ingestion:** `scripts/ingest_outlets.py`, `scripts/ingest_products.py`
- **Tests:** `tests/` (integration, unhappy flows)
- **Docs:** `docs/` (summaries, transcripts, strategy)

### **Key Trade-offs**
- **Simplicity vs. Extensibility:**
  - Modular code for easy extension (add new tools, endpoints, or data sources)
  - Single FastAPI app for all endpoints (simple, but can be split for microservices)
- **Performance vs. Cost:**
  - Uses OpenAI embeddings for RAG (high quality, but requires API key/quota)
  - FAISS for fast local vector search
- **Security vs. Usability:**
  - Strong input validation and error handling
  - User-friendly error messages (no technical leaks)
- **Testing:**
  - Comprehensive unhappy path and integration tests
  - Mocking for external APIs to ensure robustness

---

## ⚡️ Setup Instructions

### 1. **Clone the Repo & Install Dependencies**
```sh
# Clone the repo
# cd into the project directory
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
# source venv/bin/activate
pip install -r requirements.txt
```

### 2. **Set Environment Variables**
You need an OpenAI API key for product search (RAG):
```sh
# In your shell or .env file
export OPENAI_API_KEY=sk-...
```

### 3. **Ingest Data**
```sh
python scripts/ingest_outlets.py
python scripts/ingest_products.py
```

### 4. **Run the API Server**
```sh
python main.py
```
- Visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for the interactive API docs.

### 5. **Interactive Chatbot Testing**
```sh
python chatbot_interactive.py
```

---

## 🧩 **Key Files & Structure**
```
chatbot_assessment/
├── main.py                  # FastAPI entrypoint
├── chatbot/
│   ├── agent.py             # Main chatbot agent
│   ├── rag.py               # RAG system (FAISS + OpenAI)
│   └── calculator.py        # Calculator tool
├── database/
│   └── outlets_db.py        # Outlets DB + Text2SQL
├── scripts/
│   ├── ingest_outlets.py    # Ingest outlet data
│   └── ingest_products.py   # Ingest product data
├── tests/
│   └── test_agent.py        # Agent tests
├── docs/                    # Summaries, transcripts, strategy
├── data/products/           # Product data
├── chatbot_interactive.py   # Interactive CLI chatbot
└── requirements.txt         # Dependencies
```

---

## 🧪 **Testing**
Run all tests:
```sh
python -m pytest tests/ -v
```

---

## 🌐 **Endpoints & Example Usage**
- **POST /chat**: Chat with the bot
- **GET /calc**: Calculator tool
- **GET /products**: Product search (RAG)
- **GET /outlets**: Outlet info (Text2SQL)

See `/docs` for full API details and try out requests interactively.

---

## 📝 **Notes**
- For public demo, deploy to Render, Hugging Face Spaces, or Replit (see docs for details).
- For best results, ensure your OpenAI API key has quota.
- All code is modular and ready for extension or production deployment.
