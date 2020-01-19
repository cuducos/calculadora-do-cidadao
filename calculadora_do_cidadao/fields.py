from rows import fields


class PercentField(fields.PercentField):
    @classmethod
    def deserialize(cls, value):
        value = value or ""
        return super().deserialize(value.replace(",", "."))
