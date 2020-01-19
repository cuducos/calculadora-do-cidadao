from datetime import date
from typing import NamedTuple

from calculadora_do_cidadao.base import Adapter
from calculadora_do_cidadao.fields import PercentField
from calculadora_do_cidadao.months import MONTHS
from calculadora_do_cidadao.typing import MaybeIndexesGenerator


YEARS = tuple(range(1995, date.today().year + 1))
FIELD_TYPES = {f"field_{year}": PercentField for year in YEARS}


class Selic(Adapter):
    url = "http://receita.economia.gov.br/orientacao/tributaria/pagamentos-e-parcelamentos/taxa-de-juros-selic"
    file_type = "html"

    SHOULD_AGGREGATE = True
    IMPORT_KWARGS = tuple(
        {"index": index, "force_types": FIELD_TYPES} for index in range(1, 4)
    )

    def serialize(self, row: NamedTuple) -> MaybeIndexesGenerator:
        for year in YEARS:
            value = getattr(row, f"field_{year}")
            month = MONTHS[getattr(row, "mesano")]
            if value is None:
                continue
            yield self.round_date(date(year, month, 1)), value
