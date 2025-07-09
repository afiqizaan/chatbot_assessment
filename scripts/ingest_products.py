#!/usr/bin/env python3
"""
Product Data Ingestion Script
Ingests ZUS product data into the vector store for RAG system
"""

import os
import sys
import logging
from pathlib import Path

# Add the parent directory to the path so we can import our modules
sys.path.append(str(Path(__file__).parent.parent))

from chatbot.rag import EnhancedProductRAG

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def ingest_products():
    """Ingest product data into the vector store"""
    try:
        logger.info("Starting product data ingestion...")
        
        # Initialize the enhanced RAG system
        rag = EnhancedProductRAG()
        
        # Test the ingestion by doing a sample query
        test_query = "coffee cup"
        result = rag.query_products(test_query)
        
        logger.info("Product ingestion completed successfully!")
        logger.info(f"Sample query result: {result[:200]}...")
        
        return True
        
    except Exception as e:
        logger.error(f"Error during product ingestion: {e}")
        return False

def main():
    """Main function"""
    print("=== ZUS Product Data Ingestion ===")
    print("This script will ingest product data into the vector store.")
    print()
    
    success = ingest_products()
    
    if success:
        print("✅ Product ingestion completed successfully!")
        print("The RAG system is now ready to answer product queries.")
    else:
        print("❌ Product ingestion failed!")
        print("Please check the logs for more details.")
        sys.exit(1)

if __name__ == "__main__":
    main() 