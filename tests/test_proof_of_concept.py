from datetime import date
from unittest.mock import patch

import asynctest
import pytest
from aiohttp import ClientSession

from calculadora_do_cidadao import (
    BaseDaCalculadoraDoCidadão,
    CalculadoraDoCidadão,
    CalculadoraDoCidadãoAsyncio,
)


HTML = """
    <tr>
        <td class="fundoPadraoAClaro3">Data inicial</td>
        <td class="fundoPadraoAClaro3 ">07/2019</td>
    </tr>
"""
HTML_PARSEADO = {"Data inicial": date(2019, 7, 1)}


def test_preparar_data():
    assert BaseDaCalculadoraDoCidadão.preparar_data(date(2019, 12, 31)) == "12/2019"
    with patch("calculadora_do_cidadao.date") as mock_date:
        mock_date.today.return_value = date(2020, 1, 1)
        assert BaseDaCalculadoraDoCidadão.preparar_data() == "01/2020"


def test_limpar_chave():
    chave = " Índice de \n\t\tcorreção no   período\n\n"
    esperado = "Índice de correção no período"
    assert BaseDaCalculadoraDoCidadão.limpar_chave(chave) == esperado


@pytest.mark.parametrize(
    "valor, esperado",
    (
        ("12/2019", date(2019, 12, 1)),
        ("R$        1,00        ( REAL )", 1.0),
        ("1,02801170", 1.02801170),
        ("2,801170 %", None),
    ),
)
def test_limpar_valor(valor, esperado):
    assert BaseDaCalculadoraDoCidadão.limpar_valor(valor) == esperado


def test_parser():
    base = BaseDaCalculadoraDoCidadão()
    assert base.parser(HTML) == HTML_PARSEADO


def test_dados_da_requisição():
    base = BaseDaCalculadoraDoCidadão()
    args = (42.0, date(1983, 2, 8), date(2019, 12, 31))
    assert base.dados_para_requisição(*args) == {
        "dataInicial": "02/1983",
        "dataFinal": "12/2019",
        "valorCorrecao": "42,00",
        "aba": "1",
        "selIndice": base.ÍNDICE_PADRÃO,
        "idIndice": "",
        "nomeIndicePeriodo": "",
    }


def test_uso_síncrono():
    calculadora = CalculadoraDoCidadão()
    hoje = date.today()

    with patch("calculadora_do_cidadao.post") as post:
        post.return_value.text = HTML
        assert calculadora(42.0, hoje) == HTML_PARSEADO

        post.assert_called_once_with(
            calculadora.URL_DO_FORMULÁRIO,
            data=calculadora.dados_para_requisição(42.0, hoje, None),
            verify=calculadora.verificar_ssl,
        )


@pytest.mark.asyncio
async def test_uso_assíncrono():
    calculadora = CalculadoraDoCidadãoAsyncio()
    hoje = date.today()

    with asynctest.patch.object(ClientSession, "post") as post:
        post.return_value.__aenter__.return_value.text = asynctest.CoroutineMock(
            return_value=HTML
        )

        async with ClientSession() as sessão:
            assert await calculadora(sessão, 42.0, hoje) == HTML_PARSEADO

        post.assert_called_once_with(
            calculadora.URL_DO_FORMULÁRIO,
            data=calculadora.dados_para_requisição(42.0, hoje, None),
            ssl=calculadora.verificar_ssl,
        )
