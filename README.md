
# Flask-DSwagger

[![Build Status](https://travis-ci.org/abassel/mongosafe.svg?branch=master)](https://travis-ci.org/abassel/mongosafe)
[![Coverage Status](https://coveralls.io/repos/github/abassel/mongosafe/badge.svg?branch=master)](https://coveralls.io/github/abassel/mongosafe?branch=master)
[![PyPI version](https://badge.fury.io/py/mongosafe.svg)](https://badge.fury.io/py/mongosafe)
[![PyPI](https://img.shields.io/pypi/wheel/Django.svg)](https://pypi.python.org/pypi/mongosafe)


Provides safe reference fields for Mongoengine and Flask-admin dashboard without the need to migrate to MongoMallard!
It is heavily based(stolen) on MongoMallard.


[Mongoengine](https://github.com/MongoEngine/mongoengine) is an ORM-like layer on top of PyMongo.

[Flask-admin](https://github.com/flask-admin/flask-admin) is a simple and extensible administrative interface framework for Flask.

[MongoMallard](https://hack.close.io/posts/mongomallard) is a fast ORM based on MongoEngine

> Please note: This may not be the fastest way to manipulate data but it protects you from null references that will break Flask-admin.

## Install

```bash
pip install Flask-DSwagger
```

## Example

In the example bellow, Flask-DSwagger will generate automatically an OpenAPI 2.0 spec endpoint:

```python

from flask import Flask
app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello World!"


@app.route('/api/hello/<name>')
def hello_name(name):
    """
    "/hello":   # Must start for forward slash
        get:

            summary: "Endpoint to return information about logged user"

            description: "List information about your self!"

            tags: ["me"]

            produces:
              - "application/json"

            responses:
              "200":
                description: "Success response"
                schema:
                  $ref: "#/definitions/User"
              default:
                description: "unexpected error"
                schema:
                  $ref: "#/definitions/ErrorModel"

    """
    return "Hello {}!".format(name)


api_swag.generate(db_models=db, path_to_capture=api_path, path_to_spec_json=api_path + "json")


if __name__ == '__main__':
    app.run()

```

## References :notebook:
- [MongoMallard](https://hack.close.io/posts/mongomallard)
- [Mongoengine](https://github.com/MongoEngine/mongoengine)
- [Flask-admin](https://github.com/flask-admin/flask-admin)