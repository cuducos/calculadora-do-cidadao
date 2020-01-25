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
    """Field for mmm/yyyy dates."""

    INPUT_FORMAT = "%b/%Y"
