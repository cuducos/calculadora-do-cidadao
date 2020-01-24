from calculadora_do_cidadao.adapters.ibge import IbgeAdapter


class Ipca(IbgeAdapter):
    url = "ftp://ftp.ibge.gov.br/Precos_Indices_de_Precos_ao_Consumidor/IPCA/Serie_Historica/ipca_SerieHist.zip"
