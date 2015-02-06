__author__ = 'mpetyx'

from Serialiser import Serialiser
import yaml, json


class SwaggerSerialiser(Serialiser):
    resources = None

    def to_yaml(self, resources):
        self.resources = resources
        swagger_document = {}
        swagger_document["swagger"] = '2.0'
        swagger_document['paths'] = {}
        paths = {}

        for resource in self.resources:
            d = {resource: {'is': "[paged]", 'displayName': self.resources[resource].displayName}}
            for method in ['get', 'post', 'delete', 'put']:
                if method in self.resources[resource].methods:
                    d[resource][method] = {'description': self.resources[resource].methods[
                        method].description}  # , 'type': self.resources[resource].methods[method].type}
                    d[resource][method]['parameters'] = {}
                    # for parameter in self.resources[resource].methods[method].queryParameters:
                    #
                    # param = self.resources[resource].methods[method].queryParameters[parameter]

                    # d[resource][method]['queryParameters'][parameter] = param
            paths.update(d)

        swagger_document['paths'].update(paths)

        return yaml.dump(swagger_document, default_flow_style=False)

    def to_json(self):


        data = yaml.load(self.to_yaml(self.resources))
        return json.dumps(data)

