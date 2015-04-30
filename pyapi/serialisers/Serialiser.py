__author__ = 'mpetyx'

import urllib

from rdflib import Namespace, Literal
from rdflib.namespace import RDF, RDFS, OWL
from rdflib import Graph, BNode, URIRef


class Serialiser:
    resources = None
    graph = Graph()
    nest_resources = []
    document = {}
    blueprint = ""

    def __init__(self):
        self.document["swagger"] = '2.0'
        self.document['paths'] = {}


    def raml_parse_resource(self, resource_name, resource):

        d = {resource_name: {'is': "[paged]", 'displayName': resource.displayName,
                             'description': resource.description}}
        for method in ['get', 'post', 'delete', 'put']:
            if (method.upper() in resource.methods) or (method in resource.methods):
                if method.upper() in resource.methods:
                    method = method.upper()
                d[resource_name][method.lower()] = {'description': str(resource.methods[
                                                                           method].description)}  # , 'type': resource].methods[method].type}
                d[resource_name][method.lower()]['queryParameters'] = {}
                if not resource.methods[method].queryParameters:
                    continue
                for parameter in resource.methods[method].queryParameters:
                    param = {}
                    if resource.methods[method].queryParameters[parameter].example:
                        param['example'] = resource.methods[method].queryParameters[parameter].example
                    if resource.methods[method].queryParameters[parameter].pattern:
                        param['pattern'] = resource.methods[method].queryParameters[parameter].pattern
                    if resource.methods[method].queryParameters[parameter].enum:
                        param['enum'] = resource.methods[method].queryParameters[parameter].enum
                    if resource.methods[method].queryParameters[parameter].displayName:
                        param['displayName'] = resource.methods[method].queryParameters[parameter].displayName
                    if resource.methods[method].queryParameters[parameter].description:
                        param['description'] = resource.methods[method].queryParameters[parameter].description
                    if resource.methods[method].queryParameters[parameter].default:
                        param['default'] = resource.methods[method].queryParameters[parameter].default
                    if resource.methods[method].queryParameters[parameter].minLength:
                        param['minLength'] = resource.methods[method].queryParameters[parameter].minLength
                    if resource.methods[method].queryParameters[parameter].type:
                        param['type'] = resource.methods[method].queryParameters[parameter].type
                    if resource.methods[method].queryParameters[parameter].maxLength:
                        param['maxLength'] = resource.methods[method].queryParameters[parameter].maxLength
                    if resource.methods[method].queryParameters[parameter].required:
                        param['required'] = resource.methods[method].queryParameters[parameter].required
                    if resource.methods[method].queryParameters[parameter].repeat:
                        param['repeat'] = resource.methods[method].queryParameters[parameter].repeat
                    d[resource_name][method.lower()]['queryParameters'][str(parameter)] = param

        self.nest_resources.append(d)


    def hydra_parse_resource(self, resource_name, resource):
        # TODO make it as an independent class


        hydra = Namespace("http://www.w3.org/ns/hydra/core#")
        demo = Namespace("http://www.deepgraphs.org/demo#")

        demoref = URIRef("http://www.deepgraphs.org/demo#")

        self.graph.add((demoref, RDF.type, OWL.Ontology))

        link = URIRef(  # str("http://www.deepgraphs.org/demo#" + str(resource_name)).encode("utf-8"))
                        urllib.quote("http://www.deepgraphs.org/demo#" + str(resource_name), safe=':/#'))
        # ("http://www.deepgraphs.org/demo#" + str(resource_name)).encode("utf-8s")

        self.graph.add((link, RDFS.label, Literal(resource_name)))
        self.graph.add((link, RDFS.isDefinedBy, demoref))
        self.graph.add((link, RDFS.range, hydra.Resource))
        for method in ['get', 'post', 'delete', 'put']:
            if not resource.methods:
                continue
            if (method.upper() in resource.methods) or (method in resource.methods):
                if method.upper() in resource.methods:
                    method = method.upper()
                operation = BNode()
                self.graph.add((operation, RDF.type, hydra.Operation))
                self.graph.add((operation, RDFS.comment, Literal(str(resource.methods[method].description))))
                self.graph.add((operation, hydra.method, Literal(method.upper())))
                self.graph.add((operation, hydra.expects, demo.InputClass))
                self.graph.add((link, hydra.supportedOperations, operation))

                if not resource.methods[method].queryParameters:
                    continue

                for parameter in resource.methods[method].queryParameters:
                    param = resource.methods[method].queryParameters[parameter]
                    bNodeproperty = BNode()
                    # property = BNode()
                    current_property = URIRef("http://www.deepgraphs.org/demo#" + str(parameter))
                    self.graph.add((current_property, RDF.type, hydra.link))
                    self.graph.add((current_property, RDFS.isDefinedBy, demoref))
                    self.graph.add((current_property, RDFS.label, Literal(param.displayName)))
                    self.graph.add((current_property, RDFS.comment, Literal(param.description)))
                    self.graph.add((bNodeproperty, hydra.property, current_property))
                    self.graph.add((bNodeproperty, hydra.readonly, Literal(True)))
                    self.graph.add((operation, hydra.supportedProperties, bNodeproperty))

    def swagger_parse_resource(self, resource_name, resource):

        paths = {}

        d = {resource_name: {'is': "[paged]", 'displayName': resource.displayName}}
        for method in ['get', 'post', 'delete', 'put']:
            if (method.upper() in resource.methods) or (method in resource.methods):
                if method.upper() in resource.methods:
                    method = method.upper()
                d[resource_name][method] = {'description': str(
                    resource.methods[method].description)}  # , 'type': self.resources[resource].methods[method].type}
                d[resource_name][method]['parameters'] = {}

        paths.update(d)
        self.document['paths'].update(paths)

    def blueprint_parse_resource(self, resource_name, resource):

        paths = {}

        d = {resource_name: {'is': "[paged]", 'displayName': resource.displayName}}
        output = "# %s \n%s \n\n%s\n\n" % (resource_name, resource.displayName, resource.description)
        for method in ['get', 'post', 'delete', 'put']:
            if (method.upper() in resource.methods) or (method in resource.methods):
                if method.upper() in resource.methods:
                    method = method.upper()
                d[resource_name][method] = {'description': str(
                    resource.methods[method].description)}  # , 'type': self.resources[resource].methods[method].type}
                d[resource_name][method]['parameters'] = {}
                output = output + "## %s\n%s\n\n" % (method.upper(), str(resource.methods[method].description))

        self.blueprint = self.blueprint + output


    def nested_resources(self, resources, language, parentPath=""):

        for root_resource in resources:
            if language == "raml":
                self.raml_parse_resource(parentPath + root_resource, resources[root_resource])
            elif language == "hydra":
                self.hydra_parse_resource(parentPath + root_resource, resources[root_resource])
            elif language == "blueprint":
                self.blueprint_parse_resource(parentPath + root_resource, resources[root_resource])
            elif language == "swagger":
                self.swagger_parse_resource(parentPath + root_resource, resources[root_resource])

            if resources[root_resource].resources:
                self.nested_resources(resources[root_resource].resources, language=language,
                                      parentPath=parentPath + str(root_resource))

