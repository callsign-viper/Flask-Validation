Usages
=======

json_required
-------------

.. code-block:: python

   from flask import Flask
   from flask_validator import json_required, Validator

   app = Flask(__name__)
   Validator(app)


   @json_required
   @app.route('/', methods=('POST'))
   def index():
       return 'hello!'

validate_keys
--------------

.. code-block:: python

   from flask import Flask
   from flask_validator import validate_keys, Validator

   app = Flask(__name__)
   Validator(app)


   @validate_keys(['name', 'age', {'position': ['latitude', 'longitude']}])
   @app.route('/', methods=('POST'))
   def index():
       return 'hello!'

validate_common
----------------

.. code-block:: python

   from flask import Flask
   from flask_validator import validate_common, Validator

   app = Flask(__name__)
   Validator(app)


   @validate_common({'name': str, 'age': int, 'position': {'latitude': float, 'longitude': float}})
   @app.route('/', methods=('POST'))
   def index():
       return 'hello!'

validate_with_fields
---------------------

.. code-block:: python

   from flask import Flask
   from flask_validator import validate_with_fields
   from flask_validator import StringField, IntField
   from flask_Validator import Validator

   app = Flask(__name__)
   Validator(app)


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

validate_with_jsonschema
-------------------------

.. code-block:: python

   from flask import Flask
   from flask_validator import validate_with_jsonschema, Validator

   app = Flask(__name__)
   Validator(app)


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