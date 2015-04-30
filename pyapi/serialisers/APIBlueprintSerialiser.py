__author__ = 'mpetyx'

from Serialiser import Serialiser


class APIblueprintSerialiser(Serialiser):
    def __init__(self, resources):
        Serialiser.__init__(self)
        self.nested_resources(resources=resources, language="blueprint")


    def to_markdown(self):
        return self.blueprint