#!/usr/bin/env python3
"""
Simple Streamlit UI Runner
Alternative way to start the web interface
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    print("🎨 Google Calendar UI Runner")
    print("=" * 40)
    
    # Check if streamlit_app.py exists
    if not Path("streamlit_app.py").exists():
        print("❌ streamlit_app.py not found!")
        print("Make sure you're in the correct directory.")
        return
    
    # Check if API server is running
    try:
        import requests
        response = requests.get("http://localhost:8000/", timeout=5)
        if response.status_code == 200:
            print("✅ API server is running on http://localhost:8000")
        else:
            print("⚠️ API server responded but might have issues")
    except:
        print("❌ API server is not running!")
        print("Please start the API server first:")
        print("   python app.py")
        print("\nOr use the full launcher:")
        print("   python start.py")
        return
    
    # Start Streamlit
    print("🚀 Starting Streamlit UI...")
    try:
        # Run streamlit directly
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
            "--server.port", "8501",
            "--server.headless", "false"  # Show browser
        ], check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start Streamlit: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure streamlit is installed: pip install streamlit")
        print("2. Try running manually: streamlit run streamlit_app.py")
        print("3. Check if port 8501 is available")
        
    except KeyboardInterrupt:
        print("\n👋 Streamlit UI stopped")

if __name__ == "__main__":
    main()