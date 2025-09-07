from flask import Flask, jsonify, request, Response
from typing import Any, Dict
from flask_cors import CORS
from agents.appointment_agent import AppointmentAgent
from utils.thread_manager import ThreadManager

app = Flask(__name__)
CORS(app)

# Initialize the thread manager and agents
thread_manager = ThreadManager()
agents = {}

@app.route('/threads', methods=['GET'])
def get_threads() -> Response:
    return jsonify(thread_manager.get_all_threads()), 200

@app.route('/threads', methods=['POST'])
def create_thread() -> Response:
    data = request.json
    thread_name = data.get('name')
    if not thread_name:
        return jsonify({"error": "Thread name is required."}), 400
    thread_id = thread_manager.create_thread(thread_name)
    agent = AppointmentAgent()
    agent.start_chat()
    agents[thread_id] = agent
    return jsonify({"thread_id": thread_id}), 201

@app.route('/threads/<thread_id>', methods=['DELETE'])
def delete_thread(thread_id: str) -> Response:
    try:
        thread_id_int = int(thread_id)
    except ValueError:
        return jsonify({"error": "Invalid thread ID."}), 400
    if thread_manager.delete_thread(thread_id_int):
        agents.pop(thread_id_int, None)
        return jsonify({"message": "Thread deleted."}), 200
    return jsonify({"error": "Thread not found."}), 404

@app.route('/threads/<thread_id>/ask', methods=['POST'])
def ask_agent(thread_id: str) -> Response:
    try:
        thread_id_int = int(thread_id)
    except ValueError:
        return jsonify({"error": "Invalid thread ID."}), 400
    if thread_id_int not in agents:
        return jsonify({"error": "Thread not found."}), 404
    data = request.json
    user_input = data.get('input')
    if not user_input:
        return jsonify({"error": "Input is required."}), 400
    reply = agents[thread_id_int].ask(user_input)
    # Store messages as objects for frontend compatibility
    from datetime import datetime
    timestamp = datetime.now().strftime("%H:%M")
    thread_manager.add_message_to_thread(thread_id_int, {
        "content": user_input,
        "sender": "user",
        "timestamp": timestamp
    })
    thread_manager.add_message_to_thread(thread_id_int, {
        "content": reply,
        "sender": "agent",
        "timestamp": timestamp
    })
    return jsonify({"reply": reply}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5001)