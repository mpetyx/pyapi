__author__ = 'mpetyx'

import os
import unittest

from pyapi import API


fixtures_dir = os.path.join(os.path.dirname(__file__), '../samples/v2.0/json')


class TestPestoreResources(unittest.TestCase):
    def setUp(self):
        self.api = API()

    def test_parse_petstore(self):
        self.api.parse(location=os.path.join(fixtures_dir, 'petstore.json'), language="swagger")

    def test_serialise_raml_petstore(self):
        self.assertIsNotNone(self.api.serialise(language="raml"))

    def test_serialise_hydra_petstore(self):
        self.assertIsNotNone(self.api.serialise(language="hydra"))

    def test_serialise_swagger_petstore(self):
        self.assertIsNotNone(self.api.serialise(language="swagger"))


    def tearDown(self):
        assert 1 == 1


if __name__ == '__main__':
    unittest.main()