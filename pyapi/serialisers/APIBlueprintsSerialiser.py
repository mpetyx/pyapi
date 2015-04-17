__author__ = 'mpetyx'

import markdown

from Serialiser import Serialiser
import yaml


class APIBlueprintsSerialiser(Serialiser):

    def __init__(self, resources):
        Serialiser.__init__(self)
        self.nested_resources(resources=resources,language="blueprints")


    def to_markdown(self):

        return self.blueprints