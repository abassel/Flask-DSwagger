from flask import Flask
import mongoengine as mongo

import sys
import os.path

sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

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


# @app.route('/api/user')
# def user_get():
#     """
#     "/user":   # Must start with forward slash
#         get:
#
#             summary: "Endpoint to return information about users"
#
#             description: "List information about users"
#
#             tags: ["userget"]
#
#             produces:
#               - "application/json"
#
#             responses:
#               "200":
#                 description: "Success response"
#                 schema:
#                   $ref: "#/definitions/User"
#               default:
#                 description: "unexpected error"
#                 schema:
#                   $ref: "#/definitions/ErrorModel"
#
#     """
#     return "Hello World!".format()



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


# api_swag = fds.api_swagger_register(app)

# api_swag.generate(db_models={"User": User})

if __name__ == '__main__':
    app.run()
