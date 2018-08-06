from unittest import TestCase
import inspect

from flask import Flask
from flask.testing import FlaskClient

from flask_validator import *


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

        app.add_url_rule('/', view_func=decorated_view_func, methods=['POST'])

        return app.test_client()

    def _get_default_argument_value(self, func, position):
        return inspect.getfullargspec(func).defaults[position]

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

    def test_abort(self):
        abort_code = self._get_default_argument_value(self.target_func, 0)

        resp = self._plain_post_request(self.client)
        self.assertEqual(resp.status_code, abort_code)


class TestValidateKeys(BaseTestCase):
    def setUp(self):
        self.target_func = validate_keys
        self.client = self._get_test_client_of_decorated_view_function_registered_flask_app(self.target_func(['a', 'b', {'c': ['d', 'e']}]))

    def test_200(self):
        resp = self._json_post_request(self.client, json={'a': 1, 'b': 1, 'c': {'d': 1, 'e': 1}})
        self.assertEqual(resp.status_code, 200)

    def test_key_missing(self):
        key_missing_abort_code = self._get_default_argument_value(self.target_func, 0)

        resp = self._json_post_request(self.client, json={'a': 1, 'b': 1, 'c': {'d': 1}})
        self.assertEqual(resp.status_code, key_missing_abort_code)


class TestValidateCommon(BaseTestCase):
    def setUp(self):
        self.target_func = validate_common
        self.client = self._get_test_client_of_decorated_view_function_registered_flask_app(self.target_func({'a': str, 'b': int, 'c': {'d': int}}))

    def test_200(self):
        resp = self._json_post_request(self.client, json={'a': 'a', 'b': 1, 'c': {'d': 1}})
        self.assertEqual(resp.status_code, 200)

    def test_key_missing(self):
        key_missing_abort_code = self._get_default_argument_value(self.target_func, 0)

        resp = self._json_post_request(self.client, json={'a': 'a', 'b': 1, 'c': {'d': 'a'}})
        self.assertEqual(resp.status_code, key_missing_abort_code)
