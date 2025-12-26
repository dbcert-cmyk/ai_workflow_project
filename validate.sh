#!/bin/bash
#
# 3-Layer Validation Pipeline for Autonomous Code Quality
# Designed for M4 Mac Mini 16GB + Qwen 14B + Aider
#
# DO NOT MODIFY THIS FILE - It's the core validation system
#

set -e  # Exit on first error

# Check if there are any Python files
if ! ls *.py 2>/dev/null 1>&2 && ! find . -name "*.py" -not -path "./venv/*" | grep -q .; then
    echo "No Python files found yet. Skipping validation."
    exit 0
fi

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}  🛡️  3-Layer Validation Pipeline${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"

# Layer 1: Style Check (ruff)
echo -e "${YELLOW}🔍 Layer 1: Style Check (ruff)...${NC}"
if ruff check . --quiet 2>/dev/null; then
    echo -e "${GREEN}✅ Style check passed${NC}\n"
else
    echo -e "${RED}❌ Style errors found${NC}"
    echo -e "${YELLOW}💡 Run 'ruff check --fix .' to auto-fix${NC}\n"
    exit 1
fi

# Layer 2: Type Check (mypy)
echo -e "${YELLOW}🧪 Layer 2: Type Check (mypy)...${NC}"
# Find all Python files excluding venv
PY_FILES=$(find . -name "*.py" -not -path "./venv/*" -not -path "*/__pycache__/*")
MYPY_FAIL=0
for f in $PY_FILES; do
    if ! mypy "$f" --ignore-missing-imports --no-error-summary > /dev/null 2>&1; then
        echo -e "${RED}❌ Type error in $f${NC}"
        mypy "$f" --ignore-missing-imports
        MYPY_FAIL=1
    fi
done

if [ $MYPY_FAIL -eq 0 ]; then
    echo -e "${GREEN}✅ Type check passed${NC}\n"
else
    exit 1
fi

# Layer 3: Behavior Tests (pytest)
echo -e "${YELLOW}✅ Layer 3: Behavior Tests (pytest)...${NC}"
# Run pytest. We don't pipe to silence it on failure so the full traceback is visible.
if pytest --maxfail=1 --tb=short; then
    echo -e "${GREEN}✅ All tests passed${NC}\n"
else
    echo -e "${RED}❌ Tests failed${NC}\n"
    exit 1
fi

# Success!
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}  ✨ All validations passed! Code is production-ready.${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

exit 0
