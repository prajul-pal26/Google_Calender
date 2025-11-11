#!/usr/bin/env python3
"""
Google Calendar Pause/Resume Manager Launcher
Starts both the FastAPI server and Streamlit UI
"""

import subprocess
import time
import sys
import os
from pathlib import Path

def check_port_in_use(port):
    """Check if a port is already in use"""
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def start_api_server():
    """Start the FastAPI server"""
    print("🚀 Starting FastAPI server...")
    try:
        # Start the API server in background
        process = subprocess.Popen([
            sys.executable, "app.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a bit for server to start
        time.sleep(3)
        
        # Check if server is running
        if check_port_in_use(8000):
            print("✅ FastAPI server started successfully on http://localhost:8000")
            return process
        else:
            print("❌ Failed to start FastAPI server")
            return None
            
    except Exception as e:
        print(f"❌ Error starting FastAPI server: {e}")
        return None

def start_streamlit():
    """Start the Streamlit UI"""
    print("🎨 Starting Streamlit UI...")
    try:
        # Check if streamlit is installed
        try:
            import streamlit
            print(f"✅ Streamlit version {streamlit.__version__} found")
        except ImportError:
            print("❌ Streamlit not installed. Installing...")
            install_process = subprocess.Popen([
                sys.executable, "-m", "pip", "install", "streamlit"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            install_process.communicate()
            
            # Try importing again
            try:
                import streamlit
                print(f"✅ Streamlit installed successfully (version {streamlit.__version__})")
            except ImportError:
                print("❌ Failed to install Streamlit")
                return None
        
        # Start Streamlit with detailed output
        print("🚀 Launching Streamlit server...")
        process = subprocess.Popen([
            sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
            "--server.port", "8501", "--server.headless", "true"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Wait a bit for Streamlit to start
        time.sleep(5)
        
        # Check if Streamlit is running
        if check_port_in_use(8501):
            print("✅ Streamlit UI started successfully on http://localhost:8501")
            print("🌐 Open your browser and go to: http://localhost:8501")
            return process
        else:
            print("❌ Failed to start Streamlit UI")
            # Get error output
            stdout, stderr = process.communicate()
            if stderr:
                print(f"Error output: {stderr}")
            return None
            
    except Exception as e:
        print(f"❌ Error starting Streamlit UI: {e}")
        return None

def main():
    """Main launcher function"""
    print("📅 Google Calendar Pause/Resume Manager Launcher")
    print("=" * 50)
    
    # Check if required files exist
    required_files = ["app.py", "streamlit_app.py", "utils.py", "config.py"]
    missing_files = [f for f in required_files if not Path(f).exists()]
    
    if missing_files:
        print(f"❌ Missing required files: {', '.join(missing_files)}")
        print("Please make sure all required files are in the current directory.")
        return
    
    # Check if all required packages are installed
    print("🔍 Checking required packages...")
    required_packages = ["fastapi", "uvicorn", "streamlit", "requests", "google-api-python-client"]
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package} is installed")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} is missing")
    
    if missing_packages:
        print(f"\n📦 Installing missing packages: {', '.join(missing_packages)}")
        try:
            subprocess.run([
                sys.executable, "-m", "pip", "install"
            ] + missing_packages, check=True)
            print("✅ All packages installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install packages: {e}")
            print("Please run: pip install -r requirements.txt")
            return
    
    # Check if service account file exists
    if not Path("service_account.json").exists():
        print("⚠️ Warning: service_account.json not found")
        print("Please make sure you have a valid Google Calendar service account file.")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            return
    
    # Start API server
    api_process = start_api_server()
    if not api_process:
        print("❌ Cannot start without API server. Exiting.")
        return
    
    # Start Streamlit UI
    streamlit_process = start_streamlit()
    if not streamlit_process:
        print("\n❌ Failed to start Streamlit UI.")
        print("🔧 Troubleshooting steps:")
        print("1. Make sure you have internet connection")
        print("2. Try installing manually: pip install streamlit")
        print("3. Try starting manually: streamlit run streamlit_app.py")
        print("4. You can still use the API directly at http://localhost:8000")
        print("5. Check the error messages above for more details")
        
        # Ask if user wants to continue with API only
        response = input("\nContinue with API only? (y/n): ")
        if response.lower() != 'y':
            return
    else:
        print("\n🎉 Both services started successfully!")
        print("📱 Open your browser and go to: http://localhost:8501")
        print("🔧 API documentation: http://localhost:8000/docs")
        print("📖 For UI help, read UI_GUIDE.md")
    
    print("\n" + "=" * 50)
    print("Press Ctrl+C to stop all services")
    
    try:
        # Keep the script running
        while True:
            time.sleep(1)
            
            # Check if processes are still running
            if api_process.poll() is not None:
                print("❌ API server stopped unexpectedly")
                break
                
            if streamlit_process and streamlit_process.poll() is not None:
                print("❌ Streamlit UI stopped unexpectedly")
                break
                
    except KeyboardInterrupt:
        print("\n🛑 Stopping services...")
        
        # Stop processes
        if api_process:
            api_process.terminate()
            print("✅ API server stopped")
            
        if streamlit_process:
            streamlit_process.terminate()
            print("✅ Streamlit UI stopped")
        
        print("👋 Goodbye!")

if __name__ == "__main__":
    main()