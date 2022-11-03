from datetime import date
from decimal import Decimal
from typing import NamedTuple
from urllib.parse import urlencode

from calculadora_do_cidadao.adapters import Adapter
from calculadora_do_cidadao.fields import DateField
from calculadora_do_cidadao.typing import MaybeIndexesGenerator


URL = "https://www3.bcb.gov.br/novoselic/rest/fatoresAcumulados/pub/search"
URL_PARAMS = {
    "parametrosOrdenacao": '[{"nome":"periodo","decrescente":false}]',
    "page": 1,
    "pageSize": 48,
}


class Selic(Adapter):
    """Adapter for Brazilian Central Bank SELIC series."""

    url = f"{URL}?{urlencode(URL_PARAMS)}"
    file_type = "json"

    HEADERS = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br",
    }
    POST_DATA = (
        {
            "campoPeriodo": "mensal",
            "dataInicial": "",
            "dataFinal": "",
            "ano": year,
            "exibirMeses": True,
        }
        for year in range(date.today().year, 1996, -1)
    )
    IMPORT_KWARGS = {"json_path": ["registros"]}
    SHOULD_AGGREGATE = True

    def serialize(self, row: NamedTuple) -> MaybeIndexesGenerator:
        reference = DateField.deserialize(row.periodo.replace(" ", ""))  # type: ignore
        value = Decimal(row.fator)  # type: ignore
        yield reference, value

    def aggregate(self):
        accumulated = 1
        for key in sorted(self.data.keys()):
            self.data[key] = accumulated * self.data[key]
            accumulated = self.data[key]
