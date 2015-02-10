__author__ = 'mpetyx'

import os
from pyapi import API
import unittest
fixtures_dir = os.path.join(os.path.dirname(__file__), '../samples/v2.0/json')

class TestSwaggerResources(unittest.TestCase):

    def setUp(self):

        self.api = API()

    def test_petstore(self):
        self.api.parse(location=os.path.join(fixtures_dir, 'petstore.json'), language="swagger")
        self.assertEqual(self.api.serialise(language="raml"),"")


    def tearDown(self):
        assert 1==1


if __name__ == '__main__':
    unittest.main()