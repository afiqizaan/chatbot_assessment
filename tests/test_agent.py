import pytest
import httpx
from unittest.mock import patch, MagicMock
from chatbot.agent import EnhancedChatbotAgent, Intent, ConversationState

class TestEnhancedChatbotAgent:
    
    @pytest.fixture
    def agent(self):
        """Create a fresh agent instance for each test"""
        return EnhancedChatbotAgent()
    
    def test_happy_flow_sequential_conversation(self, agent):
        """
        Test Case 1: Happy Path - Complete sequential conversation flow
        Objective: Keep track of at least three related turns
        """
        # Step 1: Ask about outlet in Petaling Jaya
        response1 = agent.respond("Is there an outlet in Petaling Jaya?")
        assert "outlets in Petaling Jaya" in response1
        assert agent.memory.location == "petaling jaya"
        assert agent.memory.current_state == ConversationState.LOCATION_CONFIRMED
        
        # Step 2: Specify outlet (SS 2)
        response2 = agent.respond("SS 2, what's the opening time?")
        assert "SS 2 outlet opens at 9:00AM" in response2
        assert agent.memory.outlet == "ss 2"
        assert agent.memory.current_state == ConversationState.OUTLET_CONFIRMED
        
        # Step 3: Ask about time again (should remember context)
        response3 = agent.respond("What time does it open?")
        assert "SS 2 outlet opens at 9:00AM" in response3
        assert agent.memory.current_state == ConversationState.COMPLETED
        
        # Verify conversation history
        assert len(agent.memory.conversation_history) == 3
        assert agent.memory.conversation_history[0]["intent"] == "outlet_inquiry"
        assert agent.memory.conversation_history[1]["intent"] == "time_inquiry"
        assert agent.memory.conversation_history[2]["intent"] == "time_inquiry"
    
    def test_interrupted_flow_handling(self, agent):
        """
        Test Case 2: Unhappy Path - Interrupted conversation flow
        Objective: Handle cases where user skips steps or provides incomplete information
        """
        # User skips location and asks directly about outlet
        response = agent.respond("SS 2")
        assert "not sure" in response.lower() or "outlets" in response.lower()
        assert agent.memory.location is None
        assert agent.memory.outlet is None
        
        # User asks about time without specifying outlet
        response = agent.respond("What time does it open?")
        assert "which outlet" in response.lower()
        assert agent.memory.outlet is None
    
    def test_state_management_persistence(self, agent):
        """
        Test Case 3: State Management - Verify state persistence across turns
        """
        # Set up conversation state
        agent.respond("Is there an outlet in Petaling Jaya?")
        agent.respond("SS 2")
        
        # Verify state is maintained
        assert agent.memory.location == "petaling jaya"
        assert agent.memory.outlet == "ss 2"
        assert agent.memory.current_state == ConversationState.OUTLET_CONFIRMED
        
        # Ask about time - should use stored state
        response = agent.respond("What time does it open?")
        assert "SS 2 outlet opens at 9:00AM" in response
    
    def test_intent_detection_accuracy(self, agent):
        """
        Test Case 4: Intent Detection - Verify accurate intent classification
        """
        # Test calculation intent
        intent, confidence = agent.detect_intent("What is 5 plus 3?")
        assert intent == Intent.CALCULATION
        assert confidence > 0.8
        
        # Test time inquiry intent
        intent, confidence = agent.detect_intent("What time does SS 2 open?")
        assert intent == Intent.TIME_INQUIRY
        assert confidence > 0.7
        
        # Test outlet inquiry intent
        intent, confidence = agent.detect_intent("Is there an outlet in Kuala Lumpur?")
        assert intent == Intent.OUTLET_INQUIRY
        assert confidence > 0.8
        
        # Test greeting intent
        intent, confidence = agent.detect_intent("Hello there!")
        assert intent == Intent.GREETING
        assert confidence > 0.8
        
        # Test unknown intent
        intent, confidence = agent.detect_intent("Random gibberish text")
        assert intent == Intent.UNKNOWN
        assert confidence == 0.0
    
    def test_entity_extraction(self, agent):
        """
        Test Case 5: Entity Extraction - Verify accurate entity recognition
        """
        # Test location extraction
        entities = agent.extract_entities("Is there an outlet in Petaling Jaya?")
        assert entities["location"] == "petaling jaya"
        
        # Test outlet extraction
        entities = agent.extract_entities("What time does SS 2 open?")
        assert entities["outlet"] == "ss 2"
        
        # Test number extraction for calculations
        entities = agent.extract_entities("What is 15 plus 27?")
        assert entities["numbers"] == [15.0, 27.0]
        
        # Test multiple entities
        entities = agent.extract_entities("What time does Damansara outlet open?")
        assert entities["outlet"] == "damansara"
    
    @patch('httpx.get')
    def test_calculator_tool_integration_success(self, mock_get, agent):
        """
        Test Case 6: Tool Integration - Calculator API success scenario
        """
        # Mock successful API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": 8.0}
        mock_get.return_value = mock_response
        
        response = agent.respond("What is 5 plus 3?")
        assert "The answer is 8.0" in response
        
        # Verify API was called correctly
        mock_get.assert_called_once_with(
            "http://127.0.0.1:8000/calc",
            params={"a": 5.0, "b": 3.0, "op": "add"},
            timeout=5.0
        )
    
    @patch('httpx.get')
    def test_calculator_tool_integration_failure(self, mock_get, agent):
        """
        Test Case 7: Tool Integration - Calculator API failure scenarios
        """
        # Test API timeout
        mock_get.side_effect = httpx.TimeoutException("Request timed out")
        response = agent.respond("What is 5 plus 3?")
        assert "taking too long" in response
        
        # Test API connection error
        mock_get.side_effect = httpx.RequestError("Connection failed")
        response = agent.respond("What is 10 minus 4?")
        assert "currently unavailable" in response
        
        # Test API error response
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.return_value = {"detail": "Invalid operation"}
        mock_get.return_value = mock_response
        
        response = agent.respond("What is 10 divided by 0?")
        assert "Invalid operation" in response or "currently unavailable" in response
    
    def test_robustness_malicious_input(self, agent):
        """
        Test Case 8: Robustness - Handle malicious or invalid inputs
        """
        # Test empty input
        response = agent.respond("")
        assert "didn't catch that" in response
        
        # Test very long input
        long_input = "x" * 10000
        response = agent.respond(long_input)
        assert response is not None  # Should not crash
        
        # Test special characters
        response = agent.respond("!@#$%^&*()")
        assert "not sure how to help" in response
        
        # Test SQL injection attempt
        response = agent.respond("'; DROP TABLE users; --")
        assert response is not None  # Should not crash
    
    def test_robustness_missing_data(self, agent):
        """
        Test Case 9: Robustness - Handle missing or incomplete data
        """
        # Test calculation with insufficient numbers
        response = agent.respond("What is 5?")
        assert "need two numbers" in response or "not sure how to help" in response
        
        # Test calculation with invalid operation
        response = agent.respond("What is 5 power 3?")
        assert "couldn't understand the operation" in response
        
        # Test outlet inquiry for non-existent location
        response = agent.respond("Is there an outlet in Mars?")
        assert "don't have information" in response
        
        # Test time inquiry for non-existent outlet
        response = agent.respond("What time does Mars outlet open?")
        assert "don't have information" in response
    
    def test_conversation_reset(self, agent):
        """
        Test Case 10: State Management - Test conversation reset functionality
        """
        # Set up some conversation state
        agent.respond("Is there an outlet in Petaling Jaya?")
        agent.respond("SS 2")
        
        # Verify state is set
        assert agent.memory.location is not None
        assert agent.memory.outlet is not None
        
        # Reset conversation
        agent.reset_conversation()
        
        # Verify state is cleared
        assert agent.memory.location is None
        assert agent.memory.outlet is None
        assert agent.memory.current_state == ConversationState.INITIAL
        assert len(agent.memory.conversation_history) == 0
    
    def test_multiple_outlet_locations(self, agent):
        """
        Test Case 11: Multiple Locations - Test different outlet locations
        """
        # Test Petaling Jaya outlets
        response = agent.respond("Is there an outlet in Petaling Jaya?")
        assert "SS 2" in response
        assert "Damansara" in response
        
        # Test Kuala Lumpur outlet
        response = agent.respond("Is there an outlet in Kuala Lumpur?")
        assert "Bukit Bintang" in response
        
        # Test Subang outlet
        response = agent.respond("Is there an outlet in Subang?")
        assert "Subang" in response
    
    def test_outlet_name_normalization(self, agent):
        """
        Test Case 12: Outlet Name Normalization - Test various outlet name formats
        """
        # Test SS 2 variations
        response1 = agent.respond("What time does SS 2 open?")
        response2 = agent.respond("What time does ss2 open?")
        assert "9:00AM" in response1
        assert "9:00AM" in response2
        
        # Test Damansara
        response = agent.respond("What time does Damansara open?")
        assert "8:30AM" in response
        
        # Test Bukit Bintang
        response = agent.respond("What time does Bukit Bintang open?")
        assert "10:00AM" in response
    
    def test_greeting_handling(self, agent):
        """
        Test Case 13: Greeting Intent - Test greeting responses
        """
        greetings = ["Hello", "Hi there", "Hey", "Good morning", "Good afternoon"]
        
        for greeting in greetings:
            response = agent.respond(greeting)
            assert "Hello" in response or "assistant" in response
            assert "help" in response
    
    @patch('chatbot.rag.enhanced_rag.query_products')
    def test_product_search_integration(self, mock_query_products, agent):
        """
        Test Case 14: Product Search - Test RAG integration
        """
        # Mock product search response
        mock_query_products.return_value = "Here's what I found:\n\nZUS All Day Cup 500ml - RM79.00"
        
        response = agent.respond("I want to buy a coffee cup")
        assert "ZUS All Day Cup" in response
        
        # Test product search error handling
        mock_query_products.side_effect = Exception("Search failed")
        response = agent.respond("Show me drinkware products")
        assert "having trouble searching" in response
    
    def test_conversation_history_tracking(self, agent):
        """
        Test Case 15: Conversation History - Test conversation tracking
        """
        # Perform a conversation
        agent.respond("Hello")
        agent.respond("Is there an outlet in Petaling Jaya?")
        agent.respond("SS 2")
        
        # Verify conversation history
        history = agent.memory.conversation_history
        assert len(history) == 3
        
        # Check first interaction
        assert history[0]["intent"] == "greeting"
        assert "Hello" in history[0]["user_input"]
        
        # Check second interaction
        assert history[1]["intent"] == "outlet_inquiry"
        assert "Petaling Jaya" in history[1]["user_input"]
        
        # Check third interaction
        assert history[2]["intent"] == "time_inquiry"
        assert "SS 2" in history[2]["user_input"]
        
        # Verify timestamps are present
        for interaction in history:
            assert "timestamp" in interaction
    
    def test_confidence_scoring(self, agent):
        """
        Test Case 16: Confidence Scoring - Test confidence score updates
        """
        # Initial state
        assert agent.memory.confidence_score == 0.0
        
        # After location confirmation
        agent.respond("Is there an outlet in Petaling Jaya?")
        assert agent.memory.confidence_score == 0.8
        
        # After outlet confirmation
        agent.respond("SS 2")
        assert agent.memory.confidence_score == 0.9
        
        # After completion
        agent.respond("What time does it open?")
        assert agent.memory.confidence_score == 0.95
    
    def test_get_conversation_state(self, agent):
        """
        Test Case 17: State Inspection - Test state retrieval for debugging
        """
        # Set up some state
        agent.respond("Is there an outlet in Petaling Jaya?")
        agent.respond("SS 2")
        
        # Get state
        state = agent.get_conversation_state()
        
        # Verify state structure
        assert "location" in state
        assert "outlet" in state
        assert "current_state" in state
        assert "conversation_history" in state
        assert "confidence_score" in state
        
        # Verify state values
        assert state["location"] == "petaling jaya"
        assert state["outlet"] == "ss 2"
        assert state["confidence_score"] == 0.9 