__author__ = 'mpetyx'

from collections import OrderedDict

from Parser import Parser
from pyapi.entities import APIRoot, APIResource, APIMethod
from pyapi.libraries.pyhydra import Hypermedia

import markdown
from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint




class APIBlueprintsParser(Parser):
    def parse(self, location):


        hm = Hypermedia()
        hm.open(location)
        # if hm.open(location):
        # print hm.doc.apidoc
        # for klassi in hm.doc.classes:
        #         print "######################"
        #         print hm.doc.classes[klassi].dump()
        # for operation in  hm.doc.classes[klassi].operations:
        #     print

        # first_line, c = c.split('\n', 1)
        # raml_version = _validate_raml_header(first_line)

        # context = ParseContext(yaml.load(c), location)

        root = APIRoot(raml_version=str(0.8))
        # root.title = context.get_string_property('title', True)
        #
        # root.baseUri = context.get_string_property('baseUri')
        # root.version = context.get('version')
        # root.mediaType = context.get_string_property('mediaType')

        # root.documentation = context.get_property_with_schema('documentation', APIRoot.documentation)
        # root.traits = parse_traits(context, APIRoot.traits.field_name, root.mediaType)
        # root.resourceTypes = parse_resource_type(context)

        resources = OrderedDict()
        for klass in hm.doc.classes:
            resource = APIResource()
            resource.displayName = "yolo"
            resource.description = "example of the api"
            # Parse methods

            methods = OrderedDict()

            for operation in hm.doc.classes[klass].operations:
                method = APIMethod(notNull=True)
                method.description = str(operation.subj)
                methods[str(operation.method)] = method

            if len(methods):
                resource.methods = methods

            resources[str(klass)] = resource  #parse_resource(context, property_name, root, root.mediaType)

        if resources > 0:
            root.resources = resources

        #
        # api = APIRoot()
        # g = Graph().parse(location, format='json-ld')

        return root

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print "Start tag:", tag
        for attr in attrs:
            print "     attr:", attr
    def handle_endtag(self, tag):
        print "End tag  :", tag
    def handle_data(self, data):
        if "Response" in data:
            print "Response     :",data
            return 1
        if "/" in data:
            print "Path     :",data
            return 1
        for method in ['POST','GET','DELETE','PUT']:
            if method in data:
                print "Resource     :", data
                return 1
        print "Data     :", data
    def handle_comment(self, data):
        print "Comment  :", data
    def handle_entityref(self, name):
        c = unichr(name2codepoint[name])
        print "Named ent:", c
    def handle_charref(self, name):
        if name.startswith('x'):
            c = unichr(int(name[1:], 16))
        else:
            c = unichr(int(name))
        print "Num ent  :", c
    def handle_decl(self, data):
        print "Decl     :", data

parser = MyHTMLParser()
example = """

HOST: http://www.google.com/

--- Sample API v2 ---
---
Welcome to the our sample API documentation. All comments can be written in (support [Markdown](http://daringfireball.net/projects/markdown/syntax) syntax)
---

--
Shopping Cart Resources
The following is a section of resources related to the shopping cart
--
List products added into your shopping-cart. (comment block again in Markdown)
GET /shopping-cart
< 200
< Content-Type: application/json
{ "items": [
  { "url": "/shopping-cart/1", "product":"2ZY48XPZ", "quantity": 1, "name": "New socks", "price": 1.25 }
] }

Save new products in your shopping cart
POST /shopping-cart
> Content-Type: application/json
{ "product":"1AB23ORM", "quantity": 2 }
< 201
< Content-Type: application/json
{ "status": "created", "url": "/shopping-cart/2" }


-- Payment Resources --
This resource allows you to submit payment information to process your *shopping cart* items
POST /payment
{ "cc": "12345678900", "cvc": "123", "expiry": "0112" }
< 200
{ "receipt": "/payment/receipt/1" }
"""

example2 = """
FORMAT: 1A

# Resource and Actions API
This API example demonstrates how to define a resource with multiple actions.

## API Blueprint
+ [Previous: The Simplest API](01.%20Simplest%20API.md)
+ [This: Raw API Blueprint](https://raw.github.com/apiaryio/api-blueprint/master/examples/02.%20Resource%20and%20Actions.md)
+ [Next: Named Resource and Actions](03.%20Named%20Resource%20and%20Actions.md)

# /message
This is our [resource](http://www.w3.org/TR/di-gloss/#def-resource). It is defined by its [URI](http://www.w3.org/TR/di-gloss/#def-uniform-resource-identifier) or, more precisely, by its [URI Template](http://tools.ietf.org/html/rfc6570).

This resource has no actions specified but we will fix that soon.

## GET
Here we define an action using the `GET` [HTTP request method](http://www.w3schools.com/tags/ref_httpmethods.asp) for our resource `/message`.

As with every good action it should return a [response](http://www.w3.org/TR/di-gloss/#def-http-response). A response always bears a status code. Code 200 is great as it means all is green. Responding with some data can be a great idea as well so let's add a plain text message to our response.

+ Response 200 (text/plain)

        Hello World!

## PUT
OK, let's add another action. This time to put new data to our resource (essentially an update action). We will need to send something in a [request](http://www.w3.org/TR/di-gloss/#def-http-request) and then send a response back confirming the posting was a success (HTTP Status Code 204 ~ Resource updated successfully, no content is returned).

+ Request (text/plain)

        All your base are belong to us.

+ Response 204
"""

# api = APIBlueprintsParser(example)
html = markdown.markdown(example2)
md = markdown.Markdown()
md.convert(example2)
# print(type(parser.feed(html)))
print md