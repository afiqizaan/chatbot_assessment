import sqlite3
import json
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class Outlet:
    id: int
    name: str
    location: str
    address: str
    opening_hours: str
    phone: str
    services: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class OutletsDatabase:
    def __init__(self, db_path: str = "data/outlets.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with outlets table and sample data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create outlets table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS outlets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                location TEXT NOT NULL,
                address TEXT NOT NULL,
                opening_hours TEXT NOT NULL,
                phone TEXT,
                services TEXT,
                latitude REAL,
                longitude REAL
            )
        ''')
        
        # Insert sample ZUS outlets data
        sample_outlets = [
            (1, "ZUS Coffee SS2", "Petaling Jaya", "No. 1, Jalan SS2/24, SS2, 47300 Petaling Jaya", "7:00 AM - 11:00 PM", "+603-1234-5678", "Coffee, Food, WiFi", 3.1077, 101.6067),
            (2, "ZUS Coffee Damansara", "Petaling Jaya", "Damansara Uptown, 47400 Petaling Jaya", "8:30 AM - 10:30 PM", "+603-1234-5679", "Coffee, Food, WiFi, Drive-thru", 3.1429, 101.6177),
            (3, "ZUS Coffee Bukit Bintang", "Kuala Lumpur", "Lot 10, Bukit Bintang, 55100 Kuala Lumpur", "10:00 AM - 12:00 AM", "+603-1234-5680", "Coffee, Food, WiFi, 24/7", 3.1429, 101.7117),
            (4, "ZUS Coffee Subang", "Subang Jaya", "Subang Parade, 47500 Subang Jaya", "9:30 AM - 10:00 PM", "+603-1234-5681", "Coffee, Food, WiFi", 3.0567, 101.5857),
            (5, "ZUS Coffee Puchong", "Puchong", "IOI Mall Puchong, 47100 Puchong", "8:00 AM - 11:00 PM", "+603-1234-5682", "Coffee, Food, WiFi, Delivery", 2.9927, 101.6177),
            (6, "ZUS Coffee KLCC", "Kuala Lumpur", "Suria KLCC, 50088 Kuala Lumpur", "9:00 AM - 10:00 PM", "+603-1234-5683", "Coffee, Food, WiFi, Premium", 3.1577, 101.7117),
            (7, "ZUS Coffee Mid Valley", "Kuala Lumpur", "Mid Valley Megamall, 59200 Kuala Lumpur", "10:00 AM - 10:00 PM", "+603-1234-5684", "Coffee, Food, WiFi", 3.1177, 101.6767),
            (8, "ZUS Coffee 1 Utama", "Petaling Jaya", "1 Utama Shopping Centre, 47800 Petaling Jaya", "10:00 AM - 10:00 PM", "+603-1234-5685", "Coffee, Food, WiFi, Drive-thru", 3.1429, 101.6177)
        ]
        
        cursor.execute('DELETE FROM outlets')  # Clear existing data
        cursor.executemany('''
            INSERT INTO outlets (id, name, location, address, opening_hours, phone, services, latitude, longitude)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', sample_outlets)
        
        conn.commit()
        conn.close()
        logger.info(f"Database initialized with {len(sample_outlets)} outlets")
    
    def execute_query(self, sql_query: str) -> List[Dict[str, Any]]:
        """Execute a SQL query and return results as list of dictionaries"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row  # Enable column access by name
            cursor = conn.cursor()
            
            cursor.execute(sql_query)
            rows = cursor.fetchall()
            
            results = []
            for row in rows:
                results.append(dict(row))
            
            conn.close()
            return results
            
        except Exception as e:
            logger.error(f"Database query error: {e}")
            raise e
    
    def get_all_outlets(self) -> List[Dict[str, Any]]:
        """Get all outlets"""
        return self.execute_query("SELECT * FROM outlets")
    
    def get_outlets_by_location(self, location: str) -> List[Dict[str, Any]]:
        """Get outlets by location"""
        location_lower = location.lower()
        return self.execute_query(f"""
            SELECT * FROM outlets 
            WHERE LOWER(location) LIKE '%{location_lower}%'
        """)
    
    def get_outlets_by_service(self, service: str) -> List[Dict[str, Any]]:
        """Get outlets that offer a specific service"""
        service_lower = service.lower()
        return self.execute_query(f"""
            SELECT * FROM outlets 
            WHERE LOWER(services) LIKE '%{service_lower}%'
        """)
    
    def get_outlets_open_at(self, time: str) -> List[Dict[str, Any]]:
        """Get outlets open at a specific time (simplified logic)"""
        return self.execute_query(f"""
            SELECT * FROM outlets 
            WHERE opening_hours LIKE '%{time}%'
        """)

class Text2SQLConverter:
    """Convert natural language queries to SQL"""
    
    def __init__(self, db: OutletsDatabase):
        self.db = db
        self.table_schema = {
            "outlets": {
                "columns": ["id", "name", "location", "address", "opening_hours", "phone", "services", "latitude", "longitude"],
                "description": "ZUS Coffee outlets with location, hours, and services information"
            }
        }
    
    def convert_to_sql(self, nl_query: str) -> str:
        """
        Convert natural language query to SQL
        This is a simplified implementation - in production, you'd use an LLM
        """
        query_lower = nl_query.lower()
        
        # Simple pattern matching for common queries
        if "all outlets" in query_lower or "list outlets" in query_lower:
            return "SELECT * FROM outlets"
        
        elif "petaling jaya" in query_lower or "pj" in query_lower:
            return "SELECT * FROM outlets WHERE LOWER(location) LIKE '%petaling jaya%'"
        
        elif "kuala lumpur" in query_lower or "kl" in query_lower:
            return "SELECT * FROM outlets WHERE LOWER(location) LIKE '%kuala lumpur%'"
        
        elif "subang" in query_lower:
            return "SELECT * FROM outlets WHERE LOWER(location) LIKE '%subang%'"
        
        elif "puchong" in query_lower:
            return "SELECT * FROM outlets WHERE LOWER(location) LIKE '%puchong%'"
        
        elif "drive-thru" in query_lower or "drive thru" in query_lower:
            return "SELECT * FROM outlets WHERE LOWER(services) LIKE '%drive%'"
        
        elif "24/7" in query_lower or "24 hours" in query_lower:
            return "SELECT * FROM outlets WHERE LOWER(services) LIKE '%24%'"
        
        elif "wifi" in query_lower:
            return "SELECT * FROM outlets WHERE LOWER(services) LIKE '%wifi%'"
        
        elif "delivery" in query_lower:
            return "SELECT * FROM outlets WHERE LOWER(services) LIKE '%delivery%'"
        
        elif "ss2" in query_lower or "ss 2" in query_lower:
            return "SELECT * FROM outlets WHERE LOWER(name) LIKE '%ss2%' OR LOWER(name) LIKE '%ss 2%'"
        
        elif "damansara" in query_lower:
            return "SELECT * FROM outlets WHERE LOWER(name) LIKE '%damansara%'"
        
        elif "bukit bintang" in query_lower:
            return "SELECT * FROM outlets WHERE LOWER(name) LIKE '%bukit bintang%'"
        
        else:
            # Default to all outlets if no specific pattern matches
            return "SELECT * FROM outlets"
    
    def query_outlets(self, nl_query: str) -> List[Dict[str, Any]]:
        """Convert NL query to SQL and execute it"""
        try:
            sql_query = self.convert_to_sql(nl_query)
            logger.info(f"NL Query: '{nl_query}' -> SQL: '{sql_query}'")
            return self.db.execute_query(sql_query)
        except Exception as e:
            logger.error(f"Text2SQL error: {e}")
            return []

# Initialize database
outlets_db = OutletsDatabase()
text2sql = Text2SQLConverter(outlets_db) 