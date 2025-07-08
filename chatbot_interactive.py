#!/usr/bin/env python3
"""
Interactive Chatbot Testing Script
Run this to test the chatbot interactively
"""

from chatbot.agent import EnhancedChatbotAgent
import sys

def main():
    print("🤖 AI Chatbot Testing Interface")
    print("=" * 50)
    print("Type 'quit' to exit, 'help' for examples")
    print()
    
    # Initialize the chatbot
    try:
        agent = EnhancedChatbotAgent()
        print("✅ Chatbot initialized successfully!")
    except Exception as e:
        print(f"❌ Error initializing chatbot: {e}")
        return
    
    print("\n🎯 Try these example queries:")
    print("- 'Hello'")
    print("- 'What is 5 plus 3?'")
    print("- 'Is there an outlet in Petaling Jaya?'")
    print("- 'I want to buy a coffee cup'")
    print("- 'What time does SS 2 outlet open?'")
    print()
    
    # Interactive chat loop
    while True:
        try:
            # Get user input
            user_input = input("👤 You: ").strip()
            
            # Check for exit commands
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            if user_input.lower() == 'help':
                print("\n🎯 Example queries:")
                print("- 'Hello'")
                print("- 'What is 5 plus 3?'")
                print("- 'Is there an outlet in Petaling Jaya?'")
                print("- 'I want to buy a coffee cup'")
                print("- 'What time does SS 2 outlet open?'")
                print("- 'Show me all outlets'")
                print("- 'Calculate 10 times 5'")
                print()
                continue
            
            if not user_input:
                print("🤖 Please enter a message!")
                continue
            
            # Get chatbot response
            print("🤖 Bot: ", end="", flush=True)
            response = agent.respond(user_input)
            print(response)
            
            # Show conversation state (optional)
            if '--debug' in sys.argv:
                state = agent.get_conversation_state()
                print(f"🔍 Debug - History length: {len(state['conversation_history'])}")
            
            print()
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            print("Please try again.")

if __name__ == "__main__":
    main() 