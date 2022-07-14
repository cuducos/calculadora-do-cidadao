from decimal import Decimal
from unittest import TestCase

from pandas import Series

from calculadora_do_cidadao.pandas import Ipca


class TestPandasUseCase(TestCase):
    def test_one_argument(self):
        adpater = Ipca()
        series = Series(("2020-01-1",))
        self.assertEqual(
            adpater.adjust(series),
            Series((Decimal(0.3123),)),
        )
