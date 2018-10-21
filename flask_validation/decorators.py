from functools import wraps

from jsonschema import validate
from jsonschema.exceptions import ValidationError
from flask import abort, request, current_app

from .fields import _BaseField


def json_required(fn):
    """
    A decorator to check header type is ``application/json``

    if you decorate endpoint with this, it will ensure that the request has a valid payload type before access endpoint
    if header's content type is not ``application/json``, abort the ``invalid_content_type_abort_code``
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        invalid_content_type_abort_code = current_app.config['INVALID_CONTENT_TYPE_ABORT_CODE']
        if not request.is_json:
            abort(invalid_content_type_abort_code)

        return fn(*args, **kwargs)
    return wrapper


def validate_keys(required_keys):
    """
    A decorator to check request payload keys

    if you decorate endpoint with this, it will ensure that the request's json body includes '`required_keys'`.
    if request body didn't includes ``required_keys`` , abort with  ``key_missing_abort_code``

    Nested JSON processing is possible by inserting the dictionary in the  ``required_keys``
    like this ``['a', 'b', {'c': ['q' ,'z']}]``

    :param required_keys: key list to check request body's JSON
    """
    # ['a', 'b', {'c': ['q' ,'z']}]

    def _validate_keys(src, keys, key_missing_abort_code):
        for key in keys:
            if isinstance(key, str):
                if key not in src:
                    abort(key_missing_abort_code)
            elif isinstance(key, dict):
                for k, v in key.items():
                    if k not in src:
                        abort(key_missing_abort_code)
                    _validate_keys(src[k], v, key_missing_abort_code)

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            key_missing_abort_code = current_app.config['KEY_MISSING_ABORT_CODE']
            if request.is_json and required_keys:
                _validate_keys(request.json, required_keys, key_missing_abort_code)

            return fn(*args, **kwargs)
        return wrapper
    return decorator


def validate_common(key_type_mapping: dict):
    """
    A decorator to check request payload keys and type

    If the request payload does not include the key in  ``key_type_mapping``, abort the  ``key_missing_code``,
    and if the type is not correct, abort the  ``invalid_type_code``.

    Nested JSON processing is possible by inserting the dictionary in the  ``required_keys``
    like this ``{'a': str, 'b': int, 'c': {'d': int, 'e': str}}``


    :param key_type_mapping: A dictionary for payload check with this form ``{<key name>: <type class>}``
    """
    # {'a': str, 'b': int, 'c': {'d': int, 'e': str}}

    def validate_key_and_type(src, mapping, key_missing_abort_code, invalid_type_abort_code):
        for key, typ in mapping.items():
            if key not in src:
                abort(key_missing_abort_code)

            if isinstance(typ, type):
                if type(src[key]) is not typ:
                    abort(invalid_type_abort_code)
            elif isinstance(typ, dict):
                if not isinstance(src[key], dict):
                    abort(invalid_type_abort_code)

                validate_key_and_type(src[key], typ, key_missing_abort_code, invalid_type_abort_code)

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            key_missing_abort_code = current_app.config['KEY_MISSING_ABORT_CODE']
            invalid_type_abort_code = current_app.config['INVALID_TYPE_ABORT_CODE']
            if request.is_json and key_type_mapping:
                validate_key_and_type(request.json, key_type_mapping, key_missing_abort_code, invalid_type_abort_code)

            return fn(*args, **kwargs)
        return wrapper
    return decorator


def validate_with_fields(key_field_mapping: dict):
    """
    A decorator to check request payload with Field classes in fields.py

    If the request payload does not include the key in key_type_mapping, abort  ``key_missing_code``
    and abort  ``validation_failure_code`` if field validation fails.

    Nested JSON processing is possible by inserting the dictionary in the  ``required_keys``
    like this ``{'a': StringField(allow_empty=False), 'b': IntField(min_value=0), 'c': {'d': BooleanField()}}``

    :param key_field_mapping: A dictionary for payload check with this form ``{<key name>: <field class>}``
    """
    # {'a': StringField(allow_empty=False), 'b': IntField(min_value=0), 'c': {'d': BooleanField()}}

    def _validate_with_fields(src, mapping, key_missing_abort_code, validation_failure_abort_code):
        for key, field in mapping.items():
            if isinstance(field, _BaseField):
                if field.required and key not in src:
                    # required일 때만 not in에 대해 abort
                    abort(key_missing_abort_code)

                if key in src:
                    # required가 True던 False던, 들어 있으면 validate
                    value = src[key]

                    if field.allow_null:
                        if value is None:
                            # nullable하고, 실제로 value가 null이라면 validation 필요 x
                            continue

                    if field.validate(value) is False:
                        abort(validation_failure_abort_code)
            elif isinstance(field, dict):
                if key not in src:
                    abort(key_missing_abort_code)

                if not isinstance(src[key], dict):
                    abort(validation_failure_abort_code)

                _validate_with_fields(src[key], field, key_missing_abort_code, validation_failure_abort_code)

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            key_missing_abort_code = current_app.config['KEY_MISSING_ABORT_CODE']
            validation_failure_abort_code = current_app.config['VALIDATION_FAILURE_ABORT_CODE']
            if request.is_json and key_field_mapping:
                _validate_with_fields(request.json, key_field_mapping, key_missing_abort_code, validation_failure_abort_code)

            return fn(*args, **kwargs)
        return wrapper
    return decorator


def validate_with_jsonschema(jsonschema: dict):
    """
    A decorator to check request payload with jsonschema

    If validation fails(jsonschema.exceptions.ValidationError raised), abort the  ``validation_error_abort_code``.

    :param jsonschema: jsonschema
    """

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            validation_error_abort_code = current_app.config['VALIDATION_ERROR_ABORT_CODE']
            if request.is_json:
                try:
                    validate(request.json, jsonschema)
                except ValidationError:
                    abort(validation_error_abort_code)

            return fn(*args, **kwargs)
        return wrapper
    return decorator
