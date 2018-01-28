from flask import jsonify
from flask import Flask
from flask import request
from flask import Response
from flask import render_template
import requests

from .config import configure_app
from .domain import CreateTaskDto
from .domain import UpdateTaskDto
from .domain import TaskStatus

app = configure_app(Flask(__name__, static_folder="../frontend/dist/static", template_folder="../frontend/dist"))


@app.route('/api/boards', methods=['POST'])
@app.inject('boards_repository')
def create_board(boards_repository):
    board = boards_repository.new
    return jsonify(board.json)


@app.route('/api/boards/<board_pk>/tasks', methods=['GET'])
@app.inject('tasks_repository_factory')
def get_all_tasks(board_pk, tasks_repository_factory):
    task_repo = tasks_repository_factory(board_pk)
    tasks = task_repo.all
    return jsonify([task.json for task in tasks])


@app.route('/api/boards/<board_pk>/tasks/<task_pk>', methods=['PUT'])
@app.inject('tasks_repository_factory')
def update_task(board_pk, task_pk, tasks_repository_factory):
    task_repo = tasks_repository_factory(board_pk)
    status = request.json['status']
    body = request.json['body']
    task_repo.update(UpdateTaskDto(task_pk, body, TaskStatus.of(status)))
    return Response(status=200)


@app.route('/api/boards/<board_pk>/tasks/<task_pk>', methods=['DELETE'])
@app.inject('tasks_repository_factory')
def delete_task(board_pk, task_pk, tasks_repository_factory):
    task_repo = tasks_repository_factory(board_pk)
    task_repo.delete(task_pk)
    return Response(status=200)


@app.route('/api/boards/<board_pk>/tasks', methods=['POST'])
@app.inject('tasks_repository_factory')
def add_task(board_pk, tasks_repository_factory):
    task_repo = tasks_repository_factory(board_pk)
    created_task = task_repo.add(CreateTaskDto(request.json['body']))
    return jsonify(created_task.json)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if app.debug:
        return requests.get('http://localhost:8080/{}'.format(path)).text
    return render_template("index.html")