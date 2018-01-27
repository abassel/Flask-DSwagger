
#
# run with:  py.test --cov-report term-missing --cov=Flask_DSwagger tests -v
#

import pytest

import sys
import os.path

sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

import Flask_DSwagger as fds


from .flask_app import app, User


def test_parts():

    data = """
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

    swagger = fds.api_swagger_register(None)

    json_result = swagger.__startStructure__("1.0.0", "MyAPI", "Unit testing the API", "/api/")

    assert json_result["basePath"] == "/api/"
    assert json_result["info"]["version"] == "1.0.0"
    assert json_result["info"]["title"] == "MyAPI"
    assert json_result["info"]["description"] == "Unit testing the API"

    data = swagger.__extractEndPoints__(app, "/api/", [])

    assert len(data) == 1
    assert list(data[0][1].keys()) == ['/user/{id}']

    swagger.__processDocString__(data, json_result)

    assert list(json_result["paths"].keys()) == ['/user/{id}']

    # raise Exception("here")

    swagger.__extractModels__(db_models={"User": User}, json_result=json_result)

    assert list(json_result["definitions"].keys()) == ['User']

    # from pprint import pprint
    # pprint(json_result["definitions"]['User'])

    assert json_result["definitions"]['User']['type'] == 'object'
    assert json_result["definitions"]['User']['properties']['email']['type'] == 'string'
    assert json_result["definitions"]['User']['properties']['first_name']['type'] == 'string'
    assert json_result["definitions"]['User']['properties']['last_name']['type'] == 'string'

    # raise Exception("Error")


def test_via_flask():

    api_swag = fds.api_swagger_register(app)

    api_swag.generate(db_models={"User": User},
                        path_to_capture="/api/",
                        path_to_spec_json="/api/json",
                        version="1.0.0",
                        title="MyAPI",
                        description="Unit testing the API")

    json_result = fds.api_swagger_register.json_cache["/api/json"]

    assert json_result["basePath"] == "/api/"
    assert json_result["info"]["version"] == "1.0.0"
    assert json_result["info"]["title"] == "MyAPI"
    assert json_result["info"]["description"] == "Unit testing the API"

    assert list(json_result["paths"].keys()) == ['/user/{id}']

    assert list(json_result["definitions"].keys()) == ['User']

    assert json_result["definitions"]['User']['type'] == 'object'
    assert json_result["definitions"]['User']['properties']['email']['type'] == 'string'
    assert json_result["definitions"]['User']['properties']['first_name']['type'] == 'string'
    assert json_result["definitions"]['User']['properties']['last_name']['type'] == 'string'

