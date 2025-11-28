#!/bin/bash
# Restore from latest working backup
LATEST=$(ls -td /mnt/c/projects/midnight-infrastructure/backups/*_working 2>/dev/null | head -1)
if [ -z "$LATEST" ]; then
    echo "No backup found!"
    exit 1
fi
echo "Restoring from: $LATEST"
cp "$LATEST/payment_api.py" /mnt/c/projects/midnight-infrastructure/
cp "$LATEST/index.html" /mnt/c/projects/midnight-infrastructure/
cp "$LATEST/fulfillment.html" /mnt/c/projects/midnight-infrastructure/
cp "$LATEST/analytics-dashboard.html" /mnt/c/projects/midnight-infrastructure/
echo "✅ Restored!"
