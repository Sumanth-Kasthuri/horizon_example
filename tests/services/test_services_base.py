"""
Author: Archie Jarvis
Student ID: 20022663
"""


import unittest

from tests import test_utils


class BaseServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.session = test_utils.create_test_session()

    def tearDown(self):
        self.session.close()
