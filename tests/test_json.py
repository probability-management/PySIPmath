# -*- coding: utf-8 -*-

from .context import PySIP

import unittest
from unittest.mock import ANY, MagicMock, mock_open, patch
from unittest import TestCase

# from pandas import DataFrame


class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""

    @patch("builtins.open", mock_open(), create=True)
    @patch('pandas.DataFrame')
    def test_Json_opens_a_file_to_write(self, MockDataFrame):
        PySIP.Json(MockDataFrame(), "foo.json", "bar")
        open.assert_called_with("foo.json", "w")

    @patch("json.dump")
    @patch("builtins.open")
    @patch('pandas.DataFrame')
    def test_Json_dumps_a_dict(self, MockDataFrame, mock_open, mock_dump):
        PySIP.Json(MockDataFrame(), "foo.json", "bar")
        mock_dump.assert_called_with({
            'name': 'foo.json',
            'objectType': 'sipModel',
            'libraryType': 'SIPmath_3_0',
            'dateCreated': '10-25-2021',
            'provenance': 'bar',
            'U01': {'rng': []},
            'sips': [],
            'version': '1'
        }, ANY, indent=ANY)
        # TestCase().assertDictEqual({}, mock_dump.called)


if __name__ == '__main__':
    unittest.main()
