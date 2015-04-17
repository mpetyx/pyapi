__author__ = 'mpetyx'

from collections import OrderedDict

import json

from Parser import Parser
from pyapi.entities import APIRoot, APIResource, APIMethod, APIBody, APIResourceType, APITrait, APIQueryParameter
import requests


class SwaggerParser(Parser):
    api = APIRoot(raml_version=str(0.8))
    
    def parse(self, location):
        # self.api.g_version = g.g_version
        # g = swaggerpy.load_file('test-data/1.1/simple/resources.json')
        if "http://" in location:
            response  = requests.get(location).json()
            # import pprint
            # pprint.pprint(response)
            data = response
        else:
            with open(location) as data_file:
                data = json.load(data_file)
        # self.api.title = data['info']['title']
        # self.api.title = g.title
        # self.api.version = g.version
        # try:
        #     # data['swaggerVersion'] == "1.1"
        #     return self.version_11(data=data)
        # except:
        #     return self.version_12(data=data)
        return self.version_11(data=data)

    def version_12(self, data):

        # self.api.title = data['info']['title']
        # self.api.title = g.title
        # self.api.version = g.version
        self.api.baseUri = data['basePath']
        # self.api.protocols = data['schemes']
        # self.api.mediaType = g.mediaType
        # self.api.documentation = g.documentation
        # self.api.resourceTypes = g.resourceTypes

        resources = OrderedDict()
        for path in data['paths']:
            resource = APIResource()
            resource.displayName = str(path)
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
            self.api.resources = resources

        return self.api
        
    def version_11(self, data):
        
        # self.api.title = data['info']['title']
        # self.api.title = g.title
        # self.api.version = g.version
        self.api.baseUri = data['basePath']
        # self.api.protocols = data['schemes']
        # self.api.mediaType = g.mediaType
        # self.api.documentation = g.documentation
        # self.api.resourceTypes = g.resourceTypes

        resources = OrderedDict()
        for api in data['apis']:
            path = api['path']
            resource = APIResource()
            resource.displayName = str(path)
            resource.description = str(api['description'])
            # Parse methods

            methods = OrderedDict()

            for operation in api['operations']:
                method = APIMethod(notNull=True)
                if "summary" in operation:
                    method.description = operation['summary']
                else:
                    method.description = data['paths'][path][operation]['description']

                if "parameters" in operation:
                    parameters = OrderedDict()
                    index = 0
                    while index < len(operation['parameters']):
                        param = APIQueryParameter()
                        param.name = operation['parameters'][index]['name']
                        index = index + 1
                        parameters[param.name]=param
                    method.queryParameters = parameters
                try:
                    methods[str(operation['httpMethod'])] = method
                except:
                    methods[str(operation['method'])] = method


            if len(methods):
                resource.methods = methods

            resources[str(path)] = resource

        if resources > 0:
            self.api.resources = resources

        return self.api
