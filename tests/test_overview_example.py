__author__ = 'mpetyx'

from unittest import TestCase
import unittest
import logging
import sys

from pyapi import API


class TestpyAPI(TestCase):
    def setUp(self):
        # print "Setting up the coverage unit test for pyapi"
        self.document = API()
        self.api = API().parse(location="url", language="raml")

    def test_swagger_serialise(self):
        self.assertEqual(self.api.serialise(language="swagger"), {}, "Swagger could not be serialised properly")

    def test_raml_serialise(self):
        self.assertEqual(self.api.serialise(language="raml"), {}, "RAML could not be serialised properly")

    def test_hydra_serialise(self):
        self.assertEqual(self.api.serialise(language="hydra"), {}, "Hydra could not be serialised properly")

    def test_blueprint_serialise(self):
        self.assertEqual(self.api.serialise(language="blueprint"), {},
                         "API blueprint could not be serialised properly")

    def test_query(self):
        # print "sample"
        self.assertEqual(1, 2, "There are not equal at all!")

    # ending the test
    def tearDown(self):
        """Cleaning up after the test"""
        self.log.debug("finalising the test")


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stderr)
    logging.getLogger("SomeTest.testSomething").setLevel(logging.DEBUG)
    unittest.main()
