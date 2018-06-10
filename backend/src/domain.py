import enum
import uuid
import json
import requests as req


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

    def json(self, pk):
        return {
            'pk': pk,
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
            'pk': self.pk,
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
    def __init__(self, router_address, board_pk):
        self.board_pk = board_pk
        self.router_address = router_address

    @property
    def all(self):
        raw_tasks = json.loads(req.get(f'{self.router_address}/router/{self.board_pk}').text)
        return list(map(self._to_entity, raw_tasks))

    def add(self, create_task_dto):
        raw_tasks = json.loads(req.get(f'{self.router_address}/router/{self.board_pk}').text)
        pk = str(uuid.uuid4())
        raw_tasks.append(create_task_dto.json(pk))
        req.put(f'{self.router_address}/router/{self.board_pk}', json.dumps(raw_tasks))
        return self._to_entity(create_task_dto.json(pk))

    def delete(self, task_pk):
        raw_tasks = json.loads(req.get(f'{self.router_address}/router/{self.board_pk}').text)
        req.put(
            f'{self.router_address}/router/{self.board_pk}',
            json.dumps([t for t in raw_tasks if t['pk'] != task_pk])
        )

    def update(self, change_status_task_dto):
        self.delete(change_status_task_dto.pk)

        raw_tasks = json.loads(req.get(f'{self.router_address}/router/{self.board_pk}').text)
        raw_tasks.append(change_status_task_dto.json)
        req.put(f'{self.router_address}/router/{self.board_pk}', json.dumps(raw_tasks))
        return self._to_entity(change_status_task_dto.json)

    def _to_entity(self, task_as_json):
        return Task(
            task_as_json['pk'],
            task_as_json['body'],
            TaskStatus.of(task_as_json['status'])
        )


class BoardNotFound(ValueError):
    pass


class TaskRepositoryFactory:
    def __init__(self, router_address, boards_repository):
        self.router_address = router_address
        self.boards_repository = boards_repository

    def create(self, board_pk):
        if not self.boards_repository.exists(board_pk):
            raise BoardNotFound()
        return TaskRepository(self.router_address, board_pk)


class BoardRepository:
    def __init__(self, router_addresses):
        self.router_addresses = router_addresses
        self.BOARDS_KEY = 'boards'

    @property
    def new(self):
        boards = json.loads(req.get(f'{self.router_addresses}/router/{self.BOARDS_KEY}').text)
        pk = str(uuid.uuid4())
        boards.append(pk)
        req.put(f'{self.router_addresses}/router/{self.BOARDS_KEY}', json.dumps(boards))
        req.put(f'{self.router_addresses}/router/{pk}', json.dumps([]))
        return Board(pk)

    def exists(self, pk):
        resp = req.get(f'{self.router_addresses}/router/{self.BOARDS_KEY}')
        return resp.status_code == 200 and any(b == pk for b in json.loads(resp.text))