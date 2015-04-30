__author__ = 'mpetyx'

import os
import unittest

from pyapi import API


fixtures_dir = os.path.join(os.path.dirname(__file__), '../samples')


class TestSwaggerResources(unittest.TestCase):
    def setUp(self):
        self.api = API()

    def test_parse(self):
        self.assertIsNotNone(
            self.api.parse(location=os.path.join(fixtures_dir, 'issue_tracker.json'), language="hydra"))

    def tearDown(self):
        self.assertEqual(1, 1)


if __name__ == '__main__':
    unittest.main()