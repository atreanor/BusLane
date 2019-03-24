# -*- coding: utf-8 -*-

from sample import *

import unittest


class AdvancedTestSuite(unittest.TestCase):
    """Advanced test cases."""

    def test_thoughts(self):
        self.assertIsNone(sample.helpers())


if __name__ == '__main__':
    unittest.main()
