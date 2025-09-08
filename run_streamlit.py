#!/usr/bin/env python3
"""
Simple script to run the NOVA Streamlit app with proper configuration.
"""

import subprocess
import sys
import os

def main():
    """Run the Streamlit app with optimal settings."""
    
    print("🚀 Starting NOVA Assistant Streamlit App...")
    print("=" * 50)
    
    # Check if streamlit is installed
    try:
        import streamlit
        print(f"✅ Streamlit version: {streamlit.__version__}")
    except ImportError:
        print("❌ Streamlit not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit>=1.28.0"])
        print("✅ Streamlit installed successfully!")
    
    # Check if other dependencies are available
    try:
        from nova_client import NovaClient
        print("✅ NOVA client ready")
    except ImportError as e:
        print(f"❌ Missing dependencies: {e}")
        print("Installing requirements...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed!")
    
    # Run streamlit app
    print("\n🌐 Launching Streamlit app...")
    print("The app will open in your default web browser.")
    print("Press Ctrl+C to stop the server.\n")
    
    try:
        # Run streamlit with optimal settings
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
            "--server.port", "8501",
            "--server.address", "localhost",
            "--browser.gatherUsageStats", "false",
            "--theme.base", "light"
        ])
    except KeyboardInterrupt:
        print("\n👋 NOVA Assistant app stopped. Goodbye!")
    except Exception as e:
        print(f"❌ Error running Streamlit: {e}")

if __name__ == "__main__":
    main()

