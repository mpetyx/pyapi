__author__ = 'mpetyx'

from collections import OrderedDict

from Parser import Parser
from pyapi.entities import APIRoot, APIResource, APIMethod
from pyapi.libraries.pyhydra import Hypermedia


class HydraParser(Parser):
    def parse(self, location):


        hm = Hypermedia()
        hm.open(location)
        # if hm.open(location):
        # print hm.doc.apidoc
        # for klassi in hm.doc.classes:
        #         print "######################"
        #         print hm.doc.classes[klassi].dump()
        # for operation in  hm.doc.classes[klassi].operations:
        #     print

        # first_line, c = c.split('\n', 1)
        # raml_version = _validate_raml_header(first_line)

        # context = ParseContext(yaml.load(c), location)

        root = APIRoot(raml_version=str(0.8))
        # root.title = context.get_string_property('title', True)
        #
        # root.baseUri = context.get_string_property('baseUri')
        # root.version = context.get('version')
        # root.mediaType = context.get_string_property('mediaType')

        # root.documentation = context.get_property_with_schema('documentation', APIRoot.documentation)
        # root.traits = parse_traits(context, APIRoot.traits.field_name, root.mediaType)
        # root.resourceTypes = parse_resource_type(context)

        resources = OrderedDict()
        for klass in hm.doc.classes:
            resource = APIResource()
            resource.displayName = "yolo"
            resource.description = "example of the api"
            # Parse methods

            methods = OrderedDict()

            for operation in hm.doc.classes[klass].operations:
                method = APIMethod(notNull=True)
                method.description = str(operation.subj)
                methods[str(operation.method)] = method

            if len(methods):
                resource.methods = methods

            resources[str(klass)] = resource  #parse_resource(context, property_name, root, root.mediaType)

        if resources > 0:
            root.resources = resources

        #
        # api = APIRoot()
        # g = Graph().parse(location, format='json-ld')

        return root