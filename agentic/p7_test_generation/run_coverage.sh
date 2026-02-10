#!/bin/bash
# Run tests with coverage

echo "Running tests with coverage..."
echo "================================"

pytest test_scheduler.py \
    --cov=scheduler \
    --cov-report=term-missing \
    --cov-report=html:coverage_html \
    --cov-branch \
    -v

echo ""
echo "Coverage report saved to coverage_html/index.html"
