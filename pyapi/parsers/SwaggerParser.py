__author__ = 'mpetyx'

from rdflib import Graph

from Parser import Parser

from pyapi.libraries import swaggerpy

import contextlib
import urllib2
import mimetypes
import os.path
import urlparse
import yaml
from collections import OrderedDict

from raml_elements import ParserRamlInclude
from fields import String, Reference
from pyapi.entities import APIRoot, APIResource, APIMethod, APIBody, APIResourceType, APITrait, APIQueryParameter
from constants import RAML_SUPPORTED_FORMAT_VERSION


class SwaggerParser(Parser):
    def parse(self, location):
        api = APIRoot()
        # api.g_version = g.g_version
        g = swaggerpy.load_file('test-data/1.1/simple/resources.json')
        api.title = g.title
        api.version = g.version
        api.baseUri = g.baseUri
        api.protocols = g.baseUri
        api.mediaType = g.mediaType
        api.documentation = g.documentation
        api.traits = g.traits
        api.resources = g.resources
        api.resourceTypes = g.resourceTypes
        return api


__all__ = ["RamlException", "RamlNotFoundException", "RamlParseException",
           "ParseContext", "load", "parse"]

HTTP_METHODS = ("get", "post", "put", "delete", "head")


class RamlException(StandardError):
    pass


class RamlNotFoundException(RamlException):
    pass


class RamlParseException(RamlException):
    pass


class ParseContext(object):
    def __init__(self, data, relative_path):
        self.data = data
        self.relative_path = relative_path

    def get(self, property_name):
        """
        Extract property with name `property_name` from context

        :param property_name: property name to extract
        :type property_name: str

        :return: object
        :rtype: object or None or dict
        """

        # Handle special case with null object
        if self.data is None:
            return None

        property_value = self.data.get(property_name)
        if isinstance(property_value, ParserRamlInclude):
            _property_value, file_type = self._load_include(property_value.file_name)
            if _is_mime_type_raml(file_type):
                relative_path = _calculate_new_relative_path(self.relative_path, property_value.file_name)
                property_value = ParseContext(yaml.load(_property_value), relative_path)
            else:
                property_value = _property_value
        return property_value

    def __iter__(self):
        return iter(self.data)

    def get_string_property(self, property_name, required=False):
        property_value = self.get_property_with_schema(property_name, String(required=required))

        return property_value

    def get_property_with_schema(self, property_name, property_schema):
        property_value = self.get(property_name)
        return property_schema.to_python(property_value)

    def _load_include(self, file_name):
        """
        Load RAML include from file_name.
        :param file_name: name of file to include
        :type file_name: str

        :return: 2 elements tuple: file content and file type
        :rtype: str,str
        """

        if not _is_network_resource(self.relative_path):
            full_path = os.path.join(self.relative_path, file_name)
            return _load_local_file(full_path)
        else:
            url = urlparse.urljoin(self.relative_path, file_name)
            return _load_network_resource(url)


def load(uri):
    """
    Load and parse RAML file

    :param uri: URL which points to a RAML resource or path to the RAML resource on local file system
    :type uri: str

    :return: APIRoot object
    :rtype: pyraml.entities.APIRoot
    """

    if _is_network_resource(uri):
        relative_path = _build_network_relative_path(uri)
        c, _ = _load_network_resource(uri)
    else:
        relative_path = os.path.dirname(uri)
        c, _ = _load_local_file(uri)

    return parse(c, relative_path)


def parse(c, relative_path):
    """
    Parse RAML file

    :param c: file content
    :type c: str
    :return:
    """

    # Read RAML header
    first_line, c = c.split('\n', 1)
    raml_version = _validate_raml_header(first_line)

    context = ParseContext(yaml.load(c), relative_path)

    root = APIRoot(raml_version=raml_version)
    root.title = context.get_string_property('title', True)

    root.baseUri = context.get_string_property('baseUri')
    root.version = context.get('version')
    # root.mediaType = context.get_string_property('mediaType')

    # root.documentation = context.get_property_with_schema('documentation', APIRoot.documentation)
    # root.traits = parse_traits(context, APIRoot.traits.field_name, root.mediaType)
    root.resourceTypes = parse_resource_type(context)

    resources = OrderedDict()
    for property_name in context.__iter__():
        if property_name.startswith("/"):
            resources[property_name] = parse_resource(context, property_name, root, root.mediaType)

    if resources > 0:
        root.resources = resources

    return root


def parse_resource(c, property_name, parent_object, global_media_type):
    """
    Parse and extract resource with name

    :param c:
    :type c: ParseContext

    :param parent_object: APIRoot object or APIResource object
    :type parent_object: APIRoot or APIResource

    :param property_name: resource name to extract
    :type property_name: str

    :return: APIResource  or None
    :rtype: APIResource
    """
    property_value = c.get(property_name)
    if not property_value:
        return None

    resource = APIResource(uri=property_name)
    new_context = ParseContext(property_value, c.relative_path)
    resource.description = new_context.get_string_property("description")
    resource.displayName = new_context.get_string_property("displayName")

    if isinstance(parent_object, APIResource):
        resource.parentResource = parent_object

    # Parse methods
    methods = OrderedDict()
    for _http_method in HTTP_METHODS:
        _method = new_context.get(_http_method)
        if _method:
            methods[_http_method] = parse_method(ParseContext(_method, c.relative_path), global_media_type)
        elif _http_method in new_context.data:
            # workaround: if _http_method is already in new_context.data than
            # it's marked as !!null
            methods[_http_method] = APIMethod(notNull=True)
    if len(methods):
        resource.methods = methods

    # Parse resources
    resources = OrderedDict()
    for property_name in new_context.__iter__():
        if property_name.startswith("/"):
            resources[property_name] = parse_resource(new_context, property_name, resource, global_media_type)

    if resources > 0:
        resource.resources = resources

    return resource


def parse_resource_type(c):
    """
    Parse and extract resourceType

    :param c: ParseContext object
    :type c: ParseContext

    :return: APIResource  or None
    :rtype: APIResource
    """

    json_resource_types = c.get('resourceTypes')
    if not json_resource_types:
        return None

    # We got list of dict from c.get('resourceTypes') so we need to convert it to dict
    resource_types_context = ParseContext(json_resource_types[0], c.relative_path)

    resource_types = {}

    for rtype_name in resource_types_context:
        new_c = ParseContext(resource_types_context.get(rtype_name), resource_types_context.relative_path)

        rtype_obj = APIResourceType()
        rtype_obj.type = new_c.get_string_property("type")
        rtype_obj.is_ = new_c.get_property_with_schema("is", APIResourceType.is_)

        # Parse methods
        methods = OrderedDict()
        for _http_method in HTTP_METHODS:
            _method = new_c.get(_http_method)
            if _method:
                _method = ParseContext(_method, new_c.relative_path).get_property_with_schema('traits',
                                                                                              Reference(APITrait))
                methods[_http_method] = _method
            elif _http_method in new_c.data:
                # workaround: if _http_method is already in new_context.data than
                # it's marked as !!null
                _method = APIMethod(notNull=True)
                methods[_http_method] = _method
        if len(methods):
            rtype_obj.methods = methods

        resource_types[rtype_name] = rtype_obj

    return resource_types


def parse_method(c, global_media_type):
    """
    Parse RAML method

    :param c: ParseContext object which contains APIMethod
    :type c: ParseContext

    :param parent_object: APIRoot, APIResource or APIResourceType object
    :type parent_object: APIRoot or APIResource or APIResourceType

    :return: APIMethod or None
    :rtype: APIMethod
    """

    method = APIMethod()

    method.description = c.get_string_property("description")
    method.body = parse_inline_body(c.get("body"), c.relative_path, global_media_type)

    parsed_responses = parse_inline_body(c.get("responses"), c.relative_path, global_media_type)
    if parsed_responses:
        new_parsed_responses = OrderedDict()
        for resp_code, parsed_data in parsed_responses.iteritems():
            if resp_code == "<<":
                # Check for default code (equivalent of wildcard "*")
                new_parsed_responses.setdefault(parsed_data)
            else:
                # Otherwise response code should be numeric HTTP response code
                try:
                    resp_code = int(resp_code)
                except ValueError:
                    raise RamlParseException(
                        "Expected numeric HTTP response code in responses but got {!r}".format(resp_code))
                new_parsed_responses[resp_code] = parsed_data
        method.responses = new_parsed_responses

    method.queryParameters = c.get_property_with_schema("queryParameters", APIMethod.queryParameters)

    return method


def parse_map_of_entities(parser, context, relative_path, parent_resource):
    """

    :param parser: function which accepts 3 arguments: data, relative_path and parent_resource
    where entity is content
    :type parser: callable
    :param context: current parse context
    :type context: dict
    :param relative_path:
    :param parent_resource:
    :return:
    """
    res = OrderedDict()

    if context:
        for key, value in context.items():
            if value:
                res[key] = parser(value, relative_path, parent_resource)
            else:
                # workaround: if `key` is already in `context` than
                # it's marked as !!null
                res[key] = APIMethod(notNull=True)

    return res


def parse_body(c, global_media_type):
    """
    Parse and extract resource with name

    :param c: ParseContext object which contains APIBody
    :type c: ParseContext

    :return: APIBody or None
    :rtype: APIBody
    """

    if c.data is None:
        return None

    body = APIBody()
    body.example = c.get_string_property("example")
    body.body = parse_inline_body(c.get("body"), c.relative_path, global_media_type)

    body.schema = c.get_string_property("schema")
    body.example = c.get_string_property("example")
    body.formParameters = c.get_property_with_schema("formParameters", APIBody.formParameters)
    body.headers = c.get_property_with_schema("headers", APIBody.headers)

    return body


def parse_inline_body(data, relative_path, global_media_type):
    """
    Parse not null `body` inline property

    :param data: value of `body` property
    :type data: dict
    :param relative_path: relative path on filesystem to a RAML resource for handling `include` tags
    :type relative_path: str
    :return: OrderedDict of APIBody or None
    :rtype: OrderedDict of APIBody
    """
    if data is None:
        return None

    res = OrderedDict()

    # Data could be map of mime_type => body, http_code => body but also it could be direct
    # value of APIBody with global mediaType (grrr... so consistent)
    for field_name in APIBody._structure:
        if field_name in data:
            # This is direct value of APIBody
            parsed_data = parse_body(ParseContext(data, relative_path), global_media_type)
            res[global_media_type] = parsed_data
            return res

    for key, body_data in data.iteritems():
        if body_data:
            res[key] = parse_body(ParseContext(body_data, relative_path), global_media_type)
        else:
            # body marked as !!null
            res[key] = APIBody(notNull=True)

    return res


def _validate_raml_header(line):
    """
    Parse header of RAML file and ensure than we can work with it

    :param line: RAML header
    :type line: str

    :return: RAML format string
    :rtype: str

    :raise RamlParseException: in case of parsing errors
    """

    # Line should look like "#%RAML 0.8". Split it by whitespace and validate
    header_tuple = line.split()
    if len(header_tuple) != 2:
        raise RamlParseException("Invalid format of RAML header")

    if header_tuple[0] != "#%RAML":
        raise RamlParseException("Unable to found RAML header")

    try:
        # Extract first 2 numbers from format version, e.g. "0.8.2" -> "0.8"
        major_format_version = ".".join(header_tuple[1].split(".")[:2])

        if float(major_format_version) > RAML_SUPPORTED_FORMAT_VERSION:
            raise RamlParseException("Unsupported format of RAML file", header_tuple[1])

        return header_tuple[1]
    except ValueError:
        raise RamlParseException("Invalid RAML format version", header_tuple[1])


def _is_mime_type_raml(mime_type):
    return mime_type.lower() in ["text/yaml", "application/raml+yaml",
                                 "text/x-yaml", "application/yaml", "application/x-yaml"]


def _is_mime_type_json(mime_type):
    return mime_type.lower() == "application/json"


def _is_mime_type_xml(mime_type):
    return mime_type.lower() == "application/xml"


def _is_network_resource(uri):
    return urlparse.urlparse(uri).scheme


def _build_network_relative_path(url):
    p = urlparse.urlparse(url)
    return urlparse.urlunparse(urlparse.ParseResult(p.scheme, p.netloc, os.path.dirname(p.path), '', '', ''))


def _calculate_new_relative_path(base, uri):
    if _is_network_resource(base):
        return _build_network_relative_path(urlparse.urljoin(base, uri))
    else:
        return os.path.dirname(os.path.join(base, uri))


def _load_local_file(full_path):
    # include locates at local file system
    if not os.path.exists(full_path):
        raise RamlNotFoundException("No such file {} found".format(full_path))

    # detect file type... we should able to parse raml, yaml, json, xml and read all other content types as plain
    # files
    mime_type = mimetypes.guess_type(full_path)[0]
    if mime_type is None:
        mime_type = "text/plain"

    with contextlib.closing(open(full_path, 'rU')) as f:
        return f.read(), mime_type


def _load_network_resource(url):
    with contextlib.closing(urllib2.urlopen(url, timeout=60.0)) as f:
        # We fully rely of mime type to remote server b/c according
        # of specs it MUST support RAML mime
        mime_type = f.headers.gettype()
        return f.read(), mime_type


def _parse_raml_version(content):
    """
    Get optional property `version` and make sure that it is a string.
    If the property does not exist the function returns None

    :return: string - property value or None
    :rtype : basestring or None
    """

    property_value = content.get('version')
    if not property_value:
        return None

    # version should be string but if version specified as "0.1" yaml package recognized
    # it as float, so we should handle this situation
    if not (isinstance(property_value, (basestring, float)) or (isinstance(property_value, (basestring, int)))):
        raise RamlParseException("Property `version` must be string")

    if isinstance(property_value, float) or isinstance(property_value, int):
        res = str(property_value)

    return property_value
