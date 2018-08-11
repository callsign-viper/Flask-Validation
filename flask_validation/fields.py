import re


class _BaseField:
    """
    Base field class
    """
    def __init__(self, validator_function=None, enum=None, required: bool=True, allow_null: bool=False):
        self.required = required
        self.enum = enum
        self.allow_null = allow_null
        self.validator_function = validator_function

    def validate(self, value):
        if self.enum is not None and value not in self.enum:
            return False

        # allow_null은 decorators.py에서 체크

        if self.validator_function is not None and not self.validator_function(value):
            return False


class StringField(_BaseField):
    """
    String field class
    """
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

        return super(StringField, self).validate(value)


class NumberField(_BaseField):
    """
    Number field class
    """
    def __init__(self, min_value=None, max_value=None, **kwargs):
        self.min_value = min_value
        self.max_value = max_value

        super(NumberField, self).__init__(**kwargs)

    def validate(self, value):
        if self.min_value is not None and value < self.min_value:
            return False

        if self.max_value is not None and value > self.max_value:
            return False

        return super(NumberField, self).validate(value)


class IntField(NumberField):
    """
    Int field class
    """
    def validate(self, value):
        if not isinstance(value, int):
            return False
        
        return super(IntField, self).validate(value)


class FloatField(NumberField):
    """
    Float field class
    """
    def validate(self, value):
        if not isinstance(value, float):
            return False
        
        return super(FloatField, self).validate(value)


class BooleanField(_BaseField):
    """
    Boolean field class
    """
    def validate(self, value):
        if not isinstance(value, bool):
            return False
        
        return super(BooleanField, self).validate(value)


class ListField(_BaseField):
    """
    List field class
    """
    def __init__(self, min_length: int=None, max_length: int=None, **kwargs):
        self.min_length = min_length
        self.max_length = max_length

        super(ListField, self).__init__(**kwargs)

    def validate(self, value):
        if not isinstance(value, list):
            return False

        if self.max_length is not None and len(value) > self.max_length:
            return False

        if self.min_length is not None and len(value) < self.min_length:
            return False

        return super(ListField, self).validate(value)
