__author__ = 'mpetyx'

from pyapi.libraries.pyraml_parser_master.pyraml.model import Model
from pyapi.libraries.pyraml_parser_master.pyraml.fields import String, Reference, Map, List, Bool, Int, Float, Or


class APIDocumentation(Model):
    content = String()
    title = String()


class APISchema(Model):
    name = String()
    type = String()
    schema = String()
    example = String()


class APIQueryParameter(Model):
    name = String()
    description = String()
    example = Or(String(),Int(),Float())
    displayName = String()
    type = String()
    enum = List(Or(String(),Float(),Int()))
    pattern = String()
    minLength = Int()
    maxLength = Int()
    repeat = Bool()
    required = Bool()
    default = Or(String(),Int(),Float())
    minimum = Or(Int(),Float())
    maximum = Or(Int(),Float())


class APIHeader(Model):
    type = String()
    required = Bool()

class APIBody(Model):
    schema = String()
    example = String()
    notNull = Bool()
    formParameters = Map(String(), Reference(APIHeader))
    headers = Map(String(), Reference(APIHeader))
    body = Map(String(), Reference("pyraml.entities.APIBody"))
    is_ = List(String(), field_name="is")

class APIResponse(Model):
    schema = String()
    example = String()
    notNull = Bool()
    description = String()
    headers = Map(String(), Reference(APIHeader))
    body = Reference("pyraml.entities.APIBody")

class APITrait(Model):
    """
    traits:
      - secured:
          usage: Apply this to any method that needs to be secured
          description: Some requests require authentication.
          queryParameters:
            access_token:
              description: Access Token
              type: string
              example: ACCESS_TOKEN
              required: true
    """

    name = String()
    usage = String()
    description = String()
    displayName = String()
    responses = Map(Int(), Reference(APIResponse))
    method = String()
    queryParameters = Map(String(), Reference(APIQueryParameter))
    body = Reference(APIBody)
    # Reference to another APITrait
    is_ = List(String(), field_name="is")



class APIResourceType(Model):
    methods = Map(String(), Reference(APITrait))
    type = String()
    is_ = List(String(), field_name="is")

class APIMethod(Model):
    notNull = Bool()
    description = String()
    body = Reference(APIBody)
    responses = Map(Int(), Reference(APIBody))
    queryParameters = Map(String(), Reference(APIQueryParameter))


class APIResource(Model):
    displayName = String()
    description = String()
    uri = String()
    is_ = Reference(APITrait, field_name="is")
    type = Reference(APIResourceType)
    parentResource = Reference("pyraml.entities.APIResource")
    methods = Map(String(), Reference(APIBody))
    resources = Map(String(), Reference("pyraml.entities.APIResource"))


class APIRoot(Model):
    raml_version = String(required=True)
    title = String()
    version = String()
    baseUri = String()
    protocols = List(String())
    mediaType = String()
    documentation = List(Reference(APIDocumentation))
    traits = Map(String(), Reference(APITrait))
    resources = Map(String(), Reference(APIResource))
    resourceTypes =  Map(String(), Reference(APIResourceType))