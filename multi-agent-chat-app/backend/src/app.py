from flask import Flask, jsonify, request, Response
from typing import Dict
from flask_cors import CORS
from agents.appointment_agent import AppointmentAgent
from utils.thread_manager import ThreadManager
import requests

app = Flask(__name__)
CORS(app)

# Initialize the thread manager and agents
thread_manager = ThreadManager()
agents: Dict[int, AppointmentAgent] = {}

@app.route('/threads', methods=['GET'])
def get_threads() -> Response:
    response = jsonify(thread_manager.get_all_threads())
    response.status_code = 200
    return response

@app.route('/threads', methods=['POST'])
def create_thread() -> Response:
    data = request.json
    if not data or 'patient_id' not in data:
        response = jsonify({"error": "Patient ID is required."})
        response.status_code = 400
        return response
    patient_id = data['patient_id']

    # Fetch patient info from external API
    try:
        resp = requests.get(f"http://localhost:5000/patient/{patient_id}")
        if resp.status_code != 200:
            response = jsonify({"error": "Patient not found."})
            response.status_code = 404
            return response
        patient_info = resp.json()
    except Exception:
        response = jsonify({"error": "Failed to fetch patient info."})
        response.status_code = 500
        return response

    thread_id = thread_manager.create_thread(patient_id)
    agent = AppointmentAgent(patient_info)
    agent.start_chat()
    agents[thread_id] = agent
    response = jsonify({"thread_id": thread_id})
    response.status_code = 201
    return response

@app.route('/threads/<thread_id>', methods=['DELETE'])
def delete_thread(thread_id: str) -> Response:
    try:
        thread_id_int = int(thread_id)
    except ValueError:
        response = jsonify({"error": "Invalid thread ID."})
        response.status_code = 400
        return response
    if thread_manager.delete_thread(thread_id_int):
        agents.pop(thread_id_int, None)
        response = jsonify({"message": "Thread deleted."})
        response.status_code = 200
        return response
    response = jsonify({"error": "Thread not found."})
    response.status_code = 404
    return response

@app.route('/threads/<thread_id>/ask', methods=['POST'])
def ask_agent(thread_id: str) -> Response:
    try:
        thread_id_int = int(thread_id)
    except ValueError:
        response = jsonify({"error": "Invalid thread ID."})
        response.status_code = 400
        return response
    data = request.json
    if not data or 'input' not in data:
        response = jsonify({"error": "Input is required."})
        response.status_code = 400
        return response
    user_input = data.get('input')
    thread = thread_manager.get_thread(thread_id_int)
    if thread is None:
        response = jsonify({"error": "Thread not found."})
        response.status_code = 404
        return response
    reply = agents[thread_id_int].ask(user_input)
    if reply is None:
        response = jsonify({"error": "Agent failed to respond."})
        response.status_code = 500
        return response
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
    response = jsonify({"reply": reply})
    response.status_code = 200
    return response

if __name__ == '__main__':
    app.run(debug=True, port=5001)