from calculadora_do_cidadao.adapters.ibge import IbgeAdapter


class Ipca15(IbgeAdapter):
    url = "ftp://ftp.ibge.gov.br/Precos_Indices_de_Precos_ao_Consumidor/IPCA_15/Series_Historicas/ipca-15_SerieHist.zip"
