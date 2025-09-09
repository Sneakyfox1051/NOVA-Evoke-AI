#!/usr/bin/env python3
"""
Setup script to configure the OpenAI API key for NOVA.
This script helps you set up the API key in multiple ways.
"""

import os
import sys

def create_env_file():
    """Create a .env file with the API key."""
    api_key = "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"
    
    try:
        with open('.env', 'w') as f:
            f.write(f"OPENAI_API_KEY={api_key}\n")
        print("✅ Created .env file with your API key")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False

def set_environment_variable():
    """Set the environment variable for the current session."""
    api_key = "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"
    
    try:
        os.environ['OPENAI_API_KEY'] = api_key
        print("✅ Set OPENAI_API_KEY environment variable for current session")
        return True
    except Exception as e:
        print(f"❌ Failed to set environment variable: {e}")
        return False

def test_nova_client():
    """Test if NOVA client can be initialized."""
    try:
        from nova_client import NovaClient
        client = NovaClient()
        print("✅ NOVA client initialized successfully!")
        
        # Test health check
        health = client.health_check()
        if health['status'] == 'healthy':
            print("✅ NOVA health check passed!")
            return True
        else:
            print(f"❌ NOVA health check failed: {health.get('error', 'Unknown error')}")
            return False
    except Exception as e:
        print(f"❌ Failed to initialize NOVA client: {e}")
        return False

def main():
    """Main setup function."""
    print("🔧 NOVA API Key Setup")
    print("=" * 40)
    
    # Try to create .env file
    print("\n1. Creating .env file...")
    create_env_file()
    
    # Set environment variable
    print("\n2. Setting environment variable...")
    set_environment_variable()
    
    # Test the setup
    print("\n3. Testing NOVA client...")
    if test_nova_client():
        print("\n🎉 Setup completed successfully!")
        print("You can now run the Streamlit app:")
        print("  python run_streamlit.py")
        print("  or")
        print("  streamlit run streamlit_app.py")
    else:
        print("\n❌ Setup failed. Please check your internet connection and API key.")
        print("\nAlternative setup methods:")
        print("1. Set environment variable manually:")
        print("   export OPENAI_API_KEY='your_api_key_here'")
        print("2. Or pass the API key directly when initializing NovaClient:")
        print("   nova = NovaClient(api_key='your_api_key_here')")

if __name__ == "__main__":
    main()

