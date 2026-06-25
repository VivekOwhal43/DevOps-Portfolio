from flask import Flask, jsonify, request
import os

app = Flask(__name__)

# Temporary in-memory database for Day 1
tasks = [
    {"id": 1, "title": "Setup Git, WSL, and Docker", "done": True},
    {"id": 2, "title": "Draft initial business plan for Pune startup", "done": False},
    {"id": 3, "title": "Containerize app with Docker", "done": False}
]

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

@app.route('/tasks', methods=['POST'])
def add_task():
    new_task = request.get_json()
    tasks.append({
        "id": len(tasks) + 1, 
        "title": new_task.get('title'), 
        "done": False
    })
    return jsonify({'message': 'Task added successfully'}), 201

if __name__ == '__main__':
    # Running on 0.0.0.0 is a DevOps best practice for container compatibility
    app.run(host='0.0.0.0', port=5000, debug=True)