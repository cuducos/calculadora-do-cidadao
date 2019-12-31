from datetime import date
from re import sub

from bs4 import BeautifulSoup

from requests import post


class BaseDaCalculadoraDoCidadão:

    URL_DO_FORMULÁRIO = (
        "https://www3.bcb.gov.br/"
        "CALCIDADAO/publico/corrigirPorIndice.do?method=corrigirPorIndice"
    )

    ÍNDICES = {
        "00189IGP-M": "IGP-M (FGV) - a partir de 06/1989",
        "00190IGP-DI": "IGP-DI (FGV) - a partir de 02/1944",
        "00188INPC": "INPC (IBGE) - a partir de 04/1979",
        "00433IPCA": "IPCA (IBGE) - a partir de 01/1980",
        "10764IPC-E": "IPCA-E (IBGE) - a partir de 01/1992",
        "00191IPC-BRASIL": "IPC-BRASIL (FGV) - a partir de 01/1990",
        "00193IPC-SP": "IPC-SP (FIPE) - a partir de 11/1942",
    }
    ÍNDICE_PADRÃO = "00189IGP-M"

    def __init__(self, índice=None, verificar_ssl=True):
        self.verificar_ssl = verificar_ssl
        self.dados_do_formulário = {
            "aba": "1",
            "selIndice": self.ÍNDICE_PADRÃO,
            "idIndice": "",
            "nomeIndicePeriodo": "",
        }

    @staticmethod
    def preparar_data(data=None):
        data = data or date.today()
        return f"{data.month:0>2d}/{data.year}"

    @staticmethod
    def limpar_chave(texto):
        texto = sub(r"\s+", " ", texto)
        return texto

    @staticmethod
    def limpar_valor(texto):
        texto = sub(r"[^\d,/%]", "", texto)

        if "%" in texto:
            return

        if "," in texto:
            texto = texto.replace(",", ".")
            return float(texto)

        if "/" in texto:
            mês, ano = texto.split("/")
            return date(int(ano), int(mês), 1)

        return texto

    def parser(self, html):
        html = BeautifulSoup(html, "html.parser")
        nós = html.find_all("td", class_="fundoPadraoAClaro3")
        textos = tuple(nó.text for nó in nós)
        dados = {
            self.limpar_chave(chave): self.limpar_valor(valor)
            for chave, valor in zip(textos[::2], textos[1::2])
        }
        return {chave: valor for chave, valor in dados.items() if valor}

    def dados_para_requisição(self, valor, data_original, data_final):
        if not data_final or isinstance(data_final, date):
            data_final = self.preparar_data(data_final)

        if isinstance(data_original, date):
            data_original = self.preparar_data(data_original)

        valor = valor if isinstance(valor, float) else float(valor)
        valor = str(valor).replace(".", ",")

        dados = self.dados_do_formulário.copy()
        dados.update(
            {
                "dataInicial": data_original,
                "dataFinal": data_final,
                "valorCorrecao": valor,
            }
        )
        return dados


class CalculadoraDoCidadão(BaseDaCalculadoraDoCidadão):
    def __call__(self, valor, data_original, data_final=None):
        resposta = post(
            self.URL_DO_FORMULÁRIO,
            data=self.dados_para_requisição(valor, data_original, data_final),
            verify=self.verificar_ssl,
        )
        return self.parser(resposta.text)


class CalculadoraDoCidadãoAsyncio(BaseDaCalculadoraDoCidadão):
    async def __call__(self, sessão, valor, data_original, data_final=None):
        kwargs = {
            "data": self.dados_para_requisição(valor, data_original, data_final),
            "ssl": self.verificar_ssl,
        }

        async with sessão.post(self.URL_DO_FORMULÁRIO, **kwargs) as resposta:
            return self.parser(await resposta.text())
