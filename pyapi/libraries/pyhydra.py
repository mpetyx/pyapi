__author__ = 'mpetyx'

import sys
from rdflib import Graph, Namespace
from rdflib.namespace import RDF, RDFS
import requests

"""
    This code is copied and reused from https://gist.github.com/pebbie/3a6b2b10c71ba796dca2
"""

HYDRA = Namespace("http://www.w3.org/ns/hydra/core#")

class HydraOperation:
    def __init__(self, subj, graph):
        self.type = graph.value(subj, RDF.type)
        self.subj = subj
        self.method = graph.value(subj, HYDRA.method)
        self.expects = graph.value(subj, HYDRA.expects)
        self.returns = graph.value(subj, HYDRA.returns)
        self.statusCodes = []

    def dump(self):
        print "Operation : ", self.subj
        print "method  : ", self.method
        print "expects : ", self.expects
        print "returns : ", self.returns

class HydraProperty:
    def __init__(self, subj, graph):
        self.type = graph.value(subj, RDF.type)
        self.subj = subj
        self.title = graph.value(subj, HYDRA.title)
        self.description = graph.value(subj, HYDRA.description)
        self.property = graph.value(subj, HYDRA.property)
        self.required = graph.value(subj, HYDRA.required)
        self.readonly = graph.value(subj, HYDRA.readonly)
        self.writeonly = graph.value(subj, HYDRA.writeonly)

    def dump(self):
        if self.title is not None:
            print "Property : ", self.title,
        else:
            print "Property : ", self.subj,
        if self.required:
            print " required",
        if self.readonly:
            print " readonly",
        if self.writeonly:
            print " writeonly",
        print

class HydraClass:
    def __init__(self, subj, graph):
        self.subj = subj
        self.properties = []
        self.operations = []
        for prop in graph.objects(subj, HYDRA.supportedProperty):
            self.properties.append(HydraProperty(prop, graph))
        for op in graph.objects(subj, HYDRA.supportedOperation):
            # print "paw na valw operation"
            ntriples = [triple for triple in graph.triples((op, None, None))]
            if len(ntriples)==0:
                g = Graph().parse(location=op, format="json-ld")
                graph += g
            self.operations.append(HydraOperation(op, graph))

    def dump(self):
        print "Class : ", self.subj
        print self.subj, " properties :"
        for prop in self.properties :
            prop.dump()
        print self.subj, " operations :"
        for op in self.operations:
            op.dump()

class ApiDoc:
    def __init__(self, location):
        self.graph = Graph().parse(location=location, format="json-ld")
        self.classes = {}
        self.operations = []
        self.apidoc = self.graph.value(predicate=RDF.type, object=HYDRA.ApiDocumentation)
        if self.apidoc is None:
            raise Exception("no API Documentation found")
        for cls in self.graph.objects(self.apidoc, HYDRA.supportedClass):
            ntriples = [triple for triple in self.graph.triples((cls, None, None))]
            if len(ntriples)==0:
                g = Graph().parse(location=cls, format="json-ld")
                self.graph += g
            self.classes[cls] = HydraClass(cls, self.graph)
        for ops in self.graph.objects(self.apidoc, HYDRA.supportedOperation):
            self.operations.append(HydraOperation(ops, self.graph))

    def dump(self):
        print self.apidoc, " classes : "
        for cls, clsobj in self.classes.items():
            clsobj.dump()

def parse_link(lvalue):
    """parse Link HTTP header"""
    tmp = lvalue.split("; ")

    rel = None
    link = tmp[0]
    if link[0] =="<":
        link = link[1:-1]

    k, v = tmp[1].split('=')
    if k=="rel":
        rel = v
    if rel is not None:
        if rel[0]=='"':
            rel = rel[1:-1]

    return link, rel

class HypermediaControl:
    def __init__(self, url):
        self.url = url

class Hypermedia:
    def __init__(self, doc=None):
        self.doc = doc
        self.is_collection = False
        self.controls = []
        self.members = []

    def check_documentation(self, location):
        """return true if the location is ApiDocumentation, false if the documentation is elsewhere (pointed by Link header)
        """
        use_entry = True
        hresp = requests.head(location)
        if 'link' in hresp.headers:
            link, rel = parse_link(hresp.headers["link"])
            #print link, rel
            if rel is not None:
                self.doc = ApiDoc(link)
                use_entry = False
            else:
                self.doc = ApiDoc(location)
        else:
            self.doc = ApiDoc(location)
        return use_entry

    def open(self, location):
        """ open current location, find for api doc if not yet set
        """
        is_apidoc = False
        if self.doc is None:
            is_apidoc = self.check_documentation(location)
        if is_apidoc:
            return False

        g = Graph().parse(location=location, format="json-ld")
        # print g.serialize(format="n3")
        for subj, obj in g.subject_objects(RDF.type):
            # print subj, obj, obj in self.doc.classes
            if obj in [HYDRA.Collection, HYDRA.PagedCollection]:
                for member in g.objects(subj, HYDRA.member):
                    self.members.append(member)
            elif obj in self.doc.classes:
                for p, o in g.predicate_objects(subj):
                    if p == RDF.type: continue

                    if (p, RDF.type, None) in self.doc.graph:
                        ptype = self.doc.graph.value(p, RDF.type)
                        if ptype == HYDRA.Link:
                            pref = self.doc.graph.value(p, RDFS.comment)
                            if pref is None:
                                pref = "Link"
                            link = {}
                            link["operations"] = []
                            link["url"] = o
                            for op in self.doc.graph.objects(p, HYDRA.supportedOperation):
                                link["operations"].append(HydraOperation(op, self.doc.graph))
                            self.controls.append(link)
                            print pref, o, [str(l.method) for l in link["operations"]]
                        else:
                            print o, " is ", ptype

        return True



if __name__ == "__main__":
    links = [ 'http://www.markus-lanthaler.com/hydra/api-demo/contexts/EntryPoint.jsonld', 'http://www.markus-lanthaler.com/hydra/api-demo/vocab#']
    for link in links:
        print "I will now check the : ",link
        hm = Hypermedia()
        if hm.open(link):
            print hm.doc.apidoc
            for klassi in hm.doc.classes:
                print "######################"
                print hm.doc.classes[klassi].dump()
                # for operation in  hm.doc.classes[klassi].operations:
                #     print
            break
        break
            # print len(hm.members), len(hm.controls)
