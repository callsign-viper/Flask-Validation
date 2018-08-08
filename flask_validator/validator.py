class Validator(object):
    """
    Create the Validator instance to register config. You can either pass a flask application in directly
    here to register this extension with the flask app, or call init_app after creating
    this object (in a factory pattern).
    :param app: A flask application
    """
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self._set_default_configuration_options(app)

    @staticmethod
    def _set_default_configuration_options(app):
        app.config.setdefault('INVALID_CONTENT_TYPE_ABORT_CODE', 406)
        app.config.setdefault('KEY_MISSING_ABORT_CODE', 400)
        app.config.setdefault('INVALID_TYPE_ABORT_CODE', 400)
        app.config.setdefault('VALIDATION_FAILURE_ABORT_CODE', 400)
        app.config.setdefault('VALIDATION_ERROR_ABORT_CODE', 400)
