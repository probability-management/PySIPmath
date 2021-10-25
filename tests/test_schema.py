import json
import unittest
from unittest.mock import patch
import jsonschema
from jsonschema import validate
from pandas import DataFrame
from tests.fixtures.fit import fit_fixture

import PySIP

schema = json.load(open('tests/multi-lib-schema-2021-08-19.json', 'r'))


class SchemaTestSuite(unittest.TestCase):
    @patch("metalog.metalog.fit")
    @patch("json.dump")
    @patch("builtins.open")
    def test_Json_conforms_to_a_schema(self, mock_open, mock_dump, mock_fit):
        mock_fit.return_value = fit_fixture()
        fixture = DataFrame(data={
            "Accounts": [10.24313638, 13.69812026, 12.62841292, 2.890162231, 7.60269451],
            "Products": [7.00895936, 11.61220758, 5.07099725, 7.542072262, 13.37670202],
        })
        PySIP.Json(fixture, "foo.json", "bar")
        validate(instance=mock_dump.call_args[0][0], schema=schema)
