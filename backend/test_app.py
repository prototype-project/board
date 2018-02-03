from unittest import TestCase
import json

from src.app import app


class AppTestCase(TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_should_create_board(self):
        # when
        resp = self.app.post('/api/boards')

        # then
        self.assertEqual(resp.status_code, 200)

        # and
        data = json.loads(resp.data)
        self.assertIn('pk', data)

    def test_should_get_all_tasks_from_board(self):
        # given
        board_pk = json.loads(self.app.post('/api/boards').data)['pk']

        # when
        resp = self.app.get(f'/api/boards/{board_pk}/tasks')

        # then
        self.assertEqual([], json.loads(resp.data))

        # and
        self.assertEqual(resp.status_code, 200)

    def test_should_return_404_when_trying_to_get_nonexistent_board_tasks(self):
        # when
        resp = self.app.get('/api/boards/nonexistent/tasks')

        # then
        self.assertEqual(resp.status_code, 404)

    def test_should_add_task(self):
        # given
        board_pk = json.loads(self.app.post('/api/boards').data)['pk']

        # when
        resp = self.app.post(f'/api/boards/{board_pk}/tasks',
                             data=json.dumps({'body': 'testTask'}),
                             content_type='application/json')

        # then
        self.assertEqual(resp.status_code, 200)

        # and
        data = json.loads(resp.data)
        self.assertEqual(data['body'], 'testTask')
        self.assertEqual(data['status'], 'todo')
        self.assertIn('pk', data)

    def test_should_return_404_when_trying_to_add_task_to_nonexistent_board(self):
        pass