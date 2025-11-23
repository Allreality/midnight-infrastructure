from flask import Flask, send_from_directory, send_file
import os

app = Flask(__name__)

# Serve the main website
@app.route('/')
def landing():
    return send_file('website-v2/index.html')

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('website-v2/css', path)

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('website-v2/js', path)

@app.route('/images/<path:path>')
def send_images(path):
    return send_from_directory('website-v2/images', path)

# Keep your existing API
@app.route('/api/knowledge/<path:path>')
def api_proxy(path):
    # Proxy to your existing knowledge base API on port 5002
    import requests
    resp = requests.get(f'http://localhost:5002/api/knowledge/{path}')
    return resp.json()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
