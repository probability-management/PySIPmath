# -*- coding: utf-8 -*-

from .context import PySIP

import unittest
from unittest.mock import patch, mock_open
# from pandas import DataFrame

class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""
    m = mock_open()

    @patch('pandas.DataFrame')
    @patch("builtins.open", m, create=True)
    def test_Json_is_a_function(self, MockDataFrame):
        PySIP.Json(MockDataFrame(), "test-output.json", "bar")

    @patch('pandas.DataFrame')
    @patch("builtins.open", m, create=True)
    def test_Json_writes_a_file(self, MockDataFrame):
        PySIP.Json(MockDataFrame(), "foo.json", "bar")
        open.assert_called_with("foo.json", "w")

if __name__ == '__main__':
    unittest.main()
