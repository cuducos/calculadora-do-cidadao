from datetime import date, datetime
from decimal import Decimal
from itertools import chain
from statistics import mean
from typing import NamedTuple, Optional

from rows.fields import TextField

from calculadora_do_cidadao.adapters import Adapter
from calculadora_do_cidadao.typing import MaybeIndexesGenerator


ALL_CITIES = (
    "aracaju",
    "belem",
    "belo_horizonte",
    "boa_vista",
    "brasilia",
    "campo_grande",
    "cuiaba",
    "curitiba",
    "florianopolis",
    "fortaleza",
    "goiania",
    "joao_pessoa",
    "macae",
    "macapa",
    "maceio",
    "manaus",
    "natal",
    "palmas",
    "porto_alegre",
    "porto_velho",
    "recife",
    "rio_branco",
    "rio_de_janeiro",
    "salvador",
    "sao_luis",
    "sao_paulo",
    "teresina",
    "vitoria",
)


class CestaBasica(Adapter):
    """Adapter for DIEESE's basic shopping basket (cesta básica) price index.
    If no `city` variable is created, it averages the value of all available
    cities in any given date (this is used in subclasses)."""

    file_type = "html"
    url = "https://www.dieese.org.br/cesta/produto"

    POST_DATA = {
        "farinha": "false",
        "produtos": "1",
        "tipoDado": "5",
        "cidades": "0",
        "dataInicial": "071994",  # before that we need currency convertion
        "dataFinal": date.today().strftime("%m%Y"),
    }
    IMPORT_KWARGS = {
        "force_types": {k: TextField for k in chain(("field_0",), ALL_CITIES)}
    }

    @staticmethod
    def post_processing(body: bytes) -> bytes:
        """Fixes broken HTML syntax in the source file."""
        body = body.strip()
        xml = b'<?xml version="1.0" encoding="UTF-8" ?>'
        if body.startswith(xml):
            body = body.replace(xml, b"", 1)
        return body.strip()

    def mean(self, row: NamedTuple) -> Optional[Decimal]:
        cities = getattr(self, "cities", ALL_CITIES)
        raw = (getattr(row, city, None) for city in cities)
        strings = (value.strip() for value in raw if isinstance(value, str))
        cleaned = (value for value in strings if value and value != "-")
        values = tuple(Decimal(value.replace(",", ".")) for value in cleaned)

        if not values:
            return None

        if len(values) == 1:
            return values[0]

        return mean(values)

    def serialize(self, row: NamedTuple) -> MaybeIndexesGenerator:
        """serialize method to unpack rows's row into a tuple."""
        value = self.mean(row)
        if value is None:
            yield None
            return

        # the index has the price, let's calculate the percentage
        self.first_value = getattr(self, "first_value", value)
        adjusted_value = value / self.first_value

        reference = datetime.strptime(row[0][:7], "%m-%Y").date()
        yield reference, adjusted_value


# regional adapters


class CestaBasicaCentroOeste(CestaBasica):
    cities = (
        "brasilia",
        "cuiaba",
        "campo_grande",
        "goiania",
    )


class CestaBasicaNordeste(CestaBasica):
    cities = (
        "aracaju",
        "fortaleza",
        "joao_pessoa",
        "maceio",
        "natal",
        "recife",
        "salvador",
        "sao_luis",
        "teresina",
    )


class CestaBasicaNorte(CestaBasica):
    cities = (
        "belem",
        "boa_vista",
        "macapa",
        "manaus",
        "palmas",
        "porto_velho",
        "rio_branco",
    )


class CestaBasicaSudeste(CestaBasica):
    cities = (
        "belo_horizonte",
        "rio_de_janeiro",
        "sao_paulo",
        "vitoria",
    )


class CestaBasicaSul(CestaBasica):
    cities = (
        "curitiba",
        "florianopolis",
        "porto_alegre",
    )


# city adapters


class CestaBasicaAracaju(CestaBasica):
    cities = ("aracaju",)


class CestaBasicaBelem(CestaBasica):
    cities = ("belem",)


class CestaBasicaBeloHorizonte(CestaBasica):
    cities = ("belo_horizonte",)


class CestaBasicaBoaVista(CestaBasica):
    cities = ("boa_vista",)


class CestaBasicaBrasilia(CestaBasica):
    cities = ("brasilia",)


class CestaBasicaCampoGrande(CestaBasica):
    cities = ("campo_grande",)


class CestaBasicaCuiaba(CestaBasica):
    cities = ("cuiaba",)


class CestaBasicaCuritiba(CestaBasica):
    cities = ("curitiba",)


class CestaBasicaFlorianopolis(CestaBasica):
    cities = ("florianopolis",)


class CestaBasicaFortaleza(CestaBasica):
    cities = ("fortaleza",)


class CestaBasicaGoiania(CestaBasica):
    cities = ("goiania",)


class CestaBasicaJoaoPessoa(CestaBasica):
    cities = ("joao_pessoa",)


class CestaBasicaMacae(CestaBasica):
    cities = ("macae",)


class CestaBasicaMacapa(CestaBasica):
    cities = ("macapa",)


class CestaBasicaMaceio(CestaBasica):
    cities = ("maceio",)


class CestaBasicaManaus(CestaBasica):
    cities = ("manaus",)


class CestaBasicaNatal(CestaBasica):
    cities = ("natal",)


class CestaBasicaPalmas(CestaBasica):
    cities = ("palmas",)


class CestaBasicaPortoAlegre(CestaBasica):
    cities = ("porto_alegre",)


class CestaBasicaPortoVelho(CestaBasica):
    cities = ("porto_velho",)


class CestaBasicaRecife(CestaBasica):
    cities = ("recife",)


class CestaBasicaRioBranco(CestaBasica):
    cities = ("rio_branco",)


class CestaBasicaRioDeJaneiro(CestaBasica):
    cities = ("rio_de_janeiro",)


class CestaBasicaSalvador(CestaBasica):
    cities = ("salvador",)


class CestaBasicaSaoLuis(CestaBasica):
    cities = ("sao_luis",)


class CestaBasicaSaoPaulo(CestaBasica):
    cities = ("sao_paulo",)


class CestaBasicaTeresina(CestaBasica):
    cities = ("teresina",)


class CestaBasicaVitoria(CestaBasica):
    cities = ("vitoria",)
