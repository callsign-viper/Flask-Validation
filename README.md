# Flask-Validator-Extended [![Build Status](https://travis-ci.org/JoMingyu/Flask-Validator.svg?branch=master)](https://travis-ci.org/JoMingyu/Flask-Validator)
Pythonic JSON payload validator for requested JSON payload of Flask

Flask를 위한 view decorator 기반의 JSON 요청 데이터 validation 라이브러리. [Flask Large Application Example](https://github.com/JoMingyu/Flask-Large-Application-Example)에서 직접 구현해 사용하던 몇 가지 view decorator에서 출발했고, [MongoEngine](https://github.com/MongoEngine/mongoengine)의 설계에 영향을 받았습니다.

## Usages
### json_required(invalid_content_type_code: int=406)
요청 헤더의 content type이 application/json이 아닌 경우, `invalid_content_type_code`를 abort합니다.

```
from flask import Flask
from flask_validator import json_required

app = Flask(__name__)


@json_required()
@app.route('/', methods=('POST'))
def index():
    return 'hello!'
```

### validate_keys(required_keys, key_missing_code: int=400)
요청 payload에 required_keys가 포함되어 있지 않으면, `key_missing_code`를 abort합니다.

```
from flask import Flask
from flask_validator import validate_keys

app = Flask(__name__)


@validate_keys(['name', 'age'])
@app.route('/', methods=('POST'))
def index():
    return 'hello!'
```

Iterable 내부의 dictionary로 nested JSON 처리가 가능합니다.

```
from flask import Flask
from flask_validator import validate_keys

app = Flask(__name__)


@validate_keys(['name', 'age', {'position': ['latitude', 'longitude']}])
@app.route('/', methods=('POST'))
def index():
    return 'hello!'
```

### validate_common(key_type_mapping: dict, key_missing_code: int=400, invalid_type_code: int=400)
key와 타입을 함께 검사합니다. 요청 payload에 key_type_mapping에서의 key가 포함되어 있지 않으면 `key_missing_code`를, 타입이 맞지 않으면 `invalid_type_code`를 abort합니다.

```
from flask import Flask
from flask_validator import validate_common

app = Flask(__name__)


@validate_common({'name': str, 'age': int})
@app.route('/', methods=('POST'))
def index():
    return 'hello!'
```

value를 dictionary로 주어 nested JSON 처리가 가능합니다.

```
from flask import Flask
from flask_validator import validate_common

app = Flask(__name__)


@validate_common({'name': str, 'age': int, 'position': {'latitude': float, 'longitude': float}})
@app.route('/', methods=('POST'))
def index():
    return 'hello!'
```

### validate_with_fields(key_field_mapping: dict, key_missing_code: int=400, validation_failure_code: int=400)
속성을 정의할 수 있는 필드 클래스들을 이용한 validation입니다. 요청 payload에 key_type_mapping에서의 key가 포함되어 있지 않으면 `key_missing_code`를, validation에 실패하면 `validation_failure_code`를 abort합니다.

```
from flask import Flask
from flask_validator import validate_with_fields
from flask_validator import StringField, IntField

app = Flask(__name__)


@validate_with_fields({'name': StringField(allow_empty=False, regex='[가-힇]+'), 'age': IntField(min_value=0)})
@app.route('/', methods=('POST'))
def index():
    return 'hello!'
```

value를 dictionary로 주어 nested JSON 처리가 가능합니다.

```
from flask import Flask
from flask_validator import validate_with_fields
from flask_validator import StringField, IntField

app = Flask(__name__)


@validate_with_fields({
    'name': StringField(allow_empty=False, regex='[가-힇]+'),
    'age': IntField(min_value=0),
    'position': {
        'latitude': FloatField(min_value=-90, max_value=90),
        'longitude': FloatField(min_value=-180, max_value=180)
    }
})
@app.route('/', methods=('POST'))
def index():
    return 'hello!'
```

### validate_with_jsonschema(jsonschema: dict, validation_error_abort_code: int=400)
[jsonschema](https://github.com/Julian/jsonschema)를 이용한 validation입니다. validation에 실패할 경우(jsonschema.exceptions.ValidationError가 raise되는 경우) `validation_error_abort_code`를 abort합니다.

```
from flask import Flask
from flask_validator import validate_with_jsonschema

app = Flask(__name__)


@validate_with_jsonschema({
    'type': 'object',
    'properties': {
        'name': {'type': 'string'},
        'age': {'type': 'number'}
    }
})
@app.route('/', methods=('POST'))
def index():
    return 'hello!'
```
