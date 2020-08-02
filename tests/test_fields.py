import datetime
from decimal import Decimal

import pytest

from calculadora_do_cidadao.fields import DateField, PercentField


def test_PercentField():
    assert PercentField.deserialize("12,37%") == Decimal("0.1237")
    assert PercentField.deserialize("12.37%") == Decimal("0.1237")


def test_DateField():
    assert DateField.deserialize("2020-07-31") == datetime.date(2020, 7, 31)
    assert DateField.deserialize("31/07/2020") == datetime.date(2020, 7, 31)
    assert DateField.deserialize("2020-07") == datetime.date(2020, 7, 1)
    assert DateField.deserialize("07/2020") == datetime.date(2020, 7, 1)
    assert DateField.deserialize("Jul/2020") == datetime.date(2020, 7, 1)
    assert DateField.deserialize("2020") == datetime.date(2020, 1, 1)
    assert DateField.deserialize(2020) == datetime.date(2020, 1, 1)

    with pytest.raises(ValueError):
        DateField.deserialize(42)
    with pytest.raises(ValueError):
        DateField.deserialize("hello, world")
