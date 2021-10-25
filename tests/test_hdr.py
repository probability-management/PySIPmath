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

    @patch("metalog.metalog.fit")
    @patch("json.dump")
    @patch("builtins.open")
    def test_Json_contains_hdr_data_even_when_dependent(self, mock_open, mock_dump, mock_fit):
        mock_fit.return_value = fit_fixture()
        fixture = DataFrame(data={
            "Accounts": [10.24313638, 13.69812026, 12.62841292, 2.890162231, 7.60269451],
            "Products": [7.00895936, 11.61220758, 5.07099725, 7.542072262, 13.37670202],
        })
        PySIP.Json(fixture, "foo.json", "bar", dependence="dependent")

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

    @patch("metalog.metalog.fit")
    @patch("json.dump")
    @patch("builtins.open")
    def test_Json_respects_provided_seeds(self, mock_open, mock_dump, mock_fit):
        mock_fit.return_value = fit_fixture()
        provided_seeds = [1, 2, 3, 4, 5]
        fixture = DataFrame(data={
            "Accounts": [10.24313638, 13.69812026, 12.62841292, 2.890162231, 7.60269451],
            "Products": [7.00895936, 11.61220758, 5.07099725, 7.542072262, 13.37670202],
        })
        PySIP.Json(fixture, "foo.json", "bar", seeds=provided_seeds)

        self.assertListEqual(provided_seeds, mock_dump.call_args[0][0]["U01"]["rng"])

    @patch("builtins.print")
    @patch("metalog.metalog.fit")
    @patch("json.dump")
    @patch("builtins.open")
    def test_Json_reminds_minimum_number_of_provided_seeds(self, mock_open, mock_dump, mock_fit, mock_print):
        mock_fit.return_value = fit_fixture()
        provided_seeds = [1]
        fixture = DataFrame(data={
            "Accounts": [10.24313638, 13.69812026, 12.62841292, 2.890162231, 7.60269451],
            "Products": [7.00895936, 11.61220758, 5.07099725, 7.542072262, 13.37670202],
        })
        PySIP.Json(fixture, "foo.json", "bar", seeds=provided_seeds)

        print.assert_called_with(
            "RNG list length must be equal to or greater than the number of SIPs.")

if __name__ == '__main__':
    unittest.main()

