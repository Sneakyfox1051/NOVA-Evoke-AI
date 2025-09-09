#!/usr/bin/env python3
"""
Streamlit entry point for NOVA. Launches the Streamlit app properly.
"""

import subprocess
import sys
import os

def main():
    """Launch the Streamlit app."""
    print("🚀 Starting NOVA Assistant...")
    print("The app will open in your browser at http://localhost:8501")
    print("Press Ctrl+C to stop the server.\n")
    
    try:
        # Launch Streamlit with the app
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
            "--server.port", "8501",
            "--server.address", "localhost",
            "--browser.gatherUsageStats", "false"
        ])
    except KeyboardInterrupt:
        print("\n👋 NOVA Assistant stopped. Goodbye!")
    except Exception as e:
        print(f"❌ Error running Streamlit: {e}")

if __name__ == "__main__":
    main()

