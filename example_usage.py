#!/usr/bin/env python3
"""
Example usage of the NOVA OpenAI Assistant API integration.
This file demonstrates various ways to interact with NOVA.
"""

from nova_client import NovaClient
import json

def main():
    """Main function demonstrating NOVA usage."""
    
    print("🤖 NOVA OpenAI Assistant Integration Demo")
    print("=" * 50)
    
    try:
        # Initialize NOVA client
        print("Initializing NOVA client...")
        nova = NovaClient()
        print("✅ NOVA client initialized successfully!")
        print()
        
        # Health check
        print("🔍 Performing health check...")
        health = nova.health_check()
        print(f"Status: {health['status']}")
        print(f"API Connected: {health['api_connected']}")
        if health['status'] == 'healthy':
            print(f"Test Response: {health['test_response']}")
        print()
        
        # Example 1: Simple question
        print("💬 Example 1: Simple Question")
        print("-" * 30)
        question = "What is artificial intelligence?"
        print(f"User: {question}")
        response = nova.send_message(question)
        print(f"NOVA: {response}")
        print()
        
        # Example 2: Creative request
        print("🎨 Example 2: Creative Request")
        print("-" * 30)
        creative_request = "Write a short poem about programming"
        print(f"User: {creative_request}")
        response = nova.send_message(creative_request, temperature=0.9)
        print(f"NOVA: {response}")
        print()
        
        # Example 3: Conversation with context
        print("💭 Example 3: Conversation with Context")
        print("-" * 30)
        conversation = [
            {"role": "user", "content": "I'm learning Python programming"},
            {"role": "assistant", "content": "That's great! Python is an excellent language to learn. What specific aspect of Python are you working on?"},
            {"role": "user", "content": "I'm struggling with object-oriented programming concepts. Can you explain classes and objects?"}
        ]
        
        print("Conversation History:")
        for msg in conversation:
            print(f"{msg['role'].title()}: {msg['content']}")
        
        response = nova.send_conversation(conversation)
        print(f"NOVA: {response}")
        print()
        
        # Example 4: Different models
        print("🔧 Example 4: Using Different Models")
        print("-" * 30)
        models_to_try = ["gpt-3.5-turbo", "gpt-4"]
        question = "Explain quantum computing in simple terms"
        
        for model in models_to_try:
            print(f"Using model: {model}")
            response = nova.send_message(question, model=model, temperature=0.3)
            print(f"NOVA ({model}): {response[:200]}...")
            print()
        
        # Example 5: Available models
        print("📋 Example 5: Available Models")
        print("-" * 30)
        models = nova.get_available_models()
        print(f"Total models available: {len(models)}")
        print("First 10 models:")
        for i, model in enumerate(models[:10], 1):
            print(f"{i:2d}. {model}")
        print()
        
        print("🎉 Demo completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during demo: {str(e)}")
        print("Please check your API key and internet connection.")

def interactive_mode():
    """Interactive mode for chatting with NOVA."""
    print("🤖 NOVA Interactive Mode")
    print("Type 'quit' to exit, 'help' for commands")
    print("=" * 40)
    
    try:
        nova = NovaClient()
        
        while True:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("NOVA: Goodbye! 👋")
                break
            elif user_input.lower() == 'help':
                print("NOVA: Available commands:")
                print("- quit/exit/bye: Exit the program")
                print("- help: Show this help message")
                print("- Any other text: Chat with NOVA")
                continue
            elif not user_input:
                continue
            
            print("NOVA: ", end="", flush=True)
            response = nova.send_message(user_input)
            print(response)
            
    except KeyboardInterrupt:
        print("\n\nNOVA: Goodbye! 👋")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        interactive_mode()
    else:
        main()

