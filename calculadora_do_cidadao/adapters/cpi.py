from datetime import date
from decimal import Decimal
from typing import NamedTuple
from urllib.parse import urlencode

from rows.fields import DecimalField, DateField

from calculadora_do_cidadao.adapters import Adapter
from calculadora_do_cidadao.months import MONTHS
from calculadora_do_cidadao.typing import MaybeIndexesGenerator


URL = "https://fred.stlouisfed.org/graph/fredgraph.xls"
URL_PARAMS = {
    "id": "CpiAllUrbanCityAverage",
}


class CpiAllUrbanCityAverage(Adapter):
    """Adapter for FED's Consumer Price Index for
    All Urban Consumers: All Items (CpiAllUrbanCityAverage)"""

    file_type = "xls"

    url = f"{URL}?{urlencode(URL_PARAMS)}"

    def serialize(self, row: NamedTuple) -> MaybeIndexesGenerator:
        """Serialize method to discard the rows that are not valid data."""
        reference, value = row

        try:
            reference = DateField.deserialize(reference)
            value = DecimalField.deserialize(value)
        except ValueError:
            return

        if reference is None or value is None:
            return

        yield reference, value
