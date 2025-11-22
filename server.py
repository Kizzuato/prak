from flask import Flask, request, jsonify
import os
import json

filePath = 'data.json'
app = Flask(__name__)


def load_messages():
    """Load messages list from the JSON file. Returns empty list if file missing or invalid."""
    if not os.path.exists(filePath):
        return []
    try:
        with open(filePath, 'r', encoding='utf-8') as f:
            return json.load(f) or []
    except (json.JSONDecodeError, OSError):
        return []


def save_messages(messages):
    with open(filePath, 'w', encoding='utf-8') as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)


@app.route('/api', methods=['GET'])
def get_messages():
    messages = load_messages()
    return jsonify(messages)


@app.route('/api', methods=['POST'])
def add_message():
    data = request.get_json() or {}
    text = data.get('text')
    if text is None:
        return jsonify({'error': 'Missing "text" field'}), 400

    messages = load_messages()
    next_id = max((m.get('id', 0) for m in messages), default=0) + 1
    new_message = {
        'id': next_id,
        'text': text
    }
    messages.append(new_message)
    save_messages(messages)
    return jsonify(new_message), 201


if __name__ == '__main__':
    app.run(debug=True)