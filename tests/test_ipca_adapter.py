from datetime import date
from decimal import Decimal

import pytest

from calculadora_do_cidadao.adapters import Ipca
from calculadora_do_cidadao.base import AdapterDateNotAvailableError


@pytest.mark.parametrize(
    "original,value,target,expected",
    (
        (date(2018, 7, 6), None, None, "1.051202206630561280035407253"),
        (date(2014, 7, 8), 7, None, "9.407523138792336916983267321"),
        (date(1998, 7, 12), 3, date(2006, 7, 1), "5.279855889296777979447848574"),
    ),
)
def test_data(original, value, target, expected, ipca_fixture, mocker):
    download = mocker.patch("calculadora_do_cidadao.base.Download")
    download.return_value.return_value.__enter__.return_value = ipca_fixture
    ipca = Ipca()
    assert len(ipca.data) == 312
    assert ipca.adjust(original, value, target) == pytest.approx(Decimal(expected))

    msg = r"This adapter has data from 01/1994 to 12/2019\. 01/2020 is out of range\."
    with pytest.raises(AdapterDateNotAvailableError, match=msg):
        ipca.adjust(date(2020, 1, 1))
