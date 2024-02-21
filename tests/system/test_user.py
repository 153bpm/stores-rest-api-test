import json
from models.user import UserModel
from tests.base_test import BaseTest


class UserTest(BaseTest):
    def test_register_user(self):
        with self.app() as client, self.app_context():
            # Convert the data to JSON format
            data = {'username': 'test', 'password': '1234'}
            json_data = json.dumps(data)

            # Use the content_type parameter to specify JSON
            response = client.post('/register', data=json_data, headers={'Content-Type': 'application/json'})

            self.assertEqual(response.status_code, 201)
            self.assertIsNotNone(UserModel.find_by_username('test'))
            self.assertDictEqual({'message': 'User created successfully'}, json.loads(response.data))

    def test_register_and_login(self):
        with self.app() as client, self.app_context():
            data = {'username': 'test', 'password': '1234'}
            json_data = json.dumps(data)

            client.post('/register', data=json_data, headers={'Content-Type': 'application/json'})
            auth_request = client.post('/auth',
                                       data=json.dumps({'username': 'test', 'password': '1234'}),
                                       headers={'Content-Type': 'application/json'})

            self.assertIn('access_token', json.loads(auth_request.data).keys())

    def test_register_duplicate_user(self):
        with self.app() as client, self.app_context():
            json_data = json.dumps({'username': 'test', 'password': '1234'})

            client.post('/register', data=json_data, headers={'Content-Type': 'application/json'})
            response = client.post('/register', data=json_data, headers={'Content-Type': 'application/json'})

            self.assertEqual(response.status_code, 400)
            self.assertDictEqual({'message': 'A user with that username already exists'},
                                 json.loads(response.data))