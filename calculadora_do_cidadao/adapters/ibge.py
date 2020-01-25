from datetime import date
from decimal import Decimal
from typing import NamedTuple

from calculadora_do_cidadao.adapters import Adapter
from calculadora_do_cidadao.months import MONTHS
from calculadora_do_cidadao.typing import MaybeIndexesGenerator


class IbgeAdapter(Adapter):
    file_type = "xls"

    IMPORT_KWARGS = {"end_column": 2}
    SHOULD_UNZIP = True

    def serialize(self, row: NamedTuple) -> MaybeIndexesGenerator:
        self.last_year = getattr(self, "last_year", None)
        year, month, value = row
        if month not in MONTHS.keys():
            return

        if year is None:
            year = ""

        year = int(year.strip() or self.last_year)
        month = MONTHS[month]
        reference_date = self.round_date(date(year, month, 1))
        value = Decimal(value) / 100
        self.last_year = year
        yield reference_date, value


class Inpc(IbgeAdapter):
    url = "ftp://ftp.ibge.gov.br/Precos_Indices_de_Precos_ao_Consumidor/INPC/Serie_Historica/inpc_SerieHist.zip"


class Ipca(IbgeAdapter):
    url = "ftp://ftp.ibge.gov.br/Precos_Indices_de_Precos_ao_Consumidor/IPCA/Serie_Historica/ipca_SerieHist.zip"


class Ipca15(IbgeAdapter):
    url = "ftp://ftp.ibge.gov.br/Precos_Indices_de_Precos_ao_Consumidor/IPCA_15/Series_Historicas/ipca-15_SerieHist.zip"


class IpcaE(IbgeAdapter):
    url = "ftp://ftp.ibge.gov.br/Precos_Indices_de_Precos_ao_Consumidor/IPCA_E/Series_Historicas/ipca-e_SerieHist.zip"
