__author__ = 'mpetyx'

import contextlib
import urllib2
import mimetypes
import os.path
import urlparse
from collections import OrderedDict

import json

from Parser import Parser
from pyapi.libraries import swaggerpy
from pyapi.entities import APIRoot, APIResource, APIMethod, APIBody, APIResourceType, APITrait


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
        # api.traits = g.traits
        # api.resources = g.resources
        # api.resourceTypes = g.resourceTypes

        resources = OrderedDict()
        for klass in data['paths']:
            resource = APIResource()
            resource.displayName = "yolo"
            resource.description = "example of the api"
            # Parse methods

            methods = OrderedDict()

            for operation in data['paths'][klass]:
                method = APIMethod(notNull=True)
                try:
                    method.description = data['paths'][klass][operation]['summary']
                except:
                    method.description = data['paths'][klass][operation]['description']
                methods[str(operation)] = method

            if len(methods):
                resource.methods = methods

            resources[str(klass)] = resource  #parse_resource(context, property_name, root, root.mediaType)

        if resources > 0:
            api.resources = resources

        return api
