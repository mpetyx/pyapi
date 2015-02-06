__author__ = 'mpetyx'

from pyapi.libraries.pyraml_parser_master import pyraml
from pyapi.libraries.pyraml_parser_master.pyraml import parser
from pyapi.libraries.pyraml_parser_master.pyraml.entities import RamlResource, RamlMethod, RamlQueryParameter
from Parser import Parser

from pyapi.entities import APIRoot


class RamlParser(Parser):
    def parse(self, location):
        api = APIRoot()
        raml = pyraml.parser.load(location)
        api.raml_version = raml.raml_version
        api.title = raml.title
        api.version = raml.version
        api.baseUri = raml.baseUri
        api.protocols = raml.baseUri
        api.mediaType = raml.mediaType
        api.documentation = raml.documentation
        api.traits = raml.traits
        api.resources = raml.resources
        api.resourceTypes = raml.resourceTypes
        return api