from calculadora_do_cidadao.adapters.ibge import IbgeAdapter


class Inpc(IbgeAdapter):
    url = "ftp://ftp.ibge.gov.br/Precos_Indices_de_Precos_ao_Consumidor/INPC/Serie_Historica/inpc_SerieHist.zip"
