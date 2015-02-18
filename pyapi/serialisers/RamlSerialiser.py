__author__ = 'mpetyx'

import yaml

from Serialiser import Serialiser


class RamlSerialiser(Serialiser):
    def to_yaml(self, resources):
        self.resources = resources
        self.nested_resources(self.resources, language="raml")
        raml_document = {}
        # raml_document['version'] = self.version
        # raml_document['documentation'] = self.documentation

        for d in self.nest_resources:
            raml_document.update(d)

        return yaml.dump(raml_document, default_flow_style=False)
