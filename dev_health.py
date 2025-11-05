# dev_health.py
from flask import Flask, jsonify
app = Flask("dev_health")

@app.route("/health", methods=["GET"])
def health():
    return jsonify(status="ok"), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5060)