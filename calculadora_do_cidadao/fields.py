import datetime
from decimal import Decimal

from rows import fields


class PercentField(fields.PercentField):
    """Field for reading percentage in Brazilian Portuguese format."""

    @classmethod
    def deserialize(cls, value: str) -> Decimal:
        """Deserialize decimals using a comma as a decimal separator."""
        value = value or ""
        return super().deserialize(value.replace(",", "."))


class DateField(fields.DateField):
    """DateField which supports different date formats, including Brazilian"""

    INPUT_FORMATS = ("%Y-%m-%d", "%d/%m/%Y", "%Y-%m", "%m/%Y", "%b/%Y", "%Y")

    @classmethod
    def deserialize(cls, value, *args, **kwargs):
        value = fields.Field.deserialize(value)
        value = fields.as_string(value)

        for date_format in cls.INPUT_FORMATS:
            try:
                dt_object = datetime.datetime.strptime(value, date_format)
            except ValueError:
                continue
            else:
                return datetime.date(dt_object.year, dt_object.month, dt_object.day)
        raise ValueError("Cannot parse value as date: {}".format(value))
