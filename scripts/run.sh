#!/bin/bash

# PDF Knowledge Graph Generator Run Script
# This script starts the application with proper configuration

set -e

echo "🧠 Starting PDF Knowledge Graph Generator..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run setup.sh first."
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Check if dependencies are installed
if ! python -c "import streamlit" &> /dev/null; then
    echo "❌ Dependencies not installed. Please run setup.sh first."
    exit 1
fi

# Check if spaCy model is installed
if ! python -c "import spacy; spacy.load('en_core_web_sm')" &> /dev/null; then
    echo "❌ spaCy model not found. Please run setup.sh first."
    exit 1
fi

echo "✅ All dependencies verified"

# Create necessary directories if they don't exist
mkdir -p data
mkdir -p uploads
mkdir -p logs

# Set environment variables
export STREAMLIT_SERVER_PORT=8501
export STREAMLIT_SERVER_ADDRESS=0.0.0.0
export STREAMLIT_SERVER_HEADLESS=true

echo "Starting Streamlit application..."
echo "Application will be available at: http://localhost:8501"
echo "🛑 Press Ctrl+C to stop the application"
echo ""

# Start the application
streamlit run app.py --server.port=8501 --server.address=0.0.0.0
