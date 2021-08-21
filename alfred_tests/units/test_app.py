# coding=utf-8

import unittest
from alfred.__main__ import main


class AppTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_test1(self):
        # Assign
        # Acts
        main()
        # Assert
        self.assertEqual(0, 0)
