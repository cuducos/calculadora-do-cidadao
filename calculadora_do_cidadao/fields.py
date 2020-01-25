from rows import fields


class PercentField(fields.PercentField):
    """Field for reading decimals in Brazilian Portuguese format."""

    @classmethod
    def deserialize(cls, value):
        """Deserialize decimals using a comma as a decimal separator."""
        value = value or ""
        return super().deserialize(value.replace(",", "."))
