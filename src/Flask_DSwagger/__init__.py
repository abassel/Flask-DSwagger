
import yaml
from flask import Response
from collections import OrderedDict
import json



class model_docString(object):
    @classmethod
    def get_swagger_desc(cls):
        # Objects like BaseQuerySet and Q are being added
        # to json and are making swagger javascript client
        # crash, thus we ignore anything that is not coming
        # from BaseObject because they do not implemented
        # this method
        # See justification here:
        # http://effbot.org/pyfaq/how-do-i-check-if-an-object-is-an-instance-of-a-given-class-or-of-a-subclass-of-it.htm
        return cls.__doc__



class api_swagger_register():
    json_cache = dict()  # generated json gets stored here

    def __init__(self, app):
        self.app = app
        self.paths = []

    def generate(self,
                 db_models,
                 path_to_capture="/api/",
                 path_to_spec_json="/api/json",
                 version="1.0.0",
                 title="API",
                 description="API documentation",
                 hide=[]):

        json_result = self.__startStructure__(version, title, description, path_to_capture)

        data = self.__extractEndPoints__(self.app, path_to_capture, hide)

        self.__processDocString__(data, json_result)

        self.__extractModels__(db_models=db_models, json_result=json_result)

        api_swagger_register.json_cache[path_to_spec_json] = json_result

        def f():
            return Response(json.dumps(api_swagger_register.json_cache[path_to_spec_json]), mimetype='application/json')

        self.app.add_url_rule(path_to_spec_json, path_to_spec_json, view_func=f)


    def __processDocString__(self, data, json_result):

        for endpoint, yaml_data in data:

            # new_url = replace_parameters(rule.rule)     # '/api/v1.0/site/{id}'
            new_url = list(yaml_data.keys())[0]                 # '/site/{id}'
            if new_url in json_result['paths']:
                method = list(yaml_data[new_url].keys())[0]   # put
                spec = list(yaml_data[new_url].values())[0]   # specifications
                json_result['paths'][new_url][method] = spec
            else:
                json_result['paths'].update(yaml_data)


    def __extractEndPoints__(self, app, path_to_capture, hide):

        toRet = []

        for rule in app.url_map.iter_rules():
            if not rule.rule.startswith(path_to_capture):
                continue
            if rule.endpoint in hide:
                continue
            if app.view_functions[rule.endpoint].__doc__ is None:
                # Ignore anything without documentation
                continue
            if len(app.view_functions[rule.endpoint].__doc__.strip()) == 0:
                # Ignore anything without documentation
                continue

            docstring_yml = app.view_functions[rule.endpoint].__doc__

            yaml_data = yaml.load(docstring_yml)

            toRet.append((rule.endpoint, yaml_data))

        return toRet


    def __extractModels__(self, db_models, json_result):


        if type(db_models) is dict:
            items = list(db_models.items())
        else:
            items = list(db_models.__dict__.items())

        for name, cls in items:
            if cls.__doc__ is not None and not name.startswith("__") and not len(cls.__doc__.strip()) == 0:
                try:
                    # import pdb
                    # pdb.set_trace()
                    #if not isinstance(cls, db_models.BaseObject):
                        # objects like BaseQuerySet and Q are being added
                        # to json and are making swagger javascript client
                        # crash, thus we ignore anything that is not coming
                        # from BaseObject. Sometimes isinstance will throw
                        # an exception is the class is a list of strings!
                        #continue
                    if getattr(cls, "get_swagger_desc", None):
                        yaml_data = yaml.load(cls.get_swagger_desc())#cls.__doc__)
                        json_result['definitions'][name] = yaml_data
                except Exception as e:
                    print((name, "->", e))


    def __startStructure__(self, version, title, description, path_to_capture):

        json_result = OrderedDict()
        json_result['swagger'] = '2.0'
        json_result["info"] = {
                           "version": version,
                           "title": title,
                           "description": description
                       }
        json_result['basePath'] = path_to_capture
        json_result['consumes'] = ['application/json']
        json_result['produces'] = ['application/json']
        json_result['paths'] = OrderedDict()
        json_result['definitions'] = OrderedDict()

        return json_result
