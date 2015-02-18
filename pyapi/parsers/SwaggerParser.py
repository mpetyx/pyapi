__author__ = 'mpetyx'

from collections import OrderedDict

import json

from Parser import Parser
from pyapi.entities import APIRoot, APIResource, APIMethod, APIBody, APIResourceType, APITrait, APIQueryParameter


class SwaggerParser(Parser):
    def parse(self, location):
        api = APIRoot(raml_version=str(0.8))
        # api.g_version = g.g_version
        # g = swaggerpy.load_file('test-data/1.1/simple/resources.json')
        with open(location) as data_file:
            data = json.load(data_file)
        api.title = data['info']['title']
        # api.title = g.title
        # api.version = g.version
        api.baseUri = data['host']+data['basePath']
        api.protocols = data['schemes']
        # api.mediaType = g.mediaType
        # api.documentation = g.documentation
        # api.resourceTypes = g.resourceTypes

        resources = OrderedDict()
        for path in data['paths']:
            resource = APIResource()
            resource.displayName = "yolo"
            resource.description = "example of the api"
            # Parse methods

            methods = OrderedDict()

            for operation in data['paths'][path]:
                method = APIMethod(notNull=True)
                if "summary" in data['paths'][path][operation]:
                    method.description = data['paths'][path][operation]['summary']
                else:
                    method.description = data['paths'][path][operation]['description']

                if "parameters" in data['paths'][path][operation]:
                    parameters = OrderedDict()
                    index = 0
                    while index < len(data['paths'][path][operation]['parameters']):
                        param = APIQueryParameter()
                        param.name = data['paths'][path][operation]['parameters'][index]['name']
                        index = index + 1
                        parameters[param.name]=param
                    method.queryParameters = parameters
                methods[str(operation)] = method


            if len(methods):
                resource.methods = methods

            resources[str(path)] = resource

        if resources > 0:
            api.resources = resources

        return api
