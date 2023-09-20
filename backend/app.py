
from flask import Flask, jsonify, request
from datetime import datetime, timedelta
import random
import string

app = Flask(__name__)

# In-memory database for simplicity
keys_db = []

@app.route("/generate", methods=["POST"])
def generate_key():
    length = request.json.get("length", 8)
    duration = request.json.get("duration", "1d")

    if duration == "1d":
        expiry = datetime.now() + timedelta(days=1)
    elif duration == "1w":
        expiry = datetime.now() + timedelta(weeks=1)
    elif duration == "2w":
        expiry = datetime.now() + timedelta(weeks=2)
    elif duration == "1m":
        expiry = datetime.now() + timedelta(days=30)
    elif duration == "infinite":
        expiry = None
    else:
        return jsonify({"error": "Invalid duration"}), 400

    key = "STE-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
    keys_db.append({
        "key": key,
        "expiry": expiry
    })

    return jsonify({"key": key})

@app.route("/keys", methods=["GET"])
def get_keys():
    return jsonify({"keys": keys_db})

@app.route("/extend/<key>", methods=["POST"])
def extend_key_time(key):
    for k in keys_db:
        if k["key"] == key:
            if k["expiry"]:
                k["expiry"] += timedelta(days=1)
            return jsonify({"success": True})
    return jsonify({"error": "Key not found"}), 404

@app.route("/remove-time/<key>", methods=["POST"])
def remove_key_time(key):
    for k in keys_db:
        if k["key"] == key:
            if k["expiry"]:
                k["expiry"] -= timedelta(days=1)
            return jsonify({"success": True})
    return jsonify({"error": "Key not found"}), 404

@app.route("/delete/<key>", methods=["DELETE"])
def delete_key(key):
    global keys_db
    keys_db = [k for k in keys_db if k["key"] != key]
    return jsonify({"success": True})

if __name__ == "__main__":
    app.run(debug=True)
