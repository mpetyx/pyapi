__author__ = 'mpetyx'

from rdflib import Namespace, Literal
from rdflib.namespace import RDF, RDFS, OWL
from rdflib import Graph, BNode, URIRef

from Serialiser import Serialiser


class HydraSerialiser(Serialiser):
    graph = None
    resources = None

    def to_hydra(self, resources):
        # TODO make it as an independent class

        self.resources = resources

        g = Graph()

        hydra = Namespace("http://www.w3.org/ns/hydra/core#")
        demo = Namespace("http://www.deepgraphs.org/demo#")

        demoref = URIRef("http://www.deepgraphs.org/demo#")

        g.add((demoref, RDF.type, OWL.Ontology))

        for resource in self.resources:
            link = URIRef(
                "http://www.deepgraphs.org/demo#" + str(resource))  # str(self.resources[resource].displayName))
            g.add((link, RDFS.label, Literal(self.resources[resource].displayName)))
            g.add((link, RDFS.isDefinedBy, demoref))
            g.add((link, RDFS.range, hydra.Resource))
            if not self.resources[resource].methods:
                continue
            for method in ['get', 'post', 'delete', 'put']:
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

        self.graph = g

    def to_n3(self):

        return self.graph.serialize(format='n3', indent=4)

    def to_jsonld(self):

        return self.graph.serialize(format='json-ld', indent=4)