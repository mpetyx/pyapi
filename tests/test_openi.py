__author__ = 'mpetyx'

openi_server_url = "https://demo2.openi-ict.eu/v.04/"
openi_server_url = "https://demo2.openi-ict.eu/api-spec/v1/api_framework"
openi_server_url = "http://localhost:8000/api/doc/schema/Account/"

from pyapi import API

api_framework = API()

api_framework.parse(location=openi_server_url, language="swagger")

print api_framework.serialise("raml")