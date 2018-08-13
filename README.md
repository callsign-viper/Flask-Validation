# Flask-Validation [![Build Status](https://travis-ci.org/JoMingyu/Flask-Validation.svg?branch=master)](https://travis-ci.org/JoMingyu/Flask-Validation) [![Documentation Status](https://readthedocs.org/projects/flask-validate/badge/?version=latest)](https://flask-validate.readthedocs.io/en/latest/?badge=latest)

```bash
$ pip install flask-validation
```

Pythonic JSON payload validator for requested JSON payload of Flask

Flask를 위한 view decorator 기반의 JSON 요청 데이터 validation 라이브러리

## Example Usages
### json_required

```python
from flask import Flask
from flask_validation import json_required, Validator

app = Flask(__name__)
Validator(app)


@json_required()
@app.route('/', methods=('POST'))
def index():
    return 'hello!'
    
app.run()
```

```bash
$ curl -d '' -v http://localhost:5000
...
> POST / HTTP/1.1
> Content-Type: application/x-www-form-urlencoded
< HTTP/1.0 400 BAD REQUEST
$
$ curl -H "Content-Type: application/json" -d '' -v http://localhost:5000
...
> POST / HTTP/1.1
> Content-Type: application/x-www-form-urlencoded
< HTTP/1.0 200 OK
```

### validate_keys

```python
from flask import Flask
from flask_validation import validate_keys, Validator

app = Flask(__name__)
Validator(app)


@validate_keys(['name', 'age', { 'position': ['lati', 'longi'] }])
@app.route('/', methods=('POST'))
def index():
    return 'hello!'
    
app.run()
```

```bash
$ curl -H "Content-Type: application/json" -d '{"name": "PlanB"}' -v http://localhost:5000
...
> POST / HTTP/1.1
> Content-Type: application/x-www-form-urlencoded
< HTTP/1.0 400 BAD REQUEST
$
$ curl -H "Content-Type: application/json" -d '{"name": "PlanB", "age": 19, "position": {"lati": 35.24, "longi": 127.681146}}' -v http://localhost:5000
...
> POST / HTTP/1.1
> Content-Type: application/json
< HTTP/1.0 200 OK
```

### others

```python
from flask import Flask
from flask_validation import validate_common, validate_with_fields, validate_with_jsonschema, Validator

app = Flask(__name__)
Validator(app)


@validate_common({ 'name': str, 'age': int, { 'position': {'lati': float, 'longi': float} } })
@app.route('/1', methods=('POST'))
def validate_1():
    return 'hello!'


@validate_with_fields({
    'name': StringField(allow_empty=False, regex='[A-z ]+'),
    'age': IntField(min_value=0),
    'gender': StringField(required=False, enum=['M', 'F']),
    {
        'position': {
            'lati': NumberField(min_value=0),
            'longi': NumberField(min_value=0)
        }
    }
})
@app.route('/2', methods=('POST'))
def validate_2():
    return 'hello!'


@validate_with_jsonschema({
    'type': 'object',
    'properties': {
        'name': {'type': 'string'},
        'age': {'type': 'integer'},
        'position': {
            'type': 'object',
            'properties': {
                'lati': {'type': 'number'},
                'longi': {'type': 'number'}
            }
        }
    }
})
@app.route('/3', mehtods=('POST'))
def validate_3():
    return 'hello!'


app.run()
```

```bash
$ curl -H "Content-Type: application/json" -d '{"name": "PlanB", "age": 19, "position": {"lati": 35.24, "longi": 127.681146}}' -v http://localhost:5000/1
< HTTP/1.0 200 OK
$ curl -H "Content-Type: application/json" -d '{"name": "PlanB", "age": 19, "position": {"lati": 35.24, "longi": 127}}' -v http://localhost:5000/1
< HTTP/1.0 400 BAD REQUEST
$
$ curl -H "Content-Type: application/json" -d '{"name": "PlanB", "age": 19, "position": {"lati": 35, "longi": 127}}' -v http://localhost:5000/2
< HTTP/1.0 200 OK
$ curl -H "Content-Type: application/json" -d '{"name": "", "age": 19, "position": {"lati": 35, "longi": 127}}' -v http://localhost:5000/2
< HTTP/1.0 400 BAD REQUEST
$
$ curl -H "Content-Type: application/json" -d '{"name": "PlanB", "age": 19, "position": {"lati": 35, "longi": 127}}' -v http://localhost:5000/3
< HTTP/1.0 200 OK
$ curl -H "Content-Type: application/json" -d '{"name": "PlanB", "age": "19", "position": {"lati": 35, "longi": 127}}' -v http://localhost:5000/3
< HTTP/1.0 400 BAD REQUEST
```
