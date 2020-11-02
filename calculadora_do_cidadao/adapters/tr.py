from urllib.parse import urlencode
from typing import NamedTuple

from calculadora_do_cidadao.adapters import Adapter
from calculadora_do_cidadao.fields import DateField, PercentField
from calculadora_do_cidadao.typing import MaybeIndexesGenerator


URL = "https://www3.bcb.gov.br/sgspub/consultarvalores/consultarValoresSeries.do?method=consultarValores"
URL_PARAMS = {
    "method": "consultarValores",
    "optSelecionaSerie": 226,
    "dataInicio": "01/02/1991",
    "selTipoArqDownload": 0,
    "hdOidSeriesSelecionadas": 226,
    "hdPaginar": "true",
    "bilServico": ["[SGSFW2301]"],
}


class Tr(Adapter):
    """Adapter for TR's series."""

    file_type = "html"
    url = f"{URL}?{urlencode(URL_PARAMS)}"

    COOKIES = {"dtcookie": "1EB1526DDB7684F148B5E7B66DDF9646|Y2FsY2lkYWRhb3wwfF9kZWZhdWx0fDF8c2dzfDE"}
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
