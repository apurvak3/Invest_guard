# Blockchain mock
from flask import Blueprint, jsonify, request
from utils.encryption import encrypt_data
import json
import os

blockchain_bp = Blueprint('blockchain', __name__)

# Mock blockchain: Log to file
LOG_FILE = 'blockchain_logs.json'

if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, 'w') as f:
        json.dump([], f)

@blockchain_bp.route('/log', methods=['POST'])
def log_flagged():
    data = request.json
    content = data.get('content', '')
    encrypted = encrypt_data(content)
    with open(LOG_FILE, 'r+') as f:
        logs = json.load(f)
        logs.append({'encrypted_content': encrypted})
        f.seek(0)
        json.dump(logs, f)
    return jsonify({'tx_id': len(logs), 'status': 'Logged'})

@blockchain_bp.route('/logs', methods=['GET'])
def get_logs():
    with open(LOG_FILE, 'r') as f:
        logs = json.load(f)
    return jsonify(logs)