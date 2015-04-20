__author__ = 'mpetyx'

from parsers.RamlParser import RamlParser
from parsers.HydraParser import HydraParser
from parsers.SwaggerParser import SwaggerParser

from serialisers import HydraSerialiser
from serialisers.RamlSerialiser import RamlSerialiser
from serialisers.SwaggerSerialiser import SwaggerSerialiser
from serialisers.APIBlueprintSerialiser import APIblueprintSerialiser


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
            g = HydraSerialiser.HydraSerialiser()
            g.to_hydra(self.resources)
            if "json-ld" == format:
                return g.to_jsonld()
            else:
                return g.to_n3()
        elif "swagger" in language.lower():
            g = SwaggerSerialiser(self.resources)
            if format == "json":
                return g.to_json()
            else:
                return g.to_yaml()
        elif "blueprint" in language.lower():
            g = APIblueprintSerialiser(self.resources)
            return g.to_markdown()
        else:

            return "Not supported language yet."


api = API()
# # RAML TEST
# api.parse("http://imagine.epu.ntua.gr:1988/api/doc/schema/Account/?api_key=special-key", language='swagger')
api.parse("coffeemachine.raml","raml")
print api.serialise(language="blueprint", format="n3")
# #
# api.parse('http://www.markus-lanthaler.com/hydra/api-demo/vocab#', language="hydra")
# # print api.serialise(language="hydra",format="json-ld")
# import json
#
# with open('api-demo.json', 'w') as f:
#   json.dump(api.serialise(language="hydra",format="json-ld"), f, sort_keys = True, indent = 4, ensure_ascii=False)
