from datetime import date, datetime
from decimal import Decimal
from typing import Union

from calculadora_do_cidadao.rows import fields
from calculadora_do_cidadao.typing import Date


class PercentField(fields.PercentField):
    """Field for reading percentage in Brazilian Portuguese format."""

    @classmethod
    def deserialize(cls, value: str) -> Decimal:  # type: ignore
        """Deserialize decimals using a comma as a decimal separator."""
        value = value or ""
        return super().deserialize(value.replace(",", "."))


class DateField(fields.DateField):
    """DateField which supports different date formats, including Brazilian"""

    INPUT_FORMATS = (
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%Y-%m",
        "%m/%Y",
        "%b/%Y",
        "%b-%Y",
        "%b %Y",
        "%Y",
    )

    @classmethod
    def deserialize(cls, value: Date, *args, **kwargs) -> date:
        if isinstance(value, datetime):
            return value.date()

        if isinstance(value, date):
            return value

        if isinstance(value, (int, float)):
            return datetime.fromtimestamp(value).date()

        value = fields.Field.deserialize(value)
        as_str: str = fields.as_string(value)
        as_str = as_str[:10]  # in ISO format datetime, discard chars after date
        for date_format in cls.INPUT_FORMATS:
            try:
                dt_object = datetime.strptime(as_str, date_format)
            except ValueError:
                continue
            return dt_object.date()

        raise ValueError(f"Cannot parse value as date: {value}")
