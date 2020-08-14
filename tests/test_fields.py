from datetime import date, datetime
from decimal import Decimal

import pytest

from calculadora_do_cidadao.fields import DateField, PercentField


@pytest.mark.parametrize("value", ("12.37%", "12,37%"))
def test_percent_field(value):
    assert PercentField.deserialize(value) == Decimal("0.1237")


@pytest.mark.parametrize(
    "value",
    (
        date(2018, 7, 6),
        datetime(2018, 7, 6, 21, 0, 0),
        "2018-07-06T21:00:00",
        "2018-07-06 21:00:00",
        "2018-07-06",
        "06/07/2018",
        1530925200,
        1530925200.0,
    ),
)
def test_date_field_with_complete_dates(value):
    assert DateField.deserialize(value) == date(2018, 7, 6)


@pytest.mark.parametrize(
    "value", ("2018-07", "Jul/2018", "Jul-2018", "Jul 2018", "07/2018",),
)
def test_date_field_with_incomplete_dates(value):
    assert DateField.deserialize(value) == date(2018, 7, 1)


def test_date_field_with_only_year():
    assert DateField.deserialize("2018") == date(2018, 1, 1)


def test_date_field_error():
    with pytest.raises(ValueError):
        DateField.deserialize("hello, world")
