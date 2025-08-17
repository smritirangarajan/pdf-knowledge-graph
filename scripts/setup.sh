#!/bin/bash

# PDF Knowledge Graph Generator Setup Script
# This script automates the setup process for the application

set -e

echo "🧠 Setting up PDF Knowledge Graph Generator..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
REQUIRED_VERSION="3.8"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "❌ Python version $PYTHON_VERSION is not supported. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python $PYTHON_VERSION detected"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Download spaCy model
echo "🤖 Downloading spaCy model..."
python -m spacy download en_core_web_sm

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p data
mkdir -p uploads
mkdir -p logs

# Set permissions
echo "🔐 Setting permissions..."
chmod +x scripts/*.sh

echo "✅ Setup completed successfully!"
echo ""
echo "To run the application:"
echo "   source venv/bin/activate"
echo "   streamlit run app.py"
echo ""
echo "🐳 To run with Docker:"
echo "   docker-compose up --build"
echo ""
echo "📖 For more information, see README.md"
