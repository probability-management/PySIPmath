# -*- coding: utf-8 -*-

from .context import PySIP

import unittest
from unittest.mock import ANY, MagicMock, mock_open, patch
from unittest import TestCase

from pandas import DataFrame


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
        PySIP.Json(MockDataFrame, "foo.json", "bar")
        self.assertEqual({
            'name': 'foo.json',
            'objectType': 'sipModel',
            'libraryType': 'SIPmath_3_0',
            'dateCreated': '10-25-2021',
            'provenance': 'bar',
            'U01': {'rng': []},
            'sips': [],
            'version': '1'
        }, mock_dump.call_args[0][0])

    @patch("json.dump")
    @patch("builtins.open")
    def test_Json_contains_metadata(self, mock_open, mock_dump):
        self.maxDiff = 800
        fixture = DataFrame(data={
            "Accounts": [10.24313638, 13.69812026, 12.62841292, 2.890162231, 7.60269451],
            "Products": [7.00895936, 11.61220758, 5.07099725, 7.542072262, 13.37670202],
        })
        PySIP.Json(fixture, "foo.json", "bar")
        self.assertDictEqual({
            'P25': 7.60269451,
            'P50': 10.24313638,
            'P75': 12.62841292,
            'count': 5.0,
            'density': ANY,
            'max': 13.69812026,
            'mean': 9.4125052602,
            'min': 2.890162231,
            'std': 4.336325622060243
        }, mock_dump.call_args[0][0]["sips"][0]["metadata"])

    @patch("json.dump")
    @patch("builtins.open")
    def test_Json_contains_density_metadata(self, mock_open, mock_dump):
        self.maxDiff = 800
        fixture = DataFrame(data={
            "Accounts": [10.24313638, 13.69812026, 12.62841292, 2.890162231, 7.60269451],
            "Products": [7.00895936, 11.61220758, 5.07099725, 7.542072262, 13.37670202],
        })
        PySIP.Json(fixture, "foo.json", "bar")
        self.assertListEqual([
            999.9999999999998,
            1000.0,
            1000.0,
            1000.0,
            1000.0,
            1000.0,
            1000.0,
            1000.0,
            1000.0,
            1000.0,
            1000.0,
            1000.0,
            1000.0,
            1000.0,
            1000.0,
            1000.0,
            1000.0,
            1000.0,
            1000.0,
            1000.0,
            1000.0,
            1000.0,
            1000.0,
            1000.0,
            999.9999999999998
        ], mock_dump.call_args[0][0]["sips"][0]["metadata"]["density"])


if __name__ == '__main__':
    unittest.main()
