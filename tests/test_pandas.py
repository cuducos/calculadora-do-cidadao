from decimal import Decimal
from unittest import TestCase
from unittest.mock import patch

from pandas import Series
from pandas.testing import assert_series_equal

from calculadora_do_cidadao import Ipca as OriginalIpca
from calculadora_do_cidadao.pandas import Ipca
from tests import get_fixture


class TestPandasUseCase(TestCase):
    @staticmethod
    def assert_decimal_series_equal(left, right, **kwargs):
        return assert_series_equal(left.astype(float), right.astype(float), **kwargs)

    @patch("calculadora_do_cidadao.adapters.Download")
    def test_one_argument(self, download):
        fixture = get_fixture(OriginalIpca)
        download.return_value.return_value.__enter__.return_value = fixture

        adpater = Ipca()
        series = Series(("2006-07-01",))
        self.assert_decimal_series_equal(
            adpater.adjust(series),
            Series((Decimal(2.062688036971558),)),
        )
