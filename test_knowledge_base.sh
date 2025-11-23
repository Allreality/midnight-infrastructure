#!/bin/bash
# Quick Knowledge Base Verification Script

echo "🧪 KNOWLEDGE BASE QUICK TEST"
echo "=============================="
echo ""

# Test API is running
if curl -s http://localhost:5002/health | grep -q "healthy"; then
    echo "✅ API Server: RUNNING"
else
    echo "❌ API Server: NOT RUNNING"
    exit 1
fi

# Test stats endpoint
STATS=$(curl -s http://localhost:5002/api/knowledge/stats)
DOC_COUNT=$(echo $STATS | python3 -c "import sys, json; print(json.load(sys.stdin)['total_documents'])")
echo "✅ Total Documents: $DOC_COUNT"

# Test all 14 control families are searchable
echo ""
echo "🔍 Testing Control Family Coverage:"

FAMILIES=(
    "Access Control"
    "Awareness and Training"
    "Audit and Accountability"
    "Configuration Management"
    "Identification and Authentication"
    "Incident Response"
    "Maintenance"
    "Media Protection"
    "Personnel Security"
    "Physical Protection"
    "Risk Assessment"
    "Security Assessment"
    "System and Communications Protection"
    "System and Information Integrity"
)

FOUND=0
for family in "${FAMILIES[@]}"; do
    RESULT=$(curl -s -X POST http://localhost:5002/api/knowledge/search \
        -H "Content-Type: application/json" \
        -d "{\"query\":\"$family\"}" | python3 -c "import sys, json; print(json.load(sys.stdin)['results_count'])")
    
    if [ "$RESULT" -gt 0 ]; then
        echo "  ✅ $family: $RESULT docs"
        ((FOUND++))
    else
        echo "  ❌ $family: NOT FOUND"
    fi
done

echo ""
echo "=============================="
if [ "$FOUND" -eq 14 ]; then
    echo "✅ ALL 14 CONTROL FAMILIES VERIFIED"
    echo "✅ KNOWLEDGE BASE: OPERATIONAL"
else
    echo "⚠️  ONLY $FOUND/14 CONTROL FAMILIES FOUND"
    echo "❌ KNOWLEDGE BASE: INCOMPLETE"
fi
echo "=============================="
