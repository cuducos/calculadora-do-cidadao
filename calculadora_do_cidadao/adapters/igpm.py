from urllib.parse import urlencode
from typing import NamedTuple

from calculadora_do_cidadao.adapters import Adapter
from calculadora_do_cidadao.fields import DateField, PercentField
from calculadora_do_cidadao.typing import MaybeIndexesGenerator


URL = "https://www3.bcb.gov.br/sgspub/consultarvalores/consultarValoresSeries.do"
URL_PARAMS = {
    "method": "consultarValores",
    "optSelecionaSerie": 189,
    "dataInicio": "30/06/1989",
    "selTipoArqDownload": 1,
    "hdOidSeriesSelecionadas": 189,
    "hdPaginar": "false",
    "bilServico": ["[SGSFW2301]"],
}


class Igpm(Adapter):
    """Adapter for FGV's IGPM series."""

    file_type = "html"
    url = f"{URL}?{urlencode(URL_PARAMS)}"

    COOKIES = {"dtcookie": "EB62E3A5ABDDF04A5F354D7F23CC2681|c2dzfDF8X2RlZmF1bHR8MQ"}
    IMPORT_KWARGS = {"encoding": "iso-8859-1", "index": 4}
    SHOULD_AGGREGATE = True

    def serialize(self, row: NamedTuple) -> MaybeIndexesGenerator:
        """Serialize method to discard the rows that are not valid data."""
        reference, value = row
        try:
            value = PercentField.deserialize(f"{value}%")
            reference = DateField.deserialize(reference)
        except ValueError:
            return
        yield reference, value
