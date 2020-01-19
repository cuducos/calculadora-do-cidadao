from datetime import date
from decimal import Decimal

import pytest

from calculadora_do_cidadao.adapters import Selic
from calculadora_do_cidadao.base import AdapterDateNotAvailableError


@pytest.mark.parametrize(
    "original,expected",
    (
        (date(2019, 11, 1), "1.0037"),
        (date(2019, 10, 1), "1.00751406"),
        (date(2019, 9, 1), "1.012350127488"),
    ),
)
def test_data(original, expected, selic_fixture, mocker):
    download = mocker.patch("calculadora_do_cidadao.base.Download")
    download.return_value.return_value.__enter__.return_value = selic_fixture
    selic = Selic()
    assert len(selic.data) == 300
    assert selic.adjust(original) == Decimal(expected)

    msg = r"This adapter has data from 01/1995 to 12/2019\. 01/2020 is out of range\."
    with pytest.raises(AdapterDateNotAvailableError, match=msg):
        selic.adjust(date(2020, 1, 1))
