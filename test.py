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

    def test_200(self):
        client = self._get_test_client_of_decorated_view_function_registered_flask_app(self.target_func())

        resp = self._json_post_request(client)
        self.assertEqual(resp.status_code, 200)

    def test_abort(self):
        client = self._get_test_client_of_decorated_view_function_registered_flask_app(self.target_func())
        abort_code = self._get_default_argument_value(self.target_func, 0)

        resp = self._plain_post_request(client)
        self.assertEqual(resp.status_code, abort_code)


class TestValidateKeys(BaseTestCase):
    def setUp(self):
        self.target_func = validate_keys

    def test_200(self):
        client = self._get_test_client_of_decorated_view_function_registered_flask_app(self.target_func(['a', 'b', {'c': ['d', 'e']}]))

        resp = self._json_post_request(client, json={'a': 1, 'b': 1, 'c': {'d': 1, 'e': 1}})
        self.assertEqual(resp.status_code, 200)

    def test_abort(self):
        client = self._get_test_client_of_decorated_view_function_registered_flask_app(self.target_func(['a', 'b', {'c': ['d', 'e']}]))
        abort_code = self._get_default_argument_value(self.target_func, 0)

        resp = self._json_post_request(client, json={'a': 1, 'b': 1, 'c': {'d': 1}})
        self.assertEqual(resp.status_code, abort_code)


class TestValidateCommon
