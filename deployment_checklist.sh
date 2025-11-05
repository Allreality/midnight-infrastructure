#!/bin/bash
echo "🔍 Pre-Deployment Checklist"
echo "================================"

# 1. Check services
echo "✓ Services:"
lsof -ti:5002 > /dev/null && echo "  ✅ Midnight Infrastructure (5002)" || echo "  ❌ Port 5002 down"

# 2. Check knowledge base
DOCS=$(find knowledge-base -name "*.md" | wc -l)
echo "  ✅ Knowledge Base: $DOCS documents"

# 3. Check API keys
if [ -f .env ]; then
    echo "  ✅ Environment configured"
else
    echo "  ❌ Missing .env file"
fi

# 4. Test endpoints
echo ""
echo "✓ API Tests:"
curl -s http://localhost:5002/health > /dev/null && echo "  ✅ Health endpoint" || echo "  ❌ Health failed"
curl -s http://localhost:5002/api/payment/pricing > /dev/null && echo "  ✅ Payment API" || echo "  ❌ Payment failed"
curl -s http://localhost:5002/api/knowledge/stats > /dev/null && echo "  ✅ Knowledge API" || echo "  ❌ Knowledge failed"

# 5. Check static files
echo ""
echo "✓ Static Files:"
[ -f static/landing.html ] && echo "  ✅ Landing page" || echo "  ❌ Missing landing.html"
[ -f static/wallet-connect.html ] && echo "  ✅ Subscribe page" || echo "  ❌ Missing wallet-connect.html"
[ -f static/knowledge.html ] && echo "  ✅ Knowledge base UI" || echo "  ❌ Missing knowledge.html"

echo ""
echo "================================"
