from datetime import date
from decimal import Decimal

import pytest

from calculadora_do_cidadao.adapters import Ipca15
from calculadora_do_cidadao.base import AdapterDateNotAvailableError


@pytest.mark.parametrize(
    "original,value,target,expected",
    (
        (date(2017, 2, 13), None, None, "1.101569276203612423894969769"),
        (date(2012, 5, 8), 3, None, "4.577960384607494629737626417"),
        (date(1999, 11, 10), 5, date(2002, 9, 5), "6.068815714507691510850986688"),
    ),
)
def test_data(original, value, target, expected, ipca15_fixture, mocker):
    download = mocker.patch("calculadora_do_cidadao.base.Download")
    download.return_value.return_value.__enter__.return_value = ipca15_fixture
    ipca15 = Ipca15()
    assert len(ipca15.data) == 312
    assert ipca15.adjust(original, value, target) == pytest.approx(Decimal(expected))

    msg = r"This adapter has data from 01/1994 to 12/2019\. 02/2020 is out of range\."
    with pytest.raises(AdapterDateNotAvailableError, match=msg):
        ipca15.adjust(date(2020, 2, 1))
