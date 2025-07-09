import re
import json
import httpx
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from enum import Enum
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Intent(Enum):
    OUTLET_INQUIRY = "outlet_inquiry"
    TIME_INQUIRY = "time_inquiry"
    CALCULATION = "calculation"
    PRODUCT_SEARCH = "product_search"
    GREETING = "greeting"
    UNKNOWN = "unknown"

class ConversationState(Enum):
    INITIAL = "initial"
    LOCATION_CONFIRMED = "location_confirmed"
    OUTLET_CONFIRMED = "outlet_confirmed"
    COMPLETED = "completed"

@dataclass
class ConversationMemory:
    """Enhanced memory structure for conversation state"""
    location: Optional[str] = None
    outlet: Optional[str] = None
    current_state: ConversationState = ConversationState.INITIAL
    conversation_history: Optional[List[Dict[str, str]]] = None
    confidence_score: float = 0.0
    
    def __post_init__(self):
        if self.conversation_history is None:
            self.conversation_history = []
    
    def add_interaction(self, user_input: str, bot_response: str, intent: str):
        """Add interaction to conversation history"""
        from datetime import datetime
        if self.conversation_history is None:
            self.conversation_history = []
        self.conversation_history.append({
            "user_input": user_input,
            "bot_response": bot_response,
            "intent": intent,
            "timestamp": str(datetime.now())
        })
    
    def reset(self):
        """Reset conversation state"""
        self.location = None
        self.outlet = None
        self.current_state = ConversationState.INITIAL
        self.confidence_score = 0.0

class EnhancedChatbotAgent:
    """
    Enhanced Chatbot Agent with advanced state management, intent parsing,
    and robust error handling for Mindhive AI Chatbot Engineer assessment.
    """
    
    def __init__(self):
        self.memory = ConversationMemory()
        self.outlet_data = {
            "SS 2": {"opening_time": "9:00AM", "location": "Petaling Jaya"},
            "Damansara": {"opening_time": "8:30AM", "location": "Petaling Jaya"},
            "Bukit Bintang": {"opening_time": "10:00AM", "location": "Kuala Lumpur"},
            "Subang": {"opening_time": "9:30AM", "location": "Subang"},
            "Puchong": {"opening_time": "8:00AM", "location": "Puchong"}
        }
        self.supported_locations = ["petaling jaya", "kl", "kuala lumpur", "subang", "puchong"]
        self.supported_outlets = [
            "ss 2", "ss2", "damansara", "bukit bintang", "subang", "puchong",
            "1 utama", "one utama", "klcc", "mid valley", "ioi mall"
        ]
        
    def detect_intent(self, query: str) -> Tuple[Intent, float]:
        """
        Advanced intent detection with confidence scoring
        """
        query_lower = query.lower()
        intent_scores = {}
        
        # Mathematical operations
        math_keywords = ["add", "plus", "sum", "subtract", "minus", "multiply", "times", "divide", "divided", "calculate"]
        if any(keyword in query_lower for keyword in math_keywords):
            intent_scores[Intent.CALCULATION] = 0.9
        
        # Time inquiries
        time_keywords = ["open", "time", "when", "hours", "schedule"]
        if any(keyword in query_lower for keyword in time_keywords):
            intent_scores[Intent.TIME_INQUIRY] = 0.8
        
        # Outlet inquiries
        outlet_keywords = ["outlet", "branch", "store", "location", "where"]
        if any(keyword in query_lower for keyword in outlet_keywords):
            intent_scores[Intent.OUTLET_INQUIRY] = 0.85
        
        # Product search
        product_keywords = ["product", "item", "buy", "price", "available", "show me", "coffee", "cup", "mug", "drinkware"]
        if any(keyword in query_lower for keyword in product_keywords):
            intent_scores[Intent.PRODUCT_SEARCH] = 0.8
        
        # Greeting
        greeting_keywords = ["hello", "hi", "hey", "good morning", "good afternoon"]
        if any(keyword in query_lower for keyword in greeting_keywords):
            intent_scores[Intent.GREETING] = 0.9
        
        # Check for outlet names (SS 2, Damansara, etc.) - these indicate time inquiry
        outlet_names = ["ss 2", "ss2", "damansara", "bukit bintang", "subang", "puchong"]
        if any(outlet in query_lower for outlet in outlet_names):
            intent_scores[Intent.TIME_INQUIRY] = 0.9
        
        if not intent_scores:
            return Intent.UNKNOWN, 0.0
        
        # Return highest confidence intent
        best_intent = max(intent_scores.items(), key=lambda x: x[1])
        return best_intent[0], best_intent[1]
    
    def extract_entities(self, query: str) -> Dict[str, Any]:
        """
        Extract entities from user query
        """
        query_lower = query.lower()
        entities: Dict[str, Any] = {"_query": query}  # Store original query for reference
        
        # Extract location
        for location in self.supported_locations:
            if location in query_lower:
                entities["location"] = location
                break
        
        # Extract outlet
        for outlet in self.supported_outlets:
            if outlet in query_lower:
                entities["outlet"] = outlet
                break
        
        # Extract numbers for calculations
        numbers = re.findall(r"[-+]?\d*\.?\d+", query)
        if numbers:
            entities["numbers"] = [float(num) for num in numbers]
        
        return entities
    
    def update_state(self, intent: Intent, entities: Dict[str, Any]) -> None:
        """
        Update conversation state based on intent and entities
        """
        if intent == Intent.OUTLET_INQUIRY and "location" in entities:
            self.memory.location = entities["location"]
            self.memory.current_state = ConversationState.LOCATION_CONFIRMED
            self.memory.confidence_score = 0.8
        
        elif intent == Intent.TIME_INQUIRY and "outlet" in entities:
            self.memory.outlet = entities["outlet"]
            self.memory.current_state = ConversationState.OUTLET_CONFIRMED
            self.memory.confidence_score = 0.9
        
        elif intent == Intent.TIME_INQUIRY and self.memory.outlet:
            # User asking about time for already known outlet
            self.memory.current_state = ConversationState.COMPLETED
            self.memory.confidence_score = 0.95
        
        # Handle case where user mentions outlet name directly
        elif intent == Intent.TIME_INQUIRY and "outlet" not in entities:
            # Check if query contains outlet names
            query_lower = entities.get("_query", "").lower()
            outlet_names = ["ss 2", "ss2", "damansara", "bukit bintang", "subang", "puchong"]
            for outlet in outlet_names:
                if outlet in query_lower:
                    self.memory.outlet = outlet
                    self.memory.current_state = ConversationState.OUTLET_CONFIRMED
                    self.memory.confidence_score = 0.9
                    break
    
    def handle_calculation(self, query: str) -> str:
        """
        Enhanced calculation handling with robust error handling
        """
        try:
            # Extract numbers
            numbers = re.findall(r"[-+]?\d*\.?\d+", query)
            if len(numbers) < 2:
                return "I need two numbers to calculate. Try something like 'What is 4 plus 5?'"
            
            a, b = float(numbers[0]), float(numbers[1])
            
            # Detect operation with improved pattern matching
            query_lower = query.lower()
            if any(op in query_lower for op in ["add", "plus", "sum", "+"]):
                op = "add"
            elif any(op in query_lower for op in ["subtract", "minus", "-"]):
                op = "sub"
            elif any(op in query_lower for op in ["multiply", "times", "*"]):
                op = "mul"
            elif any(op in query_lower for op in ["divide", "divided", "/"]):
                op = "div"
            else:
                return "I couldn't understand the operation. Try 'add', 'subtract', 'multiply', or 'divide'."
            
            # Use the local calculator function instead of API call
            try:
                from chatbot.calculator import calculate
                result = calculate(a, b, op)
                return f"The answer is {result}."
            except Exception as e:
                logger.error(f"Calculator error: {e}")
                return "Sorry, I couldn't calculate that. Please try again."
                
        except ValueError as e:
            logger.error(f"Value error in calculation: {e}")
            return "I couldn't understand the numbers. Please provide valid numbers."
        except Exception as e:
            logger.error(f"Unexpected error in calculation handling: {e}")
            return "Something went wrong. Please try again."
    
    def handle_outlet_inquiry(self, entities: Dict[str, Any]) -> str:
        """
        Handle outlet-related inquiries with state management
        """
        try:
            # Import here to avoid circular imports
            from database.outlets_db import text2sql
            
            if "location" in entities:
                location = entities["location"]
                self.memory.location = location
                self.memory.current_state = ConversationState.LOCATION_CONFIRMED
                
                # Query the database for outlets in the location
                query = f"outlets in {location}"
                results = text2sql.query_outlets(query)
                
                if results:
                    outlet_names = [outlet.get('name', 'Unknown') for outlet in results]
                    outlet_list = ", ".join(outlet_names)
                    return f"Yes! We have outlets in {location.title()}: {outlet_list}. Which one are you interested in?"
                else:
                    return f"I don't have information about outlets in {location.title()}. Please try another location."
            
            return "Which area are you interested in? We have outlets in Petaling Jaya, Kuala Lumpur, Subang, and Puchong."
        except Exception as e:
            logger.error(f"Outlet inquiry error: {e}")
            return "I'm having trouble accessing outlet information right now. Please try again later."
    
    def handle_time_inquiry(self, entities: Dict[str, Any]) -> str:
        """
        Handle time-related inquiries with state management
        """
        try:
            # Import here to avoid circular imports
            from database.outlets_db import text2sql
            
            # Check if outlet is provided in current query
            if "outlet" in entities:
                outlet = entities["outlet"]
                self.memory.outlet = outlet
                self.memory.current_state = ConversationState.OUTLET_CONFIRMED
            
            # Use outlet from memory if not in current query
            outlet = self.memory.outlet or entities.get("outlet")
            
            if outlet:
                # Query the database for outlet information
                query = f"opening hours for {outlet} outlet"
                results = text2sql.query_outlets(query)
                
                if results:
                    outlet_info = results[0]
                    opening_hours = outlet_info.get('opening_hours', 'Not available')
                    outlet_name = outlet_info.get('name', outlet)
                    return f"The {outlet_name} outlet opening hours: {opening_hours}."
                else:
                    return f"I don't have information about the {outlet} outlet. Please specify a valid outlet."
            else:
                return "Which outlet are you asking about? Please specify the outlet name."
        except Exception as e:
            logger.error(f"Time inquiry error: {e}")
            return "I'm having trouble accessing outlet information right now. Please try again later."
    
    def _normalize_outlet_name(self, outlet: str) -> str:
        """
        Normalize outlet names for consistent matching
        """
        outlet_lower = outlet.lower()
        if outlet_lower in ["ss 2", "ss2"]:
            return "SS 2"
        elif outlet_lower == "damansara":
            return "Damansara"
        elif outlet_lower == "bukit bintang":
            return "Bukit Bintang"
        elif outlet_lower == "subang":
            return "Subang"
        elif outlet_lower == "puchong":
            return "Puchong"
        elif outlet_lower in ["1 utama", "one utama"]:
            return "1 Utama"
        elif outlet_lower == "klcc":
            return "KLCC"
        elif outlet_lower == "mid valley":
            return "Mid Valley"
        elif outlet_lower == "ioi mall":
            return "IOI Mall Puchong"
        return outlet.title()
    
    def handle_product_search(self, query: str) -> str:
        """
        Handle product search using enhanced RAG system
        """
        try:
            # Import here to avoid circular imports
            from chatbot.rag import enhanced_rag
            return enhanced_rag.query_products(query)
        except Exception as e:
            logger.error(f"Product search error: {e}")
            return "Sorry, I'm having trouble searching for products right now. Please try again later."
    
    def handle_greeting(self) -> str:
        """
        Handle greeting intents
        """
        return "Hello! I'm your AI assistant. I can help you with outlet information, calculations, and product searches. How can I help you today?"
    
    def respond(self, query: str) -> str:
        """
        Main response handler with comprehensive error handling and state management
        """
        try:
            # Input validation
            if not query or not query.strip():
                return "I didn't catch that. Could you please repeat your question?"
            
            # Detect intent and extract entities
            intent, confidence = self.detect_intent(query)
            entities = self.extract_entities(query)
            
            # Update conversation state
            self.update_state(intent, entities)
            
            # Generate response based on intent
            if intent == Intent.CALCULATION:
                response = self.handle_calculation(query)
            elif intent == Intent.OUTLET_INQUIRY:
                response = self.handle_outlet_inquiry(entities)
            elif intent == Intent.TIME_INQUIRY:
                response = self.handle_time_inquiry(entities)
            elif intent == Intent.PRODUCT_SEARCH:
                response = self.handle_product_search(query)
            elif intent == Intent.GREETING:
                response = self.handle_greeting()
            else:
                response = "I'm not sure how to help with that. I can assist with outlet information, calculations, and product searches. What would you like to know?"
            
            # Add interaction to memory
            self.memory.add_interaction(query, response, intent.value)
            
            return response
            
        except Exception as e:
            logger.error(f"Unexpected error in respond method: {e}")
            return "I'm experiencing some technical difficulties. Please try again in a moment."
    
    def get_conversation_state(self) -> Dict[str, Any]:
        """
        Get current conversation state for debugging/testing
        """
        return asdict(self.memory)
    
    def reset_conversation(self) -> None:
        """
        Reset conversation state
        """
        self.memory.reset()