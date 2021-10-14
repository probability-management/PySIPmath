# -*- coding: utf-8 -*-

from .context import PySIP

import unittest
from unittest.mock import patch, mock_open
# from pandas import DataFrame

class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""
    m = mock_open()

    @patch('pandas.DataFrame')
    def test_Json_is_a_function(self, MockDataFrame):
        PySIP.Json(MockDataFrame(), "test-output.json", "bar")

if __name__ == '__main__':
    unittest.main()
