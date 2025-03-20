from flask import request, jsonify
from AI.api.api import app

messages = []

@app.route('/api/chat', methods=['POST'])
def chat():
    message = request.get_json().get('message')
    print(message)

    return jsonify({ "response": "Hello, I am a chatbot." })