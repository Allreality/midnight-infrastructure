#!/bin/bash
# Claude-Proof Protection for Midnight Infrastructure
# Prevents AI from overwriting working code

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
ARCHIVE_DIR="archive/working_states"

mkdir -p "$ARCHIVE_DIR"

echo "🛡️  Claude-Proof Backup: $TIMESTAMP"

# Backup critical files
tar -czf "$ARCHIVE_DIR/backup_$TIMESTAMP.tar.gz" \
  server.py \
  static/ \
  agents/ \
  knowledge-base/ \
  --exclude='*.pyc' \
  --exclude='__pycache__'

# Git commit
git add server.py static/knowledge.html agents/
git commit -m "🛡️ Claude-proof: $TIMESTAMP" 2>/dev/null || echo "No changes to commit"

echo "✅ Backup saved: $ARCHIVE_DIR/backup_$TIMESTAMP.tar.gz"
ls -lh "$ARCHIVE_DIR/backup_$TIMESTAMP.tar.gz"
