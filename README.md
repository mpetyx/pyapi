# pyapi 
[![Build Status](https://travis-ci.org/mpetyx/pyapi.svg?branch=master)](https://travis-ci.org/mpetyx/pyapi)

***

---------- **UNDER HEAVY DEVELOPMENT - EXTREMELY UNSTABLE** -------------------- 

An API parser and serialiser for Swagger, RAML, API-Blueprintes and Hydra

***

It provides parsers and serialisers for

- [Hydra](http://www.hydra-cg.com/ "Hydra") 
- [RAML](http://raml.org/)
- [Swagger](http://swagger.io/)   
- WADL 

## 3rd Party Libraries

- [Wadl to Swagger](https://github.com/rackerlabs/wadl2swagger)
- [Raml Parser](https://github.com/an2deg/pyraml-parser)

## Validation Services

**Swagger Validation**
-- [Flex](https://github.com/pipermerriam/flex)

**Raml Validation** 
-- [Raml Parser](https://github.com/an2deg/pyraml-parser)

**Hydra Validation**



## Examples

`api = API() api.parse("bookstore.raml", language='raml')`

`print api.serialise(language="swagger", format="json") print api.serialise(language="swagger", format="yaml")`

`print api.serialise(language="raml")`

`print api.serialise(language="hydra", format="json-ld") print api.serialise(language="swagger", format="n3")`
