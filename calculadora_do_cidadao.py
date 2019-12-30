from datetime import date
from re import sub

from bs4 import BeautifulSoup

from requests import post


class CalculadoraDoCidadão:

    URL_DO_FORMULÁRIO = (
        "https://www3.bcb.gov.br/"
        "CALCIDADAO/publico/corrigirPorIndice.do?method=corrigirPorIndice"
    )

    ÍNDICES = {
        "00189IGP-M": "gIGP-M (FGV) - a partir de 06/1989",
        "00190IGP-DI": "gIGP-DI (FGV) - a partir de 02/1944",
        "00188INPC": "gINPC (IBGE) - a partir de 04/1979",
        "00433IPCA": "gIPCA (IBGE) - a partir de 01/1980",
        "10764IPC-E": "gIPCA-E (IBGE) - a partir de 01/1992",
        "00191IPC-BRASIL": "gIPC-BRASIL (FGV) - a partir de 01/1990",
        "00193IPC-SP": "gIPC-SP (FIPE) - a partir de 11/1942",
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
        mês = str(data.month).zfill(2)
        return f"{mês}/{data.year}"

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

    def __call__(self, valor, data_original, data_final=None):
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

        resposta = post(self.URL_DO_FORMULÁRIO, data=dados, verify=self.verificar_ssl)
        return self.parser(resposta.text)
