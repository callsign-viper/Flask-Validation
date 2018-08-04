from unittest import TestCase

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

    def _json_post_request(self, client, *args, **kwargs):
        return client.post('/', headers={'Content-Type': 'application/json'}, *args, **kwargs)

    def _plain_post_request(self, client, *args, **kwargs):
        return client.post('/', headers={'Content-Type': 'text/plain'}, *args, **kwargs)

