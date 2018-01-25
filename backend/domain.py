import enum


class TaskStatus(enum.Enum):
    TODO = 'todo'
    IN_PROGRESS = 'in_progress'
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
        self.status = status

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
        self._tasks.remove(task_pk)

    def update(self, change_status_task_dto):
        self._tasks.update(change_status_task_dto.pk, change_status_task_dto.json)

    def _to_entity(self, task_as_json):
        return Task(
            task_as_json['id'],
            task_as_json['fields']['body'],
            TaskStatus.of(task_as_json['fields']['status'])
        )


class BoardRepository:
    def __init__(self, board_bucket):
        self._boards = board_bucket

    @property
    def new(self):
        board_as_json = self._boards.add({})
        return Board(pk=board_as_json['id'])