from datetime import date
from decimal import Decimal
from typing import NamedTuple

from calculadora_do_cidadao.base import Adapter
from calculadora_do_cidadao.months import MONTHS
from calculadora_do_cidadao.typing import MaybeIndexesGenerator


class Ipca15(Adapter):
    url = "ftp://ftp.ibge.gov.br/Precos_Indices_de_Precos_ao_Consumidor/IPCA_15/Series_Historicas/ipca-15_SerieHist.zip"
    file_type = "xls"

    IMPORT_KWARGS = {"end_column": 2}
    SHOULD_UNZIP = True

    def serialize(self, row: NamedTuple) -> MaybeIndexesGenerator:
        self.last_year = getattr(self, "last_year", None)
        year, month, value = row
        if month not in MONTHS.keys():
            return

        year = int(year or self.last_year)
        month = MONTHS[month]
        reference_date = self.round_date(date(year, month, 1))
        value = Decimal(value) / 100
        self.last_year = year

        yield reference_date, value
