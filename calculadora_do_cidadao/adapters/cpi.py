from typing import NamedTuple
from urllib.parse import urlencode

from calculadora_do_cidadao.adapters import Adapter
from calculadora_do_cidadao.rows.fields import DecimalField
from calculadora_do_cidadao.typing import MaybeIndexesGenerator


URL = "https://fred.stlouisfed.org/graph/fredgraph.xls"
URL_PARAMS = {"id": "CPIAUCSL"}


class AllUrbanCityAverage(Adapter):
    """Adapter for FED's Consumer Price Index for All Urban Consumers: All
    Items."""

    file_type = "xls"
    url = f"{URL}?{urlencode(URL_PARAMS)}"

    IMPORT_KWARGS = {"start_row": 10, "force_types": {"cpiaucsl": DecimalField}}

    def serialize(self, row: NamedTuple) -> MaybeIndexesGenerator:
        """Serialize method to unpack Rows's row into a tuple."""
        reference, value = row
        yield reference, value
