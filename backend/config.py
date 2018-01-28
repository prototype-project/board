import types
import easydb_client
from .domain import TaskRepositoryFactory
from .domain import BoardRepository

SPACE_NAME = 'taskBoard-09876543099887653'
BOARDS_BUCKET_NAME = 'boards'


def inject(app, obj_name):
    def decorator(controller):
        def decorated_controller(*args, **kwargs):
            kwargs[obj_name] = getattr(app, obj_name, None)
            return controller(*args, **kwargs)

        decorated_controller.__name__ = controller.__name__
        return decorated_controller
    return decorator


def configure_app(app):
    app.space = easydb_client.get_space(SPACE_NAME)
    app.boards_repository = BoardRepository(app.space.get_bucket(BOARDS_BUCKET_NAME))
    app.tasks_repository_factory = TaskRepositoryFactory(app.space).create

    app.inject = types.MethodType(inject, app)
    return app
