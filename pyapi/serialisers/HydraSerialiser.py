__author__ = 'mpetyx'

from Serialiser import Serialiser


class HydraSerialiser(Serialiser):
    def to_hydra(self, resources):
        # TODO make it as an independent class

        self.resources = resources
        self.nested_resources(self.resources, language="hydra")

    def to_n3(self):
        return self.graph.serialize(format='n3', indent=4)

    def to_jsonld(self):
        return self.graph.serialize(format='json-ld', indent=4)