from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from pydantic import SecretStr
import os
import logging

# Set up logging
logger = logging.getLogger(__name__)

# Load environment variables
api_key = os.getenv("GEMINI_API_KEY")
if not api_key or not isinstance(api_key, str):
    raise EnvironmentError("Missing required environment variable: GEMINI_API_KEY")

class EnhancedProductRAG:
    def __init__(self, data_file: str = "data/products/zus_drinkware.txt"):
        """
        Initializes the EnhancedProductRAG system, including setting up the embedding model,
        the language model (LLM), and the vector store for document indexing.
        """
        self.data_file = data_file
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=SecretStr(str(api_key)),
        )
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            api_key=SecretStr(str(api_key)),
            temperature=0.7
        )
        self.vectorstore = None
        self.load_products_index()

    def load_products_index(self):
        """Main method to load and index product data into the vector store."""
        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                content = f.read()
            splitter = CharacterTextSplitter(chunk_size=300, chunk_overlap=50)
            chunks = splitter.split_text(content)
            documents = [Document(page_content=chunk) for chunk in chunks]
            self.vectorstore = FAISS.from_documents(documents, self.embeddings)
            logger.info(f"Product index loaded with {len(documents)} chunks")
        except Exception as e:
            logger.error(f"Error loading product index: {e}")

    def search_products(self, query: str, k: int = 3) -> list:
        """Search for relevant products using the FAISS vector store."""
        try:
            if not self.vectorstore:
                logger.warning("Vector store not available. Returning empty results.")
                return []
            
            results = self.vectorstore.similarity_search(query, k=k)
            return results
        except Exception as e:
            logger.error(f"Error searching products: {e}")
            return []

    def generate_summary(self, query: str, search_results: list) -> str:
        """Generate a summary of search results using the LLM."""
        try:
            if not search_results:
                return "Sorry, I couldn't find any products matching your query."
            
            context = "\n\n".join([doc.page_content for doc in search_results])
            prompt = f"""
            User Query: {query}

            Relevant Product Information:
            {context}

            Please provide a helpful summary of the products that match the user's query. 
            Include key details like product names, prices, colors, and features.
            Make it conversational and helpful for a customer.
            """
            
            response = self.llm.invoke(prompt)
            if hasattr(response, 'content'):
                return str(response.content)
            elif isinstance(response, str):
                return response
            elif isinstance(response, list):
                return "\n".join(str(item) for item in response)
            else:
                return str(response)
            
        except Exception as e:
            logger.error(f"Error generating summary: {e}")
            return "Here's what I found:\n\n" + "\n\n".join([doc.page_content for doc in search_results])

    def query_products(self, user_query: str) -> str:
        """Main method to query products with AI summary."""
        try:
            if not user_query or not user_query.strip():
                return "Sorry, I couldn't find anything relevant."
            
            search_results = self.search_products(user_query, k=3)
            
            if not search_results:
                return "Sorry, I couldn't find any products matching your query. Please try different keywords."
            
            summary = self.generate_summary(user_query, search_results)
            return summary
            
        except Exception as e:
            logger.error(f"Error in product query: {e}")
            return "I'm having trouble searching for products right now. Please try again later."

# Initialize the enhanced RAG system only if we can
try:
    enhanced_rag = EnhancedProductRAG()
except Exception as e:
    logger.warning(f"Could not initialize enhanced RAG system: {e}")
    enhanced_rag = None
