__author__ = 'mpetyx'

import json

import yaml

from Serialiser import Serialiser


class SwaggerSerialiser(Serialiser):
    def __init__(self, resources):
        Serialiser.__init__(self)
        self.nested_resources(resources=resources, language="swagger")


    def to_yaml(self):
        return yaml.dump(self.document, default_flow_style=False)

    def to_json(self):
        data = yaml.load(self.to_yaml())
        return json.dumps(data)

