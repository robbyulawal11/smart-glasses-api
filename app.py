from flask import Flask, request, jsonify # type: ignore
import json
import os

app = Flask(__name__)

# Path untuk file data
DATA_FILE = 'data.json'

# Fungsi untuk membaca data dari file JSON
def read_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    return []

# Fungsi untuk menulis data ke file JSON
def write_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

@app.route('/sensor/data', methods=['GET'])
def get_data():
    data = read_data()
    return jsonify(data), 200

@app.route('/sensor/data', methods=['POST'])
def post_data():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    new_data = request.get_json()
    if not new_data:
        return jsonify({"error": "Invalid data"}), 400

    data = read_data()
    data.append(new_data)
    write_data(data)

    return jsonify(new_data), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
