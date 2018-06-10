from flask import jsonify
from flask import Flask
from flask import request
from flask import Response
from flask import render_template
from werkzeug.exceptions import BadRequest

from .domain import CreateTaskDto
from .domain import UpdateTaskDto
from .domain import BoardNotFound
from .domain import TaskNotFound
from .config import configure_boards_repository
from .config import configure_tasks_repository

app = Flask(__name__, static_folder="../../frontend/dist/static", template_folder="../../frontend/dist")


@app.route('/api/boards', methods=['POST'])
def create_board():
    board = configure_boards_repository(app).new
    print('happy')
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
        status = request.json['status']
        body = request.json['body']
        task_repo.update(UpdateTaskDto(task_pk, body, status))
    except (BoardNotFound, TaskNotFound):
        return Response(status=404)
    except (BadRequest, ValueError):
        return Response(status=400)

    return Response(status=200)


@app.route('/api/boards/<board_pk>/tasks/<task_pk>', methods=['DELETE'])
def delete_task(board_pk, task_pk):
    try:
        task_repo = configure_tasks_repository(app)(board_pk)
        task_repo.delete(task_pk)
    except (BoardNotFound, TaskNotFound):
        return Response(status=404)

    return Response(status=200)


@app.route('/api/boards/<board_pk>/tasks', methods=['POST'])
def add_task(board_pk):
    try:
        task_repo = configure_tasks_repository(app)(board_pk)
        body = request.json['body']
    except BoardNotFound:
        return Response(status=404)
    except (KeyError, BadRequest):
        return Response(status=400)

    created_task = task_repo.add(CreateTaskDto(body))
    return jsonify(created_task.json)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")