import unittest
from unittest.mock import ANY, patch
from pandas import DataFrame
import PySIP
from tests.fixtures.fit import fit_fixture

class HDRTestSuite(unittest.TestCase):
    """Basic test cases."""

    @patch("metalog.metalog.fit")
    @patch("json.dump")
    @patch("builtins.open")
    def test_Json_contains_hdr_data(self, mock_open, mock_dump, mock_fit):
        mock_fit.return_value = fit_fixture()
        fixture = DataFrame(data={
            "Accounts": [10.24313638, 13.69812026, 12.62841292, 2.890162231, 7.60269451],
            "Products": [7.00895936, 11.61220758, 5.07099725, 7.542072262, 13.37670202],
        })
        PySIP.Json(fixture, "foo.json", "bar")

        self.assertDictEqual({
            'arguments': {
                'counter': 'PM_Index',
                'entity': 1,
                'seed3': 0,
                'seed4': 0,
                'varId': ANY
            },
            'function': 'HDR_2_0',
            'name': 'hdr1'
        }, mock_dump.call_args[0][0]["U01"]["rng"][0])

if __name__ == '__main__':
    unittest.main()

