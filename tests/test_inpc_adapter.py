from datetime import date
from decimal import Decimal

import pytest

from calculadora_do_cidadao.adapters import Inpc
from calculadora_do_cidadao.base import AdapterDateNotAvailableError


@pytest.mark.parametrize(
    "original,value,target,expected",
    (
        (date(2014, 3, 6), None, None, "1.361007124894175467688242800"),
        (date(2011, 5, 8), 9, None, "14.373499236614377437778943450"),
        (date(2009, 1, 12), 5, date(2013, 8, 1), "6.410734265150376567640231785"),
    ),
)
def test_data(original, value, target, expected, inpc_fixture, mocker):
    download = mocker.patch("calculadora_do_cidadao.base.Download")
    download.return_value.return_value.__enter__.return_value = inpc_fixture
    inpc = Inpc()
    assert len(inpc.data) == 312
    assert inpc.adjust(original, value, target) == pytest.approx(Decimal(expected))

    msg = r"This adapter has data from 01/1994 to 12/2019\. 02/2020 is out of range\."
    with pytest.raises(AdapterDateNotAvailableError, match=msg):
        inpc.adjust(date(2020, 2, 1))
