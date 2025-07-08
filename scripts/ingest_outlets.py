#!/usr/bin/env python3
"""
Outlet Data Ingestion Script
Initializes the SQL database with ZUS outlet data
"""

import os
import sys
import logging
from pathlib import Path

# Add the parent directory to the path so we can import our modules
sys.path.append(str(Path(__file__).parent.parent))

from database.outlets_db import OutletsDatabase, Text2SQLConverter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def ingest_outlets():
    """Initialize the outlets database"""
    try:
        logger.info("Starting outlet data ingestion...")
        
        # Initialize the database (this will create tables and insert sample data)
        db = OutletsDatabase()
        
        # Test the Text2SQL functionality
        text2sql = Text2SQLConverter(db)
        
        # Test some queries
        test_queries = [
            "Show me all outlets in Petaling Jaya",
            "Which outlets have drive-thru?",
            "Find outlets in Kuala Lumpur"
        ]
        
        for query in test_queries:
            results = text2sql.query_outlets(query)
            logger.info(f"Query: '{query}' -> Found {len(results)} outlets")
        
        logger.info("Outlet ingestion completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Error during outlet ingestion: {e}")
        return False

def main():
    """Main function"""
    print("=== ZUS Outlet Data Ingestion ===")
    print("This script will initialize the SQL database with outlet data.")
    print()
    
    success = ingest_outlets()
    
    if success:
        print("✅ Outlet ingestion completed successfully!")
        print("The Text2SQL system is now ready to answer outlet queries.")
    else:
        print("❌ Outlet ingestion failed!")
        print("Please check the logs for more details.")
        sys.exit(1)

if __name__ == "__main__":
    main() 