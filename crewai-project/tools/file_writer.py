# File: tools/file_writer.py
# Location: crewai-project/tools/file_writer.py
from tools.file_reader import read_json_file
import os
import json

def write_json_file(path, data, backup=True):
    try:
        # Create folder if needed
        os.makedirs(os.path.dirname(path), exist_ok=True)

        # Backup existing file
        if backup and os.path.exists(path):
            base, ext = os.path.splitext(path)
            backup_path = f"{base}_backup{ext}"
            os.rename(path, backup_path)

        # Write new file
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    except Exception as e:
        print(f"Failed to write file: {e}")