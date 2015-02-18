__author__ = 'mpetyx'

from serialisers.HydraSerialiser import HydraSerialiser
from serialisers.RamlSerialiser import RamlSerialiser
from serialisers.SwaggerSerialiser import SwaggerSerialiser

from parsers.RamlParser import RamlParser
from parsers.HydraParser import HydraParser
from parsers.SwaggerParser import SwaggerParser


class API():
    resources = []
    documentation = None
    version = None
    atlas = {}
    supportedFormats = ['raml', 'swagger', 'hydra']

    def parse(self, location=None, language=None):
        if "raml" in language.lower():
            self.atlas = RamlParser().parse(location)
            self.resources = self.atlas.resources
        elif "hydra" in language.lower():
            self.atlas = HydraParser().parse(location)
            self.resources = self.atlas.resources
        elif "swagger" in language.lower():
            self.atlas = SwaggerParser().parse(location)
            self.resources = self.atlas.resources
        else:
            return "Not supported language yet."

    def serialise(self, language, format=None):
        if "raml" in language.lower():
            g = RamlSerialiser()
            return g.to_yaml(self.resources)
        elif "hydra" in language.lower():
            g = HydraSerialiser()
            g.to_hydra(self.resources)
            if "json-ld" == format:
                return g.to_jsonld()
            else:
                return g.to_n3()
        elif "swagger" in language.lower():
            g = SwaggerSerialiser()
            if format == "json":
                g.to_yaml(self.resources)
                return g.to_json()
            else:
                return g.to_yaml(self.resources)
        else:

            return "Not supported language yet."


api = API()
# RAML TEST
# api.parse("petstore.json", language='swagger')
api.parse("coffeemachine.raml","raml")
# print api.serialise(language="raml", format="yaml")
#
# api.parse('http://www.markus-lanthaler.com/hydra/api-demo/vocab#', language="hydra")
print api.serialise(language="hydra",format="n3")
