#!/usr/bin/env python3
"""
Setup script to configure the OpenAI API key for NOVA.
This script helps you set up the API key in multiple ways.
"""

import os
import sys

def create_env_file():
    """Create a .env file template for the API key."""
    try:
        with open('.env', 'w') as f:
            f.write("# OpenAI API Configuration\n")
            f.write("OPENAI_API_KEY=your_api_key_here\n")
            f.write("OPENAI_ASSISTANT_ID=asst_XTd5ExJ9KUTLyrFkzkzPZa2f\n")
        print("✅ Created .env template file")
        print("📝 Please edit .env and add your actual API key")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False

def set_environment_variable():
    """Prompt user to set the environment variable manually."""
    print("🔑 To set your API key as an environment variable:")
    print("   Windows PowerShell: $env:OPENAI_API_KEY='your_key_here'")
    print("   Windows CMD: set OPENAI_API_KEY=your_key_here")
    print("   Linux/Mac: export OPENAI_API_KEY='your_key_here'")
    return True

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

