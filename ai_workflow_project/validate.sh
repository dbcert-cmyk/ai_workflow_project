#!/bin/bash

echo " Starting Pre-Flight Validation..."
echo ""

# 1. Run the Linter
echo " Checking code style (Ruff)..."
if ruff check .; then
    echo "✅ Style is clean!"
else
    echo "❌ Style check failed. Fix the errors above."
    exit 1
fi

echo ""

# 2. Run the Tests
echo "離 Running functional tests (Pytest)..."
if pytest -q; then
    echo "✅ All tests passed!"
else
    echo "❌ Tests failed. Check the logic."
    exit 1
fi

echo ""
echo " Validation Complete: Code is ready for production!"