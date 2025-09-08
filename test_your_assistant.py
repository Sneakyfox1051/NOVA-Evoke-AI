#!/usr/bin/env python3
"""
Test script specifically for your NOVA assistant with ID: asst_XTd5ExJ9KUTLyrFkzkzPZa2f
"""

from nova_client import NovaClient
import json

def test_your_nova_assistant():
    """Test your specific NOVA assistant."""
    print("🤖 Testing Your NOVA Assistant")
    print("=" * 50)
    print(f"Assistant ID: asst_XTd5ExJ9KUTLyrFkzkzPZa2f")
    print(f"Model: gpt-4o-mini")
    print("=" * 50)
    
    try:
        # Initialize NOVA client with your specific assistant
        nova = NovaClient()
        
        print("✅ NOVA client initialized successfully!")
        print(f"✅ Using your assistant ID: {nova.assistant_id}")
        
        # Get assistant information
        print("\n📋 Getting assistant information...")
        info = nova.get_assistant_info()
        if "error" not in info:
            print("✅ Assistant Information:")
            print(f"   Name: {info['name']}")
            print(f"   Model: {info['model']}")
            print(f"   Tools: {', '.join(info['tools'])}")
            print(f"   Created: {info['created_at']}")
        else:
            print(f"❌ Error getting assistant info: {info['error']}")
        
        # Test health check
        print("\n🏥 Running health check...")
        health = nova.health_check()
        if health['status'] == 'healthy':
            print("✅ Health check passed!")
            print(f"   API Connected: {health['api_connected']}")
            print(f"   Assistant ID: {health['assistant_id']}")
        else:
            print(f"❌ Health check failed: {health.get('error', 'Unknown error')}")
            return False
        
        # Test messages
        test_messages = [
            "Hello NOVA! How are you?",
            "Can you tell me a short joke?",
            "What's 2+2?",
            "Write a haiku about AI"
        ]
        
        print("\n💬 Testing conversation...")
        for i, message in enumerate(test_messages, 1):
            print(f"\n{i}. Testing: {message}")
            print("   Response:", end=" ")
            
            try:
                response = nova.send_message(message, use_assistant=True)
                print(response[:100] + "..." if len(response) > 100 else response)
            except Exception as e:
                print(f"❌ Error: {e}")
        
        print("\n🎉 All tests completed!")
        print("\nYour NOVA assistant is ready to use!")
        print("You can now run the Streamlit app:")
        print("  python run_streamlit.py")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Main function."""
    success = test_your_nova_assistant()
    
    if success:
        print("\n✅ Setup successful! Your assistant is working perfectly.")
    else:
        print("\n❌ Setup failed. Please check your API key and internet connection.")

if __name__ == "__main__":
    main()

