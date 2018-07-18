from functools import wraps

from flask import abort, request


def validate_common(
        key_type_mapping: dict, # {'': type, '': type, ...}
        code_when_content_type_is_not_json=406,
        key_missing_code=400,
        invalid_type_code=400):

    def validate_key_and_type(src, mapping):
        for key, typ in mapping.items():
            if key not in src:
                # 전형적인 bad request
                abort(key_missing_code)
            elif type(src[key]) is not typ:
                abort(invalid_type_code)

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if not request.is_json:
                abort(code_when_content_type_is_not_json)
            else:
                if key_type_mapping:
                    validate_key_and_type(request.json, key_type_mapping)

            return fn(*args, **kwargs)
        return wrapper
    return decorator


def validate_keys(
        required_keys, # ['a', 'b', 'c', 'd']
        code_when_content_type_is_not_json=406,
        key_missing_code=400):

    def _validate_keys(src, keys):
        for key in keys:
            if key not in src:
                abort(key_missing_code)

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if not request.is_json:
                abort(code_when_content_type_is_not_json)
            else:
                if required_keys:
                    _validate_keys(request.json, required_keys)

            return fn(*args, **kwargs)
        return wrapper
    return decorator
