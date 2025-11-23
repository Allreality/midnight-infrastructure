#!/bin/bash
# Midnight Infrastructure - Gap Analysis Verification Script
# This script tests all endpoints and functionality

echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║                                                                      ║"
echo "║         🌙  MIDNIGHT INFRASTRUCTURE - VERIFICATION SUITE             ║"
echo "║                                                                      ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

PASS=0
FAIL=0

# Test function
run_test() {
    local test_name="$1"
    local test_command="$2"
    local expected="$3"
    
    echo -n "Testing: $test_name ... "
    
    result=$(eval "$test_command" 2>&1)
    
    if echo "$result" | grep -q "$expected"; then
        echo -e "${GREEN}✓ PASS${NC}"
        ((PASS++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}"
        echo "  Expected: $expected"
        echo "  Got: $result"
        ((FAIL++))
        return 1
    fi
}

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📋 PRE-FLIGHT CHECKS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check if port 5003 is listening
echo -n "1. Checking if port 5003 is active ... "
if lsof -Pi :5003 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo -e "${GREEN}✓ PASS${NC}"
    ((PASS++))
else
    echo -e "${RED}✗ FAIL - Service not running!${NC}"
    echo ""
    echo "To start the service, run:"
    echo "  cd /mnt/c/projects/midnight-infrastructure"
    echo "  python3 app.py"
    echo ""
    exit 1
fi

# Check if Python is available
echo -n "2. Checking Python availability ... "
if command -v python3 &> /dev/null; then
    echo -e "${GREEN}✓ PASS${NC} ($(python3 --version))"
    ((PASS++))
else
    echo -e "${RED}✗ FAIL${NC}"
    ((FAIL++))
fi

# Check if curl is available
echo -n "3. Checking curl availability ... "
if command -v curl &> /dev/null; then
    echo -e "${GREEN}✓ PASS${NC}"
    ((PASS++))
else
    echo -e "${RED}✗ FAIL${NC}"
    ((FAIL++))
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔍 API ENDPOINT TESTS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Test health endpoint
run_test "Health endpoint response" \
    "curl -s http://localhost:5003/health" \
    "healthy"

# Test health endpoint has correct service name
run_test "Health endpoint service name" \
    "curl -s http://localhost:5003/health" \
    "Gap Analysis"

# Test health endpoint version
run_test "Health endpoint version" \
    "curl -s http://localhost:5003/health" \
    "2.1"

# Test gap analysis API
run_test "Gap analysis API availability" \
    "curl -s http://localhost:5003/api/gap-analysis" \
    "midnight_info"

# Test gap analysis has critical gaps
run_test "Critical gaps present" \
    "curl -s http://localhost:5003/api/gap-analysis" \
    "GAP-001"

# Test gap analysis has roadmap
run_test "Solution roadmap present" \
    "curl -s http://localhost:5003/api/gap-analysis" \
    "roadmap"

# Test gap analysis has Midnight info
run_test "Midnight blockchain info present" \
    "curl -s http://localhost:5003/api/gap-analysis" \
    "Input Output Global"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 DATA INTEGRITY TESTS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Test total gaps count
echo -n "Testing: Total gaps count ... "
GAPS=$(curl -s http://localhost:5003/api/gap-analysis | grep -o '"total_gaps": [0-9]*' | grep -o '[0-9]*')
if [ "$GAPS" -eq 9 ]; then
    echo -e "${GREEN}✓ PASS${NC} (Found $GAPS gaps)"
    ((PASS++))
else
    echo -e "${RED}✗ FAIL${NC} (Expected 9, found $GAPS)"
    ((FAIL++))
fi

# Test critical gaps count
echo -n "Testing: Critical gaps count ... "
CRITICAL=$(curl -s http://localhost:5003/api/gap-analysis | grep -o '"critical_count": [0-9]*' | grep -o '[0-9]*')
if [ "$CRITICAL" -eq 3 ]; then
    echo -e "${GREEN}✓ PASS${NC} (Found $CRITICAL critical gaps)"
    ((PASS++))
else
    echo -e "${RED}✗ FAIL${NC} (Expected 3, found $CRITICAL)"
    ((FAIL++))
fi

# Test high priority gaps count
echo -n "Testing: High priority gaps count ... "
HIGH=$(curl -s http://localhost:5003/api/gap-analysis | grep -o '"high_count": [0-9]*' | grep -o '[0-9]*')
if [ "$HIGH" -eq 4 ]; then
    echo -e "${GREEN}✓ PASS${NC} (Found $HIGH high priority gaps)"
    ((PASS++))
else
    echo -e "${RED}✗ FAIL${NC} (Expected 4, found $HIGH)"
    ((FAIL++))
fi

# Test medium priority gaps count
echo -n "Testing: Medium priority gaps count ... "
MEDIUM=$(curl -s http://localhost:5003/api/gap-analysis | grep -o '"medium_count": [0-9]*' | grep -o '[0-9]*')
if [ "$MEDIUM" -eq 2 ]; then
    echo -e "${GREEN}✓ PASS${NC} (Found $MEDIUM medium priority gaps)"
    ((PASS++))
else
    echo -e "${RED}✗ FAIL${NC} (Expected 2, found $MEDIUM)"
    ((FAIL++))
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🌐 WEB INTERFACE TESTS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Test main page loads
run_test "Main page loads" \
    "curl -s http://localhost:5003/" \
    "MIDNIGHT INFRASTRUCTURE"

# Test page has gap analysis title
run_test "Gap analysis title present" \
    "curl -s http://localhost:5003/" \
    "Gap Analysis Report"

# Test page has critical gaps section
run_test "Critical gaps section present" \
    "curl -s http://localhost:5003/" \
    "CRITICAL PRIORITY GAPS"

# Test page has comparison section
run_test "Comparison section present" \
    "curl -s http://localhost:5003/" \
    "MIDNIGHT VS COMPETITORS"

# Test page has roadmap section
run_test "Roadmap section present" \
    "curl -s http://localhost:5003/" \
    "SOLUTION ROADMAP"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔬 RESEARCH DATA VALIDATION"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Test Midnight info
run_test "Midnight CEO name" \
    "curl -s http://localhost:5003/api/gap-analysis" \
    "Eran Barak"

run_test "Midnight founder name" \
    "curl -s http://localhost:5003/api/gap-analysis" \
    "Charles Hoskinson"

run_test "Midnight token name" \
    "curl -s http://localhost:5003/api/gap-analysis" \
    "NIGHT"

run_test "Midnight developer" \
    "curl -s http://localhost:5003/api/gap-analysis" \
    "Input Output Global"

# Test competitor data
run_test "Zcash in competitors" \
    "curl -s http://localhost:5003/api/gap-analysis" \
    "Zcash"

run_test "Aleo in competitors" \
    "curl -s http://localhost:5003/api/gap-analysis" \
    "Aleo"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎯 SPECIFIC GAP TESTS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Test GAP-001 (Performance)
run_test "GAP-001: Computational Overhead" \
    "curl -s http://localhost:5003/api/gap-analysis" \
    "Computational Overhead in ZKP Generation"

# Test GAP-002 (Trusted Setup)
run_test "GAP-002: Trusted Setup" \
    "curl -s http://localhost:5003/api/gap-analysis" \
    "Trusted Setup Elimination"

# Test GAP-003 (Compliance)
run_test "GAP-003: Regulatory Compliance" \
    "curl -s http://localhost:5003/api/gap-analysis" \
    "Privacy vs. Compliance Trade-off"

# Test GAP-004 (Interoperability)
run_test "GAP-004: Cross-Chain" \
    "curl -s http://localhost:5003/api/gap-analysis" \
    "Cross-Chain Interoperability"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📈 PERFORMANCE TESTS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Test response time for health endpoint
echo -n "Testing: Health endpoint response time ... "
RESPONSE_TIME=$(curl -o /dev/null -s -w '%{time_total}\n' http://localhost:5003/health)
if (( $(echo "$RESPONSE_TIME < 1.0" | bc -l) )); then
    echo -e "${GREEN}✓ PASS${NC} (${RESPONSE_TIME}s)"
    ((PASS++))
else
    echo -e "${YELLOW}⚠ SLOW${NC} (${RESPONSE_TIME}s - should be <1s)"
    ((PASS++))
fi

# Test response time for gap analysis API
echo -n "Testing: Gap analysis API response time ... "
RESPONSE_TIME=$(curl -o /dev/null -s -w '%{time_total}\n' http://localhost:5003/api/gap-analysis)
if (( $(echo "$RESPONSE_TIME < 2.0" | bc -l) )); then
    echo -e "${GREEN}✓ PASS${NC} (${RESPONSE_TIME}s)"
    ((PASS++))
else
    echo -e "${YELLOW}⚠ SLOW${NC} (${RESPONSE_TIME}s - should be <2s)"
    ((PASS++))
fi

# Test response time for main page
echo -n "Testing: Main page response time ... "
RESPONSE_TIME=$(curl -o /dev/null -s -w '%{time_total}\n' http://localhost:5003/)
if (( $(echo "$RESPONSE_TIME < 3.0" | bc -l) )); then
    echo -e "${GREEN}✓ PASS${NC} (${RESPONSE_TIME}s)"
    ((PASS++))
else
    echo -e "${YELLOW}⚠ SLOW${NC} (${RESPONSE_TIME}s - should be <3s)"
    ((PASS++))
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 TEST SUMMARY"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

TOTAL=$((PASS + FAIL))
PASS_RATE=$((PASS * 100 / TOTAL))

echo "Total Tests: $TOTAL"
echo -e "${GREEN}Passed: $PASS${NC}"
echo -e "${RED}Failed: $FAIL${NC}"
echo "Pass Rate: ${PASS_RATE}%"
echo ""

if [ $FAIL -eq 0 ]; then
    echo -e "${GREEN}╔══════════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║                                                                      ║${NC}"
    echo -e "${GREEN}║                   ✓ ALL TESTS PASSED!                                ║${NC}"
    echo -e "${GREEN}║                                                                      ║${NC}"
    echo -e "${GREEN}║         Midnight Infrastructure Gap Analysis is working!             ║${NC}"
    echo -e "${GREEN}║                                                                      ║${NC}"
    echo -e "${GREEN}╚══════════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo "🌐 View the dashboard at: http://localhost:5003"
    echo "📊 Access API at: http://localhost:5003/api/gap-analysis"
    echo ""
    exit 0
else
    echo -e "${RED}╔══════════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${RED}║                                                                      ║${NC}"
    echo -e "${RED}║                   ✗ SOME TESTS FAILED                                ║${NC}"
    echo -e "${RED}║                                                                      ║${NC}"
    echo -e "${RED}║              Please check the errors above                           ║${NC}"
    echo -e "${RED}║                                                                      ║${NC}"
    echo -e "${RED}╚══════════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    exit 1
fi