from datetime import date
from decimal import Decimal
from typing import NamedTuple

from calculadora_do_cidadao.adapters import Adapter
from calculadora_do_cidadao.fields import DateField
from calculadora_do_cidadao.months import MONTHS
from calculadora_do_cidadao.rows.fields import PercentField
from calculadora_do_cidadao.typing import MaybeIndexesGenerator


class IbgeAdapter(Adapter):
    """This base class is incomplete and should not be used directly. It missed
    the `url` class variable to be set in its children. In spite of that, it
    implements the serialize and settings that work with most price adjustment
    indexes done by IBGE."""

    file_type = "xls"

    IMPORT_KWARGS = {"end_column": 2}
    SHOULD_UNZIP = True

    def serialize(self, row: NamedTuple) -> MaybeIndexesGenerator:
        """Serialize used for different IBGE price adjustment indexes."""
        self.last_year = getattr(self, "last_year", None)
        year, month, value = row
        if value is None or month is None:
            return

        if year is None:
            year = ""
        year = year.strip() or self.last_year

        try:
            month = MONTHS[month.capitalize()]
        except KeyError:
            return

        value = PercentField.deserialize(f"{value}%")
        reference = DateField.deserialize(f"{month}/{year}")

        self.last_year = year
        yield reference, value


class Inpc(IbgeAdapter):
    """Adapter for IBGE's INPC series."""

    url = "http://ftp.ibge.gov.br/Precos_Indices_de_Precos_ao_Consumidor/INPC/Serie_Historica/inpc_SerieHist.zip"


class Ipca(IbgeAdapter):
    """Adapter for IBGE's IPCA series."""

    url = "http://ftp.ibge.gov.br/Precos_Indices_de_Precos_ao_Consumidor/IPCA/Serie_Historica/ipca_SerieHist.zip"


class Ipca15(IbgeAdapter):
    """Adapter for IBGE's IPCA-15 series."""

    url = "http://ftp.ibge.gov.br/Precos_Indices_de_Precos_ao_Consumidor/IPCA_15/Series_Historicas/ipca-15_SerieHist.zip"


class IpcaE(IbgeAdapter):
    """Adapter for IBGE's IPCA-E series."""

    url = "http://ftp.ibge.gov.br/Precos_Indices_de_Precos_ao_Consumidor/IPCA_E/Series_Historicas/ipca-e_SerieHist.zip"
