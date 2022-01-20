from datetime import date, datetime
from decimal import Decimal
from itertools import chain
from statistics import mean
from typing import NamedTuple, Optional

from calculadora_do_cidadao.adapters import Adapter
from calculadora_do_cidadao.rows.fields import TextField
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
    If no `cities` variable is created, it averages the value of all available
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
        """Fixes broken HTML syntax in DIEESE's the source file."""
        body = body.strip()
        xml = b'<?xml version="1.0" encoding="UTF-8" ?>'
        if body.startswith(xml):
            body = body.replace(xml, b"", 1)
        return body.strip()

    def _mean(self, row: NamedTuple) -> Optional[Decimal]:
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
        """Serialize method to unpack rows's row into a tuple. Calculates the
        mean for adapters including different cities if needed."""
        value = self._mean(row)
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
    """Adapter for DIEESE's basic shopping basket (cesta básica) price index
    including Brasília, Cuiabá, Campo Grande and Goiânia."""

    cities = (
        "brasilia",
        "cuiaba",
        "campo_grande",
        "goiania",
    )


class CestaBasicaNordeste(CestaBasica):
    """Adapter for DIEESE's basic shopping basket (cesta básica) price index
    including Aracajú, Fortaleza, João Pessoa, Maceió, Natal, Recife, Salvador,
    São Luís and Teresina."""

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
    """Adapter for DIEESE's basic shopping basket (cesta básica) price index
    including Belém, Boa Vista, Macapá, Manaus, Palmas, Porto Velho and Rio
    Branco."""

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
    """Adapter for DIEESE's basic shopping basket (cesta básica) price index
    including Belo Horizonte, Rio de Janeiro, São Paulo and Vitória."""

    cities = (
        "belo_horizonte",
        "rio_de_janeiro",
        "sao_paulo",
        "vitoria",
    )


class CestaBasicaSul(CestaBasica):
    """Adapter for DIEESE's basic shopping basket (cesta básica) price index
    including Curitiba, Florianópolis and Porto Alegre."""

    cities = (
        "curitiba",
        "florianopolis",
        "porto_alegre",
    )


# city adapters


class CestaBasicaAracaju(CestaBasica):
    """Adapter for DIEESE's basic shopping basket (cesta básica) price index
    for Aracajú."""

    cities = ("aracaju",)


class CestaBasicaBelem(CestaBasica):
    """Adapter for DIEESE's basic shopping basket (cesta básica) price index
    for Belém."""

    cities = ("belem",)


class CestaBasicaBeloHorizonte(CestaBasica):
    """Adapter for DIEESE's basic shopping basket (cesta básica) price index
    for Belo Horizonte."""

    cities = ("belo_horizonte",)


class CestaBasicaBoaVista(CestaBasica):
    """Adapter for DIEESE's basic shopping basket (cesta básica) price index
    for Boa Vista."""

    cities = ("boa_vista",)


class CestaBasicaBrasilia(CestaBasica):
    """Adapter for DIEESE's basic shopping basket (cesta básica) price index
    for Brasília."""

    cities = ("brasilia",)


class CestaBasicaCampoGrande(CestaBasica):
    """Adapter for DIEESE's basic shopping basket (cesta básica) price index
    for Campo Grande."""

    cities = ("campo_grande",)


class CestaBasicaCuiaba(CestaBasica):
    """Adapter for DIEESE's basic shopping basket (cesta básica) price index
    for Cuiabá."""

    cities = ("cuiaba",)


class CestaBasicaCuritiba(CestaBasica):
    """Adapter for DIEESE's basic shopping basket (cesta básica) price index
    for Curitiba."""

    cities = ("curitiba",)


class CestaBasicaFlorianopolis(CestaBasica):
    """Adapter for DIEESE's basic shopping basket (cesta básica) price index
    for Florianópolis."""

    cities = ("florianopolis",)


class CestaBasicaFortaleza(CestaBasica):
    """Adapter for DIEESE's basic shopping basket (cesta básica) price index
    for Fortaleza."""

    cities = ("fortaleza",)


class CestaBasicaGoiania(CestaBasica):
    """Adapter for DIEESE's basic shopping basket (cesta básica) price index
    for Goiânia."""

    cities = ("goiania",)


class CestaBasicaJoaoPessoa(CestaBasica):
    """Adapter for DIEESE's basic shopping basket (cesta básica) price index
    for João Pessoa."""

    cities = ("joao_pessoa",)


class CestaBasicaMacae(CestaBasica):
    """Adapter for DIEESE's basic shopping basket (cesta básica) price index
    for Macaé."""

    cities = ("macae",)


class CestaBasicaMacapa(CestaBasica):
    """Adapter for DIEESE's basic shopping basket (cesta básica) price index
    for Macapá."""

    cities = ("macapa",)


class CestaBasicaMaceio(CestaBasica):
    """Adapter for DIEESE's basic shopping basket (cesta básica) price index
    for Maceió."""

    cities = ("maceio",)


class CestaBasicaManaus(CestaBasica):
    """Adapter for DIEESE's basic shopping basket (cesta básica) price index
    for Manaus."""

    cities = ("manaus",)


class CestaBasicaNatal(CestaBasica):
    """Adapter for DIEESE's basic shopping basket (cesta básica) price index
    for Natal."""

    cities = ("natal",)


class CestaBasicaPalmas(CestaBasica):
    """Adapter for DIEESE's basic shopping basket (cesta básica) price index
    for Palmas."""

    cities = ("palmas",)


class CestaBasicaPortoAlegre(CestaBasica):
    """Adapter for DIEESE's basic shopping basket (cesta básica) price index
    for Porto Alegre."""

    cities = ("porto_alegre",)


class CestaBasicaPortoVelho(CestaBasica):
    """Adapter for DIEESE's basic shopping basket (cesta básica) price index
    for Porto Velho."""

    cities = ("porto_velho",)


class CestaBasicaRecife(CestaBasica):
    """Adapter for DIEESE's basic shopping basket (cesta básica) price index
    for Recife."""

    cities = ("recife",)


class CestaBasicaRioBranco(CestaBasica):
    """Adapter for DIEESE's basic shopping basket (cesta básica) price index
    for Rio Branco."""

    cities = ("rio_branco",)


class CestaBasicaRioDeJaneiro(CestaBasica):
    """Adapter for DIEESE's basic shopping basket (cesta básica) price index
    for Rio de Janeiro."""

    cities = ("rio_de_janeiro",)


class CestaBasicaSalvador(CestaBasica):
    """Adapter for DIEESE's basic shopping basket (cesta básica) price index
    for Salvador."""

    cities = ("salvador",)


class CestaBasicaSaoLuis(CestaBasica):
    """Adapter for DIEESE's basic shopping basket (cesta básica) price index
    for São Luís."""

    cities = ("sao_luis",)


class CestaBasicaSaoPaulo(CestaBasica):
    """Adapter for DIEESE's basic shopping basket (cesta básica) price index
    for São Paulo."""

    cities = ("sao_paulo",)


class CestaBasicaTeresina(CestaBasica):
    """Adapter for DIEESE's basic shopping basket (cesta básica) price index
    for Teresina."""

    cities = ("teresina",)


class CestaBasicaVitoria(CestaBasica):
    """Adapter for DIEESE's basic shopping basket (cesta básica) price index
    for Vitória."""

    cities = ("vitoria",)
