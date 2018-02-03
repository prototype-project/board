import easydb_client
from .domain import TaskRepositoryFactory
from .domain import BoardRepository

SPACE_NAME = 'taskBoard-09876543099887653'
BOARDS_BUCKET_NAME = 'boards'


def configure_space(app):
    if not hasattr(app, 'space'):
        app.space = easydb_client.get_space(SPACE_NAME)
    return app.space


def configure_boards_repository(app):
    configure_space(app)
    if not hasattr(app, 'boards_repository'):
        app.boards_repository = BoardRepository(app.space.get_bucket(BOARDS_BUCKET_NAME))
    return app.boards_repository


def configure_tasks_repository(app):
    configure_space(app)
    if not hasattr(app, 'tasks_repository_factory'):
        app.tasks_repository_factory = TaskRepositoryFactory(app.space).create
    return app.tasks_repository_factory
