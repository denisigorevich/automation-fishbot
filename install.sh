#!/bin/bash

# Fishbot Installation Script for Linux
# This script sets up the environment and installs dependencies

echo "========================================"
echo "Fishbot - Educational Installation"
echo "========================================"
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "🐍 Python version: $python_version"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "📦 Installing pip..."
    sudo apt-get update
    sudo apt-get install -y python3-pip
fi

# Install system dependencies
echo "📦 Installing system dependencies..."
sudo apt-get update
sudo apt-get install -y \
    portaudio19-dev \
    python3-tk \
    python3-dev \
    scrot \
    alsa-utils \
    libasound2-dev

# Create virtual environment (optional but recommended)
echo "🔧 Setting up virtual environment..."
if ! command -v python3-venv &> /dev/null; then
    sudo apt-get install -y python3-venv
fi

python3 -m venv fishbot_env
source fishbot_env/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install Python dependencies
echo "📦 Installing Python packages..."
pip install -r requirements.txt

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p templates
mkdir -p logs

# Set permissions
echo "🔒 Setting permissions..."
chmod +x main.py
chmod +x setup_detector.py

echo ""
echo "✅ Installation completed successfully!"
echo ""
echo "🚀 To run the fishbot:"
echo "   1. Activate virtual environment: source fishbot_env/bin/activate"
echo "   2. Run setup first: python3 setup_detector.py"
echo "   3. Run the bot: python3 main.py"
echo ""
echo "⚠️  Remember: This is for educational purposes only!"
echo "    Use responsibly and respect game terms of service."
echo ""