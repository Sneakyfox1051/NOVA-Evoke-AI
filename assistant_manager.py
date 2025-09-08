#!/usr/bin/env python3
"""
Assistant Manager for NOVA - Helps you find and manage your OpenAI Assistants.
"""

from nova_client import NovaClient
import json

def list_all_assistants():
    """List all your OpenAI Assistants."""
    print("🔍 Finding your OpenAI Assistants...")
    print("=" * 50)
    
    try:
        nova = NovaClient()
        assistants = nova.list_assistants()
        
        if not assistants or "error" in assistants[0]:
            print("❌ No assistants found or error occurred:")
            if assistants:
                print(f"   {assistants[0]['error']}")
            return
        
        print(f"✅ Found {len(assistants)} assistant(s):\n")
        
        for i, assistant in enumerate(assistants, 1):
            print(f"{i}. {assistant['name']}")
            print(f"   ID: {assistant['id']}")
            print(f"   Model: {assistant['model']}")
            print(f"   Created: {assistant['created_at']}")
            print(f"   Instructions: {assistant['instructions']}")
            print("-" * 40)
        
        return assistants
        
    except Exception as e:
        print(f"❌ Error: {e}")

def find_nova_assistant():
    """Find and set up the NOVA assistant."""
    print("🤖 Looking for NOVA Assistant...")
    print("=" * 40)
    
    try:
        nova = NovaClient()
        assistants = nova.list_assistants()
        
        if not assistants or "error" in assistants[0]:
            print("❌ No assistants found.")
            return None
        
        # Look for NOVA assistant
        nova_assistant = None
        for assistant in assistants:
            if assistant['name'].lower() == 'nova':
                nova_assistant = assistant
                break
        
        if nova_assistant:
            print(f"✅ Found NOVA Assistant!")
            print(f"   ID: {nova_assistant['id']}")
            print(f"   Model: {nova_assistant['model']}")
            
            # Set it as the active assistant
            if nova.set_assistant_by_id(nova_assistant['id']):
                print("✅ NOVA Assistant is now active!")
                return nova_assistant['id']
            else:
                print("❌ Failed to set NOVA as active assistant.")
                return None
        else:
            print("❌ NOVA Assistant not found.")
            print("Available assistants:")
            for assistant in assistants:
                print(f"   - {assistant['name']} (ID: {assistant['id']})")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_assistant(assistant_id=None):
    """Test the assistant with a simple message."""
    print("🧪 Testing Assistant...")
    print("=" * 30)
    
    try:
        nova = NovaClient()
        
        if assistant_id:
            if not nova.set_assistant_by_id(assistant_id):
                print(f"❌ Failed to set assistant ID: {assistant_id}")
                return False
        
        # Test message
        test_message = "Hello! Can you tell me a short joke?"
        print(f"📤 Sending: {test_message}")
        
        response = nova.send_message(test_message, use_assistant=True)
        print(f"📥 Response: {response}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing assistant: {e}")
        return False

def main():
    """Main function for assistant management."""
    print("🤖 NOVA Assistant Manager")
    print("=" * 50)
    
    while True:
        print("\nChoose an option:")
        print("1. List all assistants")
        print("2. Find and set NOVA assistant")
        print("3. Test current assistant")
        print("4. Set specific assistant by ID")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == "1":
            list_all_assistants()
            
        elif choice == "2":
            assistant_id = find_nova_assistant()
            if assistant_id:
                print(f"\n🎉 NOVA Assistant is ready! ID: {assistant_id}")
                print("You can now use it in your Streamlit app.")
            
        elif choice == "3":
            test_assistant()
            
        elif choice == "4":
            assistant_id = input("Enter assistant ID: ").strip()
            if assistant_id:
                if test_assistant(assistant_id):
                    print("✅ Assistant is working!")
                else:
                    print("❌ Assistant test failed.")
            
        elif choice == "5":
            print("👋 Goodbye!")
            break
            
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

