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
        assert "SS2" in response2 or "SS 2" in response2
        assert agent.memory.outlet == "ss 2"
        assert agent.memory.current_state == ConversationState.OUTLET_CONFIRMED
        
        # Step 3: Ask about time again (should remember context)
        response3 = agent.respond("What time does it open?")
        assert "SS2" in response3 or "SS 2" in response3
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
        assert "SS2" in response or "SS 2" in response  # Should still work with direct outlet query
        
        # User asks about time without specifying outlet
        response = agent.respond("What time does it open?")
        assert "which outlet" in response.lower() or "specify" in response.lower()
    
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
        assert "SS2" in response or "SS 2" in response
    
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
    
    def test_calculator_tool_integration_success(self, agent):
        """
        Test Case 6: Tool Integration - Calculator success scenario
        """
        response = agent.respond("What is 5 plus 3?")
        assert "The answer is 8" in response
    
    def test_calculator_tool_integration_failure(self, agent):
        """
        Test Case 7: Tool Integration - Calculator failure scenarios
        """
        # Test division by zero
        response = agent.respond("What is 10 divided by 0?")
        assert "error" in response.lower() or "couldn't" in response.lower()
        
        # Test invalid operation
        response = agent.respond("What is 5 power 3?")
        assert "not sure" in response.lower() or "couldn't" in response.lower()
    
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
        assert "not sure" in response.lower() or "couldn't" in response.lower()
    
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
        # Note: conversation_history is preserved for debugging purposes
    
    def test_multiple_outlet_locations(self, agent):
        """
        Test Case 11: Multiple Locations - Test different outlet locations
        """
        # Test Petaling Jaya outlets
        response = agent.respond("Is there an outlet in Petaling Jaya?")
        assert "Petaling Jaya" in response
        
        # Test Kuala Lumpur outlets
        response = agent.respond("Is there an outlet in Kuala Lumpur?")
        assert "Kuala Lumpur" in response or "KL" in response
    
    def test_outlet_name_normalization(self, agent):
        """
        Test Case 12: Outlet Name Normalization - Test various outlet name formats
        """
        # Test SS 2 variations
        response1 = agent.respond("What time does SS 2 open?")
        response2 = agent.respond("What time does ss2 open?")
        assert "SS2" in response1 or "SS 2" in response1
        assert "SS2" in response2 or "SS 2" in response2
    
    def test_greeting_handling(self, agent):
        """
        Test Case 13: Greeting - Test greeting intent handling
        """
        response = agent.respond("Hello!")
        assert "hello" in response.lower() or "assistant" in response.lower()
        
        response = agent.respond("Hi there")
        assert "hello" in response.lower() or "assistant" in response.lower()
    
    @patch('chatbot.rag.enhanced_rag.query_products')
    def test_product_search_integration(self, mock_query_products, agent):
        """
        Test Case 14: Product Search - Test RAG integration
        """
        # Mock successful product search
        mock_query_products.return_value = "Here are some coffee cups available..."
        
        response = agent.respond("Show me coffee cups")
        assert "coffee cups" in response.lower()
        
        # Verify RAG was called
        mock_query_products.assert_called_once_with("Show me coffee cups")
    
    def test_conversation_history_tracking(self, agent):
        """
        Test Case 15: Conversation History - Test history tracking
        """
        # Make some interactions
        agent.respond("Hello")
        agent.respond("What is 5 plus 3?")
        agent.respond("Is there an outlet in KL?")
        
        # Verify history is tracked
        assert len(agent.memory.conversation_history) == 3
        
        # Verify history structure
        for interaction in agent.memory.conversation_history:
            assert "user_input" in interaction
            assert "bot_response" in interaction
            assert "intent" in interaction
            assert "timestamp" in interaction
    
    def test_confidence_scoring(self, agent):
        """
        Test Case 16: Confidence Scoring - Test confidence levels
        """
        # Test high confidence intents
        intent, confidence = agent.detect_intent("What is 5 plus 3?")
        assert confidence > 0.8
        
        intent, confidence = agent.detect_intent("Hello there!")
        assert confidence > 0.8
        
        # Test lower confidence intents
        intent, confidence = agent.detect_intent("Random text here")
        assert confidence == 0.0
    
    def test_get_conversation_state(self, agent):
        """
        Test Case 17: State Retrieval - Test state access
        """
        # Set up some state
        agent.respond("Is there an outlet in Petaling Jaya?")
        
        # Get state
        state = agent.get_conversation_state()
        
        # Verify state structure
        assert "location" in state
        assert "outlet" in state
        assert "current_state" in state
        assert "conversation_history" in state
        assert "confidence_score" in state 