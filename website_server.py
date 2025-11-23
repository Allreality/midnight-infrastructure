from flask import Flask, send_file, send_from_directory
import os

app = Flask(__name__)

@app.route('/')
def index():
    return send_file('website-v2/index.html')

@app.route('/css/<path:filename>')
def css_files(filename):
    return send_from_directory('website-v2/css', filename)

@app.route('/js/<path:filename>')
def js_files(filename):
    return send_from_directory('website-v2/js', filename)

@app.route('/images/<path:filename>')
def image_files(filename):
    return send_from_directory('website-v2/images', filename)

@app.route('/health')
def health():
    return {'status': 'healthy', 'website': 'Total Reality Global'}

if __name__ == '__main__':
    print("=" * 60)
    print("🌐 Total Reality Global Website Server")
    print("=" * 60)
    print("Starting on http://localhost:3001")
    print("Press Ctrl+C to stop")
    print("=" * 60)
    app.run(host='0.0.0.0', port=3001, debug=True)
