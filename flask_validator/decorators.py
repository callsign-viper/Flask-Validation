from functools import wraps

from jsonschema import validate
from jsonschema.exceptions import ValidationError
from flask import abort, request

from .fields import _BaseField


def json_required(invalid_content_type_abort_code: int=406):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if not request.is_json:
                abort(invalid_content_type_abort_code)

            return fn(*args, **kwargs)
        return wrapper
    return decorator


def validate_keys(required_keys, key_missing_abort_code: int=400):
    # ['a', 'b', {'c': ['q' ,'z']}]
    def _validate_keys(src, keys):
        for key in keys:
            if isinstance(key, str):
                if key not in src:
                    abort(key_missing_abort_code)
            elif isinstance(key, dict):
                for k, v in key.items():
                    if k not in src:
                        abort(key_missing_abort_code)
                    _validate_keys(src[k], v)

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if request.is_json and required_keys:
                _validate_keys(request.json, required_keys)

            return fn(*args, **kwargs)
        return wrapper
    return decorator


def validate_common(key_type_mapping: dict, key_missing_abort_code: int=400, invalid_type_abort_code: int=400):
    # {'a': str, 'b': int, 'c': {'d': int, 'e': str}}
    def validate_key_and_type(src, mapping):
        for key, typ in mapping.items():
            if key not in src:
                abort(key_missing_abort_code)

            if isinstance(typ, type):
                if type(src[key]) is not typ:
                    abort(invalid_type_abort_code)
            elif isinstance(typ, dict):
                if not isinstance(src[key], dict):
                    abort(invalid_type_abort_code)

                validate_key_and_type(src[key], typ)

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if request.is_json and key_type_mapping:
                validate_key_and_type(request.json, key_type_mapping)

            return fn(*args, **kwargs)
        return wrapper
    return decorator


def validate_with_fields(key_field_mapping: dict, key_missing_abort_code: int=400, validation_failure_abort_code: int=400):
    # {'a': StringField(allow_empty=False), 'b': IntField(min_value=0), 'c': {'d': BooleanField()}}
    def _validate_with_fields(src, mapping):
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

                    print(value)
                    print(field.validate(value))
                    if field.validate(value) is False:
                        abort(validation_failure_abort_code)
            elif isinstance(field, dict):
                if key not in src:
                    abort(key_missing_abort_code)

                if not isinstance(src[key], dict):
                    abort(validation_failure_abort_code)

                _validate_with_fields(src[key], field)

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if request.is_json and key_field_mapping:
                _validate_with_fields(request.json, key_field_mapping)

            return fn(*args, **kwargs)
        return wrapper
    return decorator


def validate_with_jsonschema(jsonschema: dict, validation_error_abort_code: int=400):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if request.is_json:
                try:
                    validate(request.json, jsonschema)
                except ValidationError:
                    abort(validation_error_abort_code)

            return fn(*args, **kwargs)
        return wrapper
    return decorator
