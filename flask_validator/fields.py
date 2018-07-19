import re


class _BaseField:
    def __init__(self, validator_function=None, enum=None, required: bool=True, allow_null: bool=False):
        self.required = required
        self.enum = enum
        self.allow_null = allow_null
        self.validator_function = validator_function

    def validate(self, value):
        raise NotImplementedError()


class StringField(_BaseField):
    def __init__(self, allow_empty: bool=True, min_length: int=None, max_length: int=None, regex=None, **kwargs):
        self.allow_empty = allow_empty
        self.min_length = min_length
        self.max_length = max_length
        self.regex = re.compile(regex) if regex else None

        super(StringField, self).__init__(**kwargs)

    def validate(self, value):
        if not isinstance(value, str):
            return False

        if self.max_length is not None and len(value) > self.max_length:
            return False

        if self.min_length is not None and len(value) < self.min_length:
            return False

        if self.regex is not None and self.regex.match(value) is None:
            return False


class IntField(_BaseField):
    def __init__(self, min_value=None, max_value=None, **kwargs):
        self.min_value = min_value
        self.max_value = max_value

        super(IntField, self).__init__(**kwargs)

    def validate(self, value):
        if not isinstance(value, int):
            return False

        if self.min_value is not None and value < self.min_value:
            return False

        if self.max_value is not None and value > self.max_value:
            return False


class BooleanField(_BaseField):
    def validate(self, value):
        if not isinstance(value, bool):
            return False
