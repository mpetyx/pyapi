__author__ = 'mpetyx'

import yaml
import json

from pyapi.libraries.pyraml_parser_master import pyraml
from pyapi.libraries.pyraml_parser_master.pyraml import parser
from pyapi.libraries.pyraml_parser_master.pyraml.entities import RamlResource, RamlMethod, RamlQueryParameter

from rdflib import Namespace, Literal
from rdflib.namespace import RDF, RDFS, OWL
from rdflib import Graph, BNode, URIRef

class API():

    resources = []
    documentation = None
    version = None
    atlas = {}

    def parse(self, document= None, location=None):
        self.atlas = pyraml.parser.load(document)
        self.resources = self.atlas.resources

    def to_raml(self):

        raml_document = {}
        raml_document['version'] = self.version
        raml_document['documentation'] = self.documentation
        print "you have resources "+str(len(self.resources))
        for resource in self.resources:
            d = {resource: {'is': "[paged]", 'displayName':self.resources[resource].displayName}}
            for method in ['get','post','delete','put']:
                if method in self.resources[resource].methods:
                    d[resource][method] = {'description': self.resources[resource].methods[method].description} #, 'type': self.resources[resource].methods[method].type}
                    d[resource][method]['queryParameters'] = {}
                    for parameter in self.resources[resource].methods[method].queryParameters:
                    #   queryParam1.example == "two", queryParam1
                    #   queryParam1.enum == ["one", "two", "three"], queryParam1
                    #   queryParam1.displayName == "name name", queryParam1
                    #   queryParam1.description == "name description"
                    #   queryParam1.default == "three", queryParam1
                    #   queryParam1.minLength == 3, queryParam1
                    #   queryParam1.type == "string", queryParam1
                    #   queryParam1.maxLength == 5, queryParam1
                    #   queryParam1.pattern == '[a-z]{3,5}', queryParam1
                    #   queryParam1.required == False, queryParam1
                    #   queryParam1.repeat == False, queryParam1

                        param = self.resources[resource].methods[method].queryParameters[parameter]
                        # param = {}
                        # param['example'] =
                        d[resource][method]['queryParameters'][parameter] = param
            raml_document.update(d)

        print yaml.dump(raml_document, default_flow_style=False)

    def to_yaml_swagger(self):

        swagger_document = {}
        swagger_document["swagger"] =  '2.0'
        swagger_document['paths'] = {}
        paths = {}

        for resource in self.resources:
            d = {resource: {'is': "[paged]", 'displayName':self.resources[resource].displayName}}
            for method in ['get','post','delete','put']:
                if method in self.resources[resource].methods:
                    d[resource][method] = {'description': self.resources[resource].methods[method].description} #, 'type': self.resources[resource].methods[method].type}
                    d[resource][method]['parameters'] = {}
                    # for parameter in self.resources[resource].methods[method].queryParameters:
                    #
                    #     param = self.resources[resource].methods[method].queryParameters[parameter]

                        # d[resource][method]['queryParameters'][parameter] = param
            paths.update(d)

        swagger_document['paths'].update(paths)


        return yaml.dump(swagger_document, default_flow_style=False)


    def to_json_swagger(self):


        data = yaml.load(self.to_yaml_swagger())
        json_doc = json.dumps(data)

        print(json_doc)

    def to_hydra(self):

        g = Graph()

        hydra = Namespace("http://www.w3.org/ns/hydra/core#")
        demo = Namespace("http://www.deepgraphs.org/demo#")

        demoref = URIRef("http://www.deepgraphs.org/demo#")

        g.add((demoref, RDF.type, OWL.Ontology))

        for resource in self.resources:
            link = URIRef("http://www.deepgraphs.org/demo#"+str(resource)) #str(self.resources[resource].displayName))
            g.add((link, RDFS.label, Literal(self.resources[resource].displayName)))
            g.add((link, RDFS.isDefinedBy, demoref))
            g.add((link, RDFS.range, hydra.Resource))
            for method in ['get','post','delete','put']:
                if method in self.resources[resource].methods:
                    # d[resource][method]['parameters'] = {}

                    operation = BNode()
                    g.add((operation, RDF.type, hydra.Operation))
                    g.add((operation, RDFS.comment, Literal(self.resources[resource].methods[method].description)))
                    g.add((operation, hydra.method, Literal(method.upper())))
                    g.add((operation, hydra.expects, demo.InputClass))
                    g.add((link, hydra.supportedOperations, operation))

                    if self.resources[resource].methods[method].queryParameters == None:
                        continue

                    for parameter in self.resources[resource].methods[method].queryParameters:
                        param = self.resources[resource].methods[method].queryParameters[parameter]
                        # d[resource][method]['queryParameters'][parameter] = param
                        bNodeproperty = BNode()
                        property = BNode()
                        g.add((property, RDF.type, hydra.link))
                        g.add((property, RDFS.isDefinedBy, demoref))
                        g.add((property, RDFS.label, Literal(param.displayName)))
                        g.add((property, RDFS.comment, Literal(param.description)))
                        g.add((bNodeproperty, hydra.property, property))
                        g.add((bNodeproperty, hydra.readonly, Literal(True)))
                        g.add((operation, hydra.supportedProperties, bNodeproperty ))


        return g.serialize(format='n3', indent=4)


api = API()
api.parse("bookstore.raml")
api.version = 2.0
print api.to_hydra()
