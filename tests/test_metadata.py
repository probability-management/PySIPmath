import unittest
from unittest.mock import ANY, patch
from tests.fixtures.fit import fit_fixture
from pandas import DataFrame

from .context import PySIP

class MetadataTestSuite(unittest.TestCase):
    """Metadata test cases."""

    @patch("metalog.metalog.fit")
    @patch("json.dump")
    @patch("builtins.open")
    def test_Json_contains_metadata(self, mock_open, mock_dump, mock_fit):
        mock_fit.return_value = fit_fixture()
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

    @patch("metalog.metalog.fit")
    @patch("json.dump")
    @patch("builtins.open")
    def test_Json_contains_density_metadata(self, mock_open, mock_dump, mock_fit):
        mock_fit.return_value = fit_fixture()
        fixture = DataFrame(data={
            "Accounts": [10.24313638, 13.69812026, 12.62841292, 2.890162231, 7.60269451],
            "Products": [7.00895936, 11.61220758, 5.07099725, 7.542072262, 13.37670202],
        })
        PySIP.Json(fixture, "foo.json", "bar")
        # These numbers are derived from the `fit_fixture`, and differ from those derived
        # from the original metalog.metalog.fit, somehow.
        self.assertListEqual([
            0.0025771154162709774,
            0.07982657640547815,
            0.029550125014221145,
            0.017235957098999936,
            0.011535801921317236,
            0.008261040431818098,
            0.006143783605397077,
            0.004674061970193781,
            0.003647715373304234,
            0.002885727261202881,
            0.0022485786991766413,
            0.0018531373331520753,
            0.0015078193031848432,
            0.001162501273217611,
            0.0009057936754070011,
            0.0007265846238809351,
            0.000586335727297715,
            0.0004729949810635803,
            0.0003819172217154018,
            0.00030610153965857025,
            0.000250857227215982,
            0.0002006087608621535,
            0.00016834437845785648,
            0.00013607999605355945,
            0.00010381561364926245
        ], mock_dump.call_args[0][0]["sips"][0]["metadata"]["density"])


if __name__ == '__main__':
    unittest.main()
