from datetime import date
from decimal import Decimal
from typing import NamedTuple, Tuple, Union

from calculadora_do_cidadao.base import Adapter
from calculadora_do_cidadao.months import MONTHS


class Ipca(Adapter):
    url = "ftp://ftp.ibge.gov.br/Precos_Indices_de_Precos_ao_Consumidor/IPCA/Serie_Historica/ipca_SerieHist.zip"
    IMPORT_KWARGS = {"end_column": 2}

    def serialize(self, row: NamedTuple) -> Union[Tuple[date, Decimal], None]:
        self.last_year = getattr(self, "last_year", None)
        year, month, value = row
        if month not in MONTHS.keys():
            return None

        year = int(year or self.last_year)
        month = MONTHS[month]
        reference_date = self.round_date(date(year, month, 1))
        value = Decimal(value) / 100
        self.last_year = year

        return reference_date, value
