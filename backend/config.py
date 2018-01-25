import easydb_client
from flask import g
from .domain import TaskRepository
from .domain import BoardRepository

SPACE_NAME = 'taskBoard-09876543099887653'
BOARDS_BUCKET_NAME = 'boards'


def get_space():
    if not hasattr(g, 'space'):
        g.space = easydb_client.get_space(SPACE_NAME)

    return g.space


def get_task_repository(board_pk):
    space = get_space()
    return TaskRepository(space.get_bucket(board_pk))


def get_board_repository():
    space = get_space()
    return BoardRepository(space.get_bucket(BOARDS_BUCKET_NAME))
