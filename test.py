from unittest import TestCase

from flask import Flask
from flask.testing import FlaskClient

from flask_validation import common_regex as cr
from flask_validation import *


class BaseTestCase(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def _get_test_client_of_decorated_view_function_registered_flask_app(self, decorator_func) -> FlaskClient:
        def view_func():
            return 'hello'

        decorated_view_func = decorator_func(view_func)
        app = Flask(__name__)
        Validator(app)

        app.add_url_rule('/', view_func=decorated_view_func, methods=['POST'])

        return app.test_client()

    def _json_post_request(self, client, *args, **kwargs):
        return client.post('/', headers={'Content-Type': 'application/json'}, *args, **kwargs)

    def _plain_post_request(self, client, *args, **kwargs):
        return client.post('/', headers={'Content-Type': 'text/plain'}, *args, **kwargs)


class TestJsonRequired(BaseTestCase):
    def setUp(self):
        self.target_func = json_required
        self.client = self._get_test_client_of_decorated_view_function_registered_flask_app(self.target_func())

    def test_200(self):
        resp = self._json_post_request(self.client)
        self.assertEqual(resp.status_code, 200)

    def test_invalid_content_type(self):
        resp = self._plain_post_request(self.client)
        self.assertEqual(resp.status_code, 406)


class TestValidateKeys(BaseTestCase):
    def setUp(self):
        self.target_func = validate_keys
        self.client = self._get_test_client_of_decorated_view_function_registered_flask_app(self.target_func([
            'a',
            'b',
            {
                'c': [
                    'd', 'e'
                ]
            }
        ]))

    def test_200(self):
        resp = self._json_post_request(self.client, json={'a': 1, 'b': 1, 'c': {'d': 1, 'e': 1}})
        self.assertEqual(resp.status_code, 200)

    def test_key_missing(self):
        resp = self._json_post_request(self.client, json={'a': 1, 'b': 1, 'c': {'d': 1}})
        self.assertEqual(resp.status_code, 400)


class TestValidateCommon(BaseTestCase):
    def setUp(self):
        self.target_func = validate_common
        self.client = self._get_test_client_of_decorated_view_function_registered_flask_app(self.target_func({
            'a': str,
            'b': int,
            'c': {
                'd': int
            }
        }))

    def test_200(self):
        resp = self._json_post_request(self.client, json={'a': 'a', 'b': 1, 'c': {'d': 1}})
        self.assertEqual(resp.status_code, 200)

    def test_key_missing(self):
        resp = self._json_post_request(self.client, json={'a': 'a', 'b': 1})
        self.assertEqual(resp.status_code, 400)

    def test_invalid_type(self):
        resp = self._json_post_request(self.client, json={'a': 'a', 'b': 1, 'c': {'d': 'a'}})
        self.assertEqual(resp.status_code, 400)


class TestValidateWithFields(BaseTestCase):
    def setUp(self):
        self.target_func = validate_with_fields
        self.client = self._get_test_client_of_decorated_view_function_registered_flask_app(self.target_func({
            'a': StringField(max_length=10),
            'b': IntField(min_value=0),
            'c': FloatField(min_value=3.8),
            'd': ListField(max_length=10),
            'e': {
                'f': BooleanField(allow_null=True)
            }
        }))

    def test_200(self):
        resp = self._json_post_request(self.client, json={'a': 'a', 'b': 1, 'c': 6.5, 'd': [1, 2, 3], 'e': {'f': None}})
        self.assertEqual(resp.status_code, 200)

    def test_key_missing(self):
        resp = self._json_post_request(self.client, json={'a': 'a'})
        self.assertEqual(resp.status_code, 400)

    def test_validation_failure(self):
        resp = self._json_post_request(self.client, json={'a': 'a', 'b': 1, 'c': 1.5, 'd': [1, 2, 3], 'e': {'f': None}})
        self.assertEqual(resp.status_code, 400)


class TestValidateWithJsonSchema(BaseTestCase):
    def setUp(self):
        self.target_func = validate_with_jsonschema
        self.client = self._get_test_client_of_decorated_view_function_registered_flask_app(self.target_func({
            'type': 'object',
            'properties': {
                'a': {'type': 'string'},
                'b': {'type': 'number'},
                'c': {
                    'type': 'object',
                    'properties': {
                        'd': {'type': 'number'}
                    }
                }
            }
        }))

    def test_200(self):
        resp = self._json_post_request(self.client, json={'a': 'a', 'b': 1, 'c': {'d': 1}})
        self.assertEqual(resp.status_code, 200)

    def test_validation_error(self):
        resp = self._json_post_request(self.client, json={'a': 'a', 'b': 1, 'c': {'d': 'a'}})

        self.assertEqual(resp.status_code, 400)


class TestValidateWithCommonRegex(BaseTestCase):
    def setUp(self):
        self.target_func = validate_with_fields
        self.client = self._get_test_client_of_decorated_view_function_registered_flask_app(self.target_func({
            'email': StringField(regex=cr.email),
            'url': StringField(regex=cr.url),
            'visa_card': StringField(regex=cr.visa_card),
            'master_card': StringField(regex=cr.master_card),
            'isbn': StringField(regex=cr.isbn),
            'hex': StringField(regex=cr.hex),
            'ipv4': StringField(regex=cr.ipv4),
            'digit': StringField(regex=cr.digit),
            'date': StringField(regex=cr.date)
        }))

    def test_200(self):
        resp = self._json_post_request(self.client, json={
            'email': 'viper@istruly.sexy',
            'url': 'https://www.google.com/',
            'visa_card': '4000 1234 5678 9010',
            'master_card': '5412 5412 5412 5412',
            'isbn': '9791160501308',
            'hex': '#ffb2d9',
            'ipv4': '127.0.0.1',
            'digit': '20010420',
            'date': '2018/04/20'
        })
        self.assertEqual(resp.status_code, 200)

    def test_validation_error(self):
        resp = self._json_post_request(self.client, json={
            'email': 'https://www.google.com/',
            'url': 'viper@istruly.sexy',
            'visa_card': '5412 5412 5412 5412',
            'master_card': '4000 1234 5678 9010',
            'isbn': '#ffb2d9',
            'hex': '9791160501308',
            'ipv4': '2018/04/20',
            'digit': '127.0.0.1',
            'date': '20010420'
        })
        self.assertEqual(resp.status_code, 400)
