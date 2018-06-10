from .domain import TaskRepositoryFactory
from .domain import BoardRepository


def configure_boards_repository(app):
    if not hasattr(app, 'boards_repository'):
        app.boards_repository = BoardRepository('http://104.131.17.195:8082')
    return app.boards_repository


def configure_tasks_repository(app):
    if not hasattr(app, 'tasks_repository_factory'):
        app.tasks_repository_factory = TaskRepositoryFactory('http://104.131.17.195:8082', configure_boards_repository(app)).create
    return app.tasks_repository_factory
