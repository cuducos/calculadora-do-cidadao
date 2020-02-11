from datetime import date
from decimal import Decimal
from typing import NamedTuple
from urllib.parse import urlencode

from rows.fields import DecimalField, DateField

from calculadora_do_cidadao.adapters import Adapter
from calculadora_do_cidadao.months import MONTHS
from calculadora_do_cidadao.typing import MaybeIndexesGenerator


today_date = str(date.today())

URL = "https://fred.stlouisfed.org/graph/fredgraph.xls"
URL_PARAMS = {
    "bgcolor": "%23e1e9f0",
    "chart_type": "line",
    "drp": "0",
    "fo": "open%20sans",
    "graph_bgcolor": "%23ffffff",
    "height": "450",
    "mode": "fred",
    "recession_bars": "on",
    "txtcolor": "%23444444",
    "ts": "12",
    "tts": "12",
    "width": "1168",
    "nt": "0",
    "thu": "0",
    "trc": "0",
    "show_legend": "yes",
    "show_axis_titles": "yes",
    "show_tooltip": "yes",
    "id": "CPIAUCSL",
    "scale": "left",
    "cosd": "1947-01-01",
    "coed": "2019-12-01",
    "line_color": "%234572a7",
    "link_values": "false",
    "line_style": "solid",
    "mark_type": "none",
    "mw": "3",
    "lw": "2",
    "ost": "99999",
    "oet": "99999",
    "mma": "0",
    "fml": "a",
    "fq": "Monthly",
    "fam": "avg",
    "fgst": "lin",
    "fgsnd": "2009-06-01",
    "line_index": "1",
    "transformation": "lin",
    "vintage_date": today_date,
    "revision_date": today_date,
    "nd": "1947-01-01",
}


class Cpiaucsl(Adapter):
    """Adapter for CPIAUCSL's FED's series."""

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
