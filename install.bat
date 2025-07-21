@echo off
REM WoW Fishbot Installation Script for Windows
REM This script sets up the environment and installs dependencies

echo ========================================
echo WoW Fishbot - Educational Installation
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH.
    echo Please install Python 3.8 or higher from https://python.org
    pause
    exit /b 1
)

REM Display Python version
echo 🐍 Python version:
python --version

REM Check if pip is available
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ pip is not available. Please ensure Python is properly installed.
    pause
    exit /b 1
)

REM Create virtual environment (recommended)
echo 🔧 Setting up virtual environment...
python -m venv fishbot_env

REM Activate virtual environment
echo 🔓 Activating virtual environment...
call fishbot_env\Scripts\activate.bat

REM Upgrade pip
echo ⬆️ Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo 📦 Installing Python packages...
pip install -r requirements.txt

REM Create necessary directories
echo 📁 Creating directories...
if not exist "templates" mkdir templates
if not exist "logs" mkdir logs

echo.
echo ✅ Installation completed successfully!
echo.
echo 🚀 To run the fishbot:
echo    1. Activate virtual environment: fishbot_env\Scripts\activate.bat
echo    2. Run setup first: python setup_detector.py
echo    3. Run the bot: python main.py
echo.
echo ⚠️  Remember: This is for educational purposes only!
echo    Use responsibly and respect game terms of service.
echo.

pause