# tools/file_reader.py

def read_json_file(path):
    import json, os
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing file: {path}")
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)