#!/usr/bin/env python3
"""
Streamlit entry point for NOVA.
Loads environment variables securely and launches the app.
"""

import os
import subprocess
import sys
from dotenv import load_dotenv

def main():
    """Load .env and launch the Streamlit app with the correct environment."""
    # Load environment variables from your .env file
    load_dotenv()
    print("✅ Environment variables from .env loaded.")

    # Get the API key from the loaded environment
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        print("❌ FATAL: OPENAI_API_KEY not found in .env file.")
        print("Please make sure your .env file is correct.")
        sys.exit(1) # Exit if the key isn't found

    # Create a copy of the current system's environment
    env = os.environ.copy()
    # Force the correct API key into this new environment
    env["OPENAI_API_KEY"] = api_key
    print("✅ API Key has been forced into the app's environment.")

    print("🚀 Starting NOVA Assistant...")
    try:
        # Run the streamlit app using the modified environment
        subprocess.run(
            [sys.executable, "-m", "streamlit", "run", "streamlit_app.py"],
            env=env, # This is the critical part
            check=True
        )
    except KeyboardInterrupt:
        print("\n👋 NOVA Assistant stopped. Goodbye!")
    except Exception as e:
        print(f"❌ Error running Streamlit: {e}")

if __name__ == "__main__":
    main()