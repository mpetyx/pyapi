__author__ = 'mpetyx'

from Serialiser import Serialiser
import yaml


class RamlSerialiser(Serialiser):
    resources = None

    def to_yaml(self, resources):
        self.resources = resources
        raml_document = {}
        # raml_document['version'] = self.version
        # raml_document['documentation'] = self.documentation
        for resource in self.resources:
            d = {resource: {'is': "[paged]", 'displayName': self.resources[resource].displayName,
                            'description': self.resources[resource].description}}
            if not self.resources[resource].methods:
                continue
            for method in ['get', 'post', 'delete', 'put']:
                if (method.upper() in self.resources[resource].methods) or (method in self.resources[resource].methods):
                    if method.upper() in self.resources[resource].methods:
                        method = method.upper()
                    d[resource][method] = {'description': self.resources[resource].methods[
                        method].description}  # , 'type': self.resources[resource].methods[method].type}
                    d[resource][method]['queryParameters'] = {}
                    if not self.resources[resource].methods[method].queryParameters:
                        continue
                    for parameter in self.resources[resource].methods[method].queryParameters:
                        # queryParam1.example == "two", queryParam1
                        #   queryParam1.enum == ["one", "two", "three"], queryParam1
                        #   queryParam1.displayName == "name name", queryParam1
                        #   queryParam1.description == "name description"
                        #   queryParam1.default == "three", queryParam1
                        #   queryParam1.minLength == 3, queryParam1
                        #   queryParam1.type == "string", queryParam1
                        #   queryParam1.maxLength == 5, queryParam1
                        #   queryParam1.pattern == '[a-z]{3,5}', queryParam1
                        #   queryParam1.required == False, queryParam1
                        #   queryParam1.repeat == False, queryParam1

                        param = self.resources[resource].methods[method].queryParameters[parameter]
                        # param = {}
                        # param['example'] =
                        d[resource][method]['queryParameters'][parameter] = param
            raml_document.update(d)

        return yaml.dump(raml_document, default_flow_style=False)