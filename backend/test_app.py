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
        # when
        resp = self.app.post('/api/boards/nonexistent/tasks',
                             data=json.dumps({'body': 'testTask'}),
                             content_type='application/json')

        # then
        self.assertEqual(resp.status_code, 404)

    def test_should_return_400_when_trying_to_add_task_by_sending_invalid_data(self):
        # given
        board_pk = json.loads(self.app.post('/api/boards').data)['pk']

        # when
        resp = self.app.post(f'/api/boards/{board_pk}/tasks',
                             data='{]}}',
                             content_type='application/json')

        # then
        self.assertEqual(resp.status_code, 400)

        # when
        resp = self.app.post(f'/api/boards/{board_pk}/tasks',
                             data=json.dumps({'invalid': 'data'}),
                             content_type='application/json')

        # then
        self.assertEqual(resp.status_code, 400)

    def test_should_delete_task(self):
        # given
        board_pk = json.loads(self.app.post('/api/boards').data)['pk']

        # and
        task_pk = json.loads(self.app.post(f'/api/boards/{board_pk}/tasks',
                                           data=json.dumps({'body': 'testTask'}),
                                           content_type='application/json').data)['pk']

        # when
        resp = self.app.delete(f'/api/boards/{board_pk}/tasks/{task_pk}')

        # and
        self.assertEqual(resp.status_code, 200)

    def test_should_return_404_when_trying_to_delete_task_from_nonexistent_board(self):
        # when
        resp = self.app.delete('/api/boards/nonexistentBoard/tasks/someTask')

        # and
        self.assertEqual(resp.status_code, 404)

    def test_should_return_404_when_trying_to_delete_nonexistent_task(self):
        # given
        board_pk = json.loads(self.app.post('/api/boards').data)['pk']

        # when
        resp = self.app.delete(f'/api/boards/{board_pk}/tasks/someTask')

        # and
        self.assertEqual(resp.status_code, 404)

    def test_should_update_task(self):
        # given
        board_pk = json.loads(self.app.post('/api/boards').data)['pk']

        # and
        task_pk = json.loads(self.app.post(f'/api/boards/{board_pk}/tasks',
                                           data=json.dumps({'body': 'testTask'}),
                                           content_type='application/json').data)['pk']

        # when
        resp = self.app.put(f'/api/boards/{board_pk}/tasks/{task_pk}',
                     content_type='application/json',
                     data=json.dumps({'status': 'done', 'body': 'new body'}))

        # then
        self.assertEqual(resp.status_code, 200)

    def test_should_return_404_when_trying_to_update_task_from_nonexistent_board(self):
        # when
        resp = self.app.put(f'/api/boards/nonexistentBoard/tasks/someTask',
                            content_type='application/json',
                            data=json.dumps({'status': 'done', 'body': 'new body'}))

        # then
        self.assertEqual(resp.status_code, 404)

    def test_should_return_404_when_trying_to_update_nonexistent_task(self):
        # given
        board_pk = json.loads(self.app.post('/api/boards').data)['pk']

        # when
        resp = self.app.put(f'/api/boards/{board_pk}/tasks/someTask',
                            content_type='application/json',
                            data=json.dumps({'status': 'done', 'body': 'new body'}))

        # then
        self.assertEqual(resp.status_code, 404)

    def test_should_return_400_when_trying_to_update_task_to_unknown_status(self):
        # given
        board_pk = json.loads(self.app.post('/api/boards').data)['pk']

        # and
        task_pk = json.loads(self.app.post(f'/api/boards/{board_pk}/tasks',
                                           data=json.dumps({'body': 'testTask'}),
                                           content_type='application/json').data)['pk']

        # when
        resp = self.app.put(f'/api/boards/{board_pk}/tasks/{task_pk}',
                            content_type='application/json',
                            data=json.dumps({'status': 'invalidStatus', 'body': 'new body'}))

        # then
        self.assertEqual(resp.status_code, 400)

    def test_should_return_400_when_trying_to_update_task_by_sending_invalid_data(self):
        # given
        board_pk = json.loads(self.app.post('/api/boards').data)['pk']

        # and
        task_pk = json.loads(self.app.post(f'/api/boards/{board_pk}/tasks',
                                           data=json.dumps({'body': 'testTask'}),
                                           content_type='application/json').data)['pk']

        # when
        resp = self.app.put(f'/api/boards/{board_pk}/tasks/{task_pk}',
                            content_type='application/json',
                            data='{[')

        # then
        self.assertEqual(resp.status_code, 400)