
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
import mongoengine as mongo

import Flask_DSwagger as fds

app = Flask(__name__)

class User(mongo.Document, fds.model_docString):
    """
    type: object
    properties:
      first_name:
        type: string
        description: His/Her first name.
      last_name:
        type: string
        description: His/Her last name.
      email:
        type: string
        description: His/Her email.
    """
    first_name = mongo.StringField()
    last_name = mongo.StringField()
    email = mongo.StringField()


@app.route('/')
def hello():
    return "I will not be in the documentation because my path does not start with /api"


@app.route('/api/user/<id>')
def user_getbyname(id):
    """
    "/user/{id}":   # Must start with forward slash
        get:

            summary: "Endpoint to return information about a single user"

            description: "List information about user of a given id"

            tags: ["userbyid"]

            operationId: "get_user_by_id"

            produces:
                - "application/json"

            parameters:
            - name: id
              in: path
              description: "id of site in the database"
              required: true
              type: "string"

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

    return "Hello {}!".format(id)


api_swag = fds.api_swagger_register(app)

api_swag.generate(db_models={"User": User})

if __name__ == '__main__':
    app.run()

```

## References :notebook:
- [MongoMallard](https://hack.close.io/posts/mongomallard)
- [Mongoengine](https://github.com/MongoEngine/mongoengine)
- [Flask-admin](https://github.com/flask-admin/flask-admin)