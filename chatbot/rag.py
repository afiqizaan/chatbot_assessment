# chatbot/rag.py
from dotenv import load_dotenv
load_dotenv()

from langchain_openai import AzureOpenAIEmbeddings

from langchain_community.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from openai import OpenAI
import os
import logging

logger = logging.getLogger(__name__)

# Set your OpenAI key
openai_key = os.getenv("OPENAI_API_KEY")
openai_base = os.getenv("OPENAI_API_BASE")
openai_api_type = os.getenv("OPENAI_API_TYPE", "azure")
openai_api_version = os.getenv("OPENAI_API_VERSION")
openai_deployment_name = os.getenv("OPENAI_DEPLOYMENT_NAME")
openai_embedding_deployment_name = os.getenv("OPENAI_EMBEDDING_DEPLOYMENT_NAME")

class EnhancedProductRAG:
    def __init__(self, data_file: str = "data/products/zus_drinkware.txt"):
        self.data_file = data_file
        self.embeddings = None
        self.openai_client = None
        self.vectorstore = None
        
        # Initialize OpenAI components only if API key is available
        if openai_key:
            try:
                self.embeddings = AzureOpenAIEmbeddings(
                    azure_deployment=openai_embedding_deployment_name,
                    model="text-embedding-ada-002",  # or your Azure embedding model name
                    openai_api_type=openai_api_type,
                )
                self.openai_client = OpenAI(
                    api_key=openai_key,
                    base_url=openai_base,
                    default_headers={"api-key": openai_key}
                )
                self.load_products_index()
            except Exception as e:
                logger.warning(f"Could not initialize OpenAI components: {e}")
                self.embeddings = None
                self.openai_client = None
        else:
            logger.warning("OpenAI API key not found. RAG system will use fallback mode.")
    
    def load_products_index(self):
        """Load and index product data into vector store"""
        try:
            if not self.embeddings:
                logger.warning("Embeddings not available. Skipping vector store initialization.")
                return
                
            # Load and split the file
            with open(self.data_file, "r", encoding="utf-8") as f:
                content = f.read()

            splitter = CharacterTextSplitter(chunk_size=300, chunk_overlap=50)
            chunks = splitter.split_text(content)
            documents = [Document(page_content=chunk) for chunk in chunks]

            # Embed and store in FAISS
            self.vectorstore = FAISS.from_documents(documents, self.embeddings)
            logger.info(f"Product index loaded with {len(documents)} chunks")
            
        except Exception as e:
            logger.error(f"Error loading product index: {e}")
            # Don't raise the error, just log it
    
    def search_products(self, query: str, k: int = 3) -> list:
        """Search for relevant products"""
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
        """Generate AI summary of search results"""
        try:
            if not search_results:
                return "Sorry, I couldn't find any products matching your query."
            
            # If OpenAI is not available, fall back to simple concatenation
            if not self.openai_client:
                logger.warning("OpenAI client not available. Using fallback summary.")
                return "Here's what I found:\n\n" + "\n\n".join([doc.page_content for doc in search_results])
            
            # Prepare context from search results
            context = "\n\n".join([doc.page_content for doc in search_results])
            
            # Create prompt for summary
            prompt = f"""
            User Query: {query}
            
            Relevant Product Information:
            {context}
            
            Please provide a helpful summary of the products that match the user's query. 
            Include key details like product names, prices, colors, and features.
            Make it conversational and helpful for a customer.
            """
            
            # Generate summary using OpenAI API
            model_name = openai_deployment_name or "gpt-35-turbo"  # fallback if not set
            response = self.openai_client.chat.completions.create(
                model=model_name,  # Use Azure deployment name
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1
            )
            content = response.choices[0].message.content
            return content if content else "Sorry, I couldn't generate a summary at the moment."
            
        except Exception as e:
            logger.error(f"Error generating summary: {e}")
            # Fallback to simple concatenation
            return "Here's what I found:\n\n" + "\n\n".join([doc.page_content for doc in search_results])
    
    def query_products(self, user_query: str) -> str:
        """Main method to query products with AI summary"""
        try:
            # Input validation
            if not user_query or not user_query.strip():
                return "Sorry, I couldn't find anything relevant."
            
            # Search for relevant products
            search_results = self.search_products(user_query, k=3)
            
            if not search_results:
                return "Sorry, I couldn't find any products matching your query. Please try different keywords."
            
            # Generate AI summary
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