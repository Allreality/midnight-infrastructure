#!/usr/bin/env python3
"""
Generate summary of all industries in knowledge base
"""
import os
from pathlib import Path

kb_path = "knowledge-base"
report = []

report.append("# 🌙 Midnight Infrastructure - Industry Knowledge Base\n")
report.append(f"**Generated:** {os.popen('date').read().strip()}\n\n")
report.append("## 📊 Industry Coverage\n\n")

# Scan all directories
for category in sorted(os.listdir(kb_path)):
    cat_path = os.path.join(kb_path, category)
    if os.path.isdir(cat_path):
        # Count files
        files = list(Path(cat_path).rglob('*.md'))
        if files:
            report.append(f"### {category.replace('_', ' ').title()}\n")
            report.append(f"**Documents:** {len(files)}\n\n")
            
            # List first 5 docs
            for f in files[:5]:
                report.append(f"- {f.name}\n")
            
            if len(files) > 5:
                report.append(f"- ... and {len(files)-5} more\n")
            report.append("\n")

# Save report
with open("knowledge-base/INDUSTRY_SUMMARY.md", "w") as f:
    f.writelines(report)

print("✅ Industry summary generated!")
print("📄 View: knowledge-base/INDUSTRY_SUMMARY.md")
