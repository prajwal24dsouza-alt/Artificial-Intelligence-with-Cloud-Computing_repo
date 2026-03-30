#!/bin/bash

# Setup script for Break the AI - LLM Adversarial Testing Suite
# This script installs dependencies and prepares the environment

set -e

echo "=========================================="
echo "Break the AI - Setup Script"
echo "=========================================="
echo ""

# Check Python
echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8 or higher."
    exit 1
fi
python_version=$(python3 --version | awk '{print $2}')
echo "✓ Python $python_version found"
echo ""

# Check Ollama
echo "Checking Ollama installation..."
if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama not found. Please install Ollama from https://ollama.ai"
    exit 1
fi
echo "✓ Ollama found at $(which ollama)"
echo ""

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Check/Download model
echo "Checking for Mistral model..."
if ollama list | grep -q "mistral"; then
    echo "✓ Mistral model is already downloaded"
else
    echo "⏳ Downloading Mistral model (this may take several minutes)..."
    ollama pull mistral
    echo "✓ Mistral model downloaded"
fi
echo ""

# Verify Ollama is running
echo "Checking if Ollama server is running..."
if curl -s http://localhost:11434/api/generate -X POST -d '{"model":"mistral","prompt":"test"}' > /dev/null 2>&1; then
    echo "✓ Ollama server is running and responsive"
else
    echo "⚠️ Ollama server is not responding. Start it with: ollama serve"
fi
echo ""

echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. If Ollama is not running, start it in a separate terminal:"
echo "   $ ollama serve"
echo ""
echo "2. Run the test suite:"
echo "   $ python run_tests.py"
echo ""
echo "3. Analyze results with Jupyter:"
echo "   $ jupyter notebook analysis.ipynb"
echo ""
