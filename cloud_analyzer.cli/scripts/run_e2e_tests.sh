#!/bin/bash
# Script to run end-to-end tests for cloud analyzer

set -e

echo "Running Cloud Analyzer End-to-End Tests"
echo "======================================"

# Set up test environment
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src:$(pwd)/../cloud_analyzer.common/src"

# Install test dependencies if needed
if ! python -c "import pytest" 2>/dev/null; then
    echo "Installing test dependencies..."
    pip install pytest pytest-asyncio pytest-mock pytest-cov moto boto3
fi

# Run different test suites
echo ""
echo "1. Running unit tests for new checks..."
pytest ../cloud_analyzer.common/tests/checks -v -m "not e2e"

echo ""
echo "2. Running integration tests..."
pytest tests/e2e/test_full_workflow_integration.py -v

echo ""
echo "3. Running CLI end-to-end tests..."
pytest tests/e2e/test_new_checks_e2e.py -v

echo ""
echo "4. Running provider simulation tests..."
pytest tests/e2e/test_real_provider_e2e.py -v -m e2e

echo ""
echo "5. Running full test suite with coverage..."
pytest --cov=src --cov=../cloud_analyzer.common/src --cov-report=html --cov-report=term tests/

echo ""
echo "Test Summary"
echo "============"
echo "All tests completed. Check htmlcov/index.html for coverage report."