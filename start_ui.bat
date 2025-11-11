@echo off
title Google Calendar UI Launcher

echo 📅 Google Calendar Pause/Resume Manager
echo =====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python first
    pause
    exit /b 1
)

REM Check if required files exist
if not exist "streamlit_app.py" (
    echo ❌ streamlit_app.py not found!
    echo Make sure you're in the correct directory.
    pause
    exit /b 1
)

if not exist "app.py" (
    echo ❌ app.py not found!
    echo Make sure you're in the correct directory.
    pause
    exit /b 1
)

echo 🚀 Starting API server...
start "API Server" cmd /k "python app.py"

echo ⏳ Waiting for API server to start...
timeout /t 3 /nobreak >nul

echo 🎨 Starting Streamlit UI...
python -m streamlit run streamlit_app.py --server.port 8501

echo.
echo 👋 UI stopped. API server is still running.
echo Close the API server window when done.
pause