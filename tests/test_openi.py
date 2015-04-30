__author__ = 'mpetyx'

openi_server_url = "http://imagine.epu.ntua.gr:1988//api/doc/resources/"
schema = "http://imagine.epu.ntua.gr:1988/api/doc/schema"

import requests

from pyapi import API


server = requests.get(openi_server_url)

objects = server.json()['apis']

api_framework = API()

for object in objects:
    print openi_server_url + object['path']
    api_framework.parse(location=schema + object['path'], language="swagger")

    print api_framework.serialise("raml")