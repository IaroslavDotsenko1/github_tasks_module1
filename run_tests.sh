#!/bin/bash

# Test script for Mergington High School Activities API
# This script runs all tests with coverage reporting

echo "Running FastAPI tests with coverage..."
echo "======================================"

# Change to the project directory
cd "$(dirname "$0")"

# Use the virtual environment python
PYTHON_PATH="./.venv/bin/python"

# Check if virtual environment exists
if [ ! -f "$PYTHON_PATH" ]; then
    echo "Virtual environment not found at $PYTHON_PATH"
    echo "Using system Python..."
    PYTHON_PATH="python"
fi

# Run tests with coverage
$PYTHON_PATH -m pytest tests/ --cov=src --cov-report=term-missing --cov-report=html -v

echo ""
echo "Tests completed!"
echo "Coverage report saved to htmlcov/index.html"