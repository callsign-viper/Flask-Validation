# Contributing

Thank you for your interest! Flask-Validation is always looking for contributors. If you
don't feel comfortable contributing code, adding docstrings to the source files
is very appreciated.

We are committed to providing a friendly, safe and welcoming environment for all,
regardless of gender, sexual orientation, disability, ethnicity, religion,
or similar personal characteristic.
Our [code of conduct](./CONDUCT.md) sets the standards for behavior.

## Installation

To develop on sanic (and mainly to just run the tests) it is highly recommend to
install from sources.

So assume you have already cloned the repo and are in the working directory with
a virtual environment already set up, then run:

```bash
pip3 install -r requirements.txt
```

## Running tests

To run the tests for sanic it is recommended to use tox like so:
'''bash
python3 -m unittest test.py
'''

See it's that simple!

## Pull requests!

So the pull request approval rules are pretty simple:
1. All pull requests must pass unit tests.
2. All pull requests must be reviewed and approved by at least
one current collaborator on the project.
3. All pull requests must pass flake8 checks.
4. All pull requests must be consistent with the existing code.
5. If you decide to remove/change anything from any common interface
a deprecation message should accompany it.
6. If you implement a new feature you should have at least one unit
test to accompany it.

## Documentation

Flask-Validation's documentation is built
To generate the documentation from scratch:

```bash
cd docs && make html
```

The HTML documentation will be created in the `docs/_build` folder.
