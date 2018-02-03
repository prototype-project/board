import enum
import easydb_client


class TaskStatus(enum.Enum):
    TODO = 'todo'
    IN_PROGRESS = 'inProgress'
    DONE = 'done'

    @classmethod
    def of(cls, status_as_str):
        if cls.TODO.value == status_as_str:
            return cls.TODO
        elif cls.IN_PROGRESS.value == status_as_str:
            return cls.IN_PROGRESS
        elif cls.DONE.value == status_as_str:
            return cls.DONE
        else:
            raise ValueError('Unknown status')


class Task:
    def __init__(self, pk, body, status):
        self.pk = pk
        self.body = body
        self.status = status

    @property
    def json(self):
        return {
            'pk': self.pk,
            'body': self.body,
            'status': self.status.value
        }


class CreateTaskDto:
    def __init__(self, body):
        self.body = body
        self.status = TaskStatus.TODO

    @property
    def json(self):
        return {
            'body': self.body,
            'status': self.status.value
        }


class UpdateTaskDto:
    def __init__(self, pk, body, status):
        self.pk = pk
        self.body = body
        self.status = TaskStatus.of(status)

    @property
    def json(self):
        return {
            'body': self.body,
            'status': self.status.value
        }


class Board:
    def __init__(self, pk):
        self.pk = pk

    @property
    def json(self):
        return {
            'pk': self.pk
        }


class TaskNotFound(ValueError):
    pass


class TaskRepository:
    def __init__(self, task_bucket):
        self._tasks = task_bucket

    @property
    def all(self):
        return map(self._to_entity, self._tasks.all())

    def add(self, create_task_dto):
        created_task_as_json = self._tasks.add(create_task_dto.json)
        return self._to_entity(created_task_as_json)

    def delete(self, task_pk):
        try:
            self._tasks.remove(task_pk)
        except easydb_client.ElementNotFound:
            raise TaskNotFound()

    def update(self, change_status_task_dto):
        try:
            self._tasks.update(change_status_task_dto.pk, change_status_task_dto.json)
        except easydb_client.ElementNotFound:
            raise TaskNotFound

    def _to_entity(self, task_as_json):
        return Task(
            task_as_json['id'],
            task_as_json['fields']['body'],
            TaskStatus.of(task_as_json['fields']['status'])
        )


class BoardNotFound(ValueError):
    pass


class TaskRepositoryFactory:
    def __init__(self, space, boards_repository):
        self.space = space
        self.boards_repository = boards_repository

    def create(self, board_pk):
        if not self.boards_repository.exists(board_pk):
            raise BoardNotFound()
        return TaskRepository(self.space.get_bucket(board_pk))


class BoardRepository:
    def __init__(self, board_bucket):
        self._boards = board_bucket

    @property
    def new(self):
        board_as_json = self._boards.add({})
        return Board(pk=board_as_json['id'])

    def exists(self, pk):
        try:
            self._boards.get(pk)
            return True
        except easydb_client.ElementNotFound:
            return False