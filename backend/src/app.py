from flask import jsonify
from flask import Flask
from flask import request
from flask import Response
from flask import render_template
import requests

from .domain import CreateTaskDto
from .domain import UpdateTaskDto
from .domain import BoardNotFound
from .config import configure_boards_repository
from .config import configure_tasks_repository

app = Flask(__name__, static_folder="../../frontend/dist/static", template_folder="../../frontend/dist")


@app.route('/api/boards', methods=['POST'])
def create_board():
    board = configure_boards_repository(app).new
    return jsonify(board.json)


@app.route('/api/boards/<board_pk>/tasks', methods=['GET'])
def get_all_tasks(board_pk):
    try:
        task_repo = configure_tasks_repository(app)(board_pk)
    except BoardNotFound:
        return Response(status=404)

    tasks = task_repo.all
    return jsonify([task.json for task in tasks])


@app.route('/api/boards/<board_pk>/tasks/<task_pk>', methods=['PUT'])
def update_task(board_pk, task_pk):
    try:
        task_repo = configure_tasks_repository(app)(board_pk)
    except BoardNotFound:
        return Response(status=404)

    status = request.json['status']
    body = request.json['body']
    task_repo.update(UpdateTaskDto(task_pk, body, status))
    return Response(status=200)


@app.route('/api/boards/<board_pk>/tasks/<task_pk>', methods=['DELETE'])
def delete_task(board_pk, task_pk):
    task_repo = configure_tasks_repository(app)(board_pk)
    task_repo.delete(task_pk)
    return Response(status=200)


@app.route('/api/boards/<board_pk>/tasks', methods=['POST'])
def add_task(board_pk):
    task_repo = configure_tasks_repository(app)(board_pk)
    print(request.data)
    body = request.json['body']
    created_task = task_repo.add(CreateTaskDto(body))
    return jsonify(created_task.json)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if app.debug:
        return requests.get('http://localhost:8080/{}'.format(path)).text
    return render_template("index.html")