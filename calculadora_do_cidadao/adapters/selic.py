from datetime import date
from typing import NamedTuple

from calculadora_do_cidadao.adapters import Adapter
from calculadora_do_cidadao.fields import DateField, PercentField
from calculadora_do_cidadao.months import MONTHS
from calculadora_do_cidadao.typing import MaybeIndexesGenerator


YEARS = tuple(range(1995, date.today().year + 1))
FIELD_TYPES = {f"field_{year}": PercentField for year in YEARS}


class Selic(Adapter):
    """Adapter for Brazilian Central Bank SELIC series."""

    url = "http://receita.economia.gov.br/orientacao/tributaria/pagamentos-e-parcelamentos/taxa-de-juros-selic"
    file_type = "html"

    SHOULD_AGGREGATE = True
    IMPORT_KWARGS = tuple(
        {"index": index, "force_types": FIELD_TYPES} for index in range(1, 4)
    )

    def serialize(self, row: NamedTuple) -> MaybeIndexesGenerator:
        """As each row contains more than one index this method might yield
        more than one `calculadora_do_cidadao.typing.Index`."""
        for year in YEARS:
            keys = (f"field_{year}", "mesano")
            value, month = (getattr(row, key) for key in keys)
            if value is None:
                continue

            reference = DateField.deserialize(f"{MONTHS[month]}/{year}")
            yield reference, value
