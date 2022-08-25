from calculadora_do_cidadao.adapters import cpi, dieese, ibge, igpm, selic


class PandasWrapper:
    def __init__(self, adapter):
        self.adapter = adapter()

    def adjust(self, original_date, value=None, target_date=None):
        # TODO: check if Pandas has a decimal/precision type
        return original_date.apply(self.adapter.adjust)

    @classmethod
    def wrap(cls, adapter):
        """This assures that the adapter downloads the data only when
        `PandasWrapper` is instantiated (as it works for regular adapters)."""

        def wrapper():
            return cls(adapter)

        return wrapper


AllUrbanCityAverage = PandasWrapper.wrap(cpi.AllUrbanCityAverage)
CestaBasicaAracaju = PandasWrapper.wrap(dieese.CestaBasicaAracaju)
CestaBasicaBelem = PandasWrapper.wrap(dieese.CestaBasicaBelem)
CestaBasicaBeloHorizonte = PandasWrapper.wrap(dieese.CestaBasicaBeloHorizonte)
CestaBasicaBoaVista = PandasWrapper.wrap(dieese.CestaBasicaBoaVista)
CestaBasicaBrasilia = PandasWrapper.wrap(dieese.CestaBasicaBrasilia)
CestaBasicaCampoGrande = PandasWrapper.wrap(dieese.CestaBasicaCampoGrande)
CestaBasicaCentroOeste = PandasWrapper.wrap(dieese.CestaBasicaCentroOeste)
CestaBasicaCuiaba = PandasWrapper.wrap(dieese.CestaBasicaCuiaba)
CestaBasicaCuritiba = PandasWrapper.wrap(dieese.CestaBasicaCuritiba)
CestaBasicaFlorianopolis = PandasWrapper.wrap(dieese.CestaBasicaFlorianopolis)
CestaBasicaFortaleza = PandasWrapper.wrap(dieese.CestaBasicaFortaleza)
CestaBasicaGoiania = PandasWrapper.wrap(dieese.CestaBasicaGoiania)
CestaBasicaJoaoPessoa = PandasWrapper.wrap(dieese.CestaBasicaJoaoPessoa)
CestaBasicaMacae = PandasWrapper.wrap(dieese.CestaBasicaMacae)
CestaBasicaMacapa = PandasWrapper.wrap(dieese.CestaBasicaMacapa)
CestaBasicaMaceio = PandasWrapper.wrap(dieese.CestaBasicaMaceio)
CestaBasicaManaus = PandasWrapper.wrap(dieese.CestaBasicaManaus)
CestaBasicaNatal = PandasWrapper.wrap(dieese.CestaBasicaNatal)
CestaBasicaNordeste = PandasWrapper.wrap(dieese.CestaBasicaNordeste)
CestaBasicaNorte = PandasWrapper.wrap(dieese.CestaBasicaNorte)
CestaBasicaPalmas = PandasWrapper.wrap(dieese.CestaBasicaPalmas)
CestaBasicaPortoAlegre = PandasWrapper.wrap(dieese.CestaBasicaPortoAlegre)
CestaBasicaPortoVelho = PandasWrapper.wrap(dieese.CestaBasicaPortoVelho)
CestaBasicaRecife = PandasWrapper.wrap(dieese.CestaBasicaRecife)
CestaBasicaRioBranco = PandasWrapper.wrap(dieese.CestaBasicaRioBranco)
CestaBasicaRioDeJaneiro = PandasWrapper.wrap(dieese.CestaBasicaRioDeJaneiro)
CestaBasicaSalvador = PandasWrapper.wrap(dieese.CestaBasicaSalvador)
CestaBasicaSaoLuis = PandasWrapper.wrap(dieese.CestaBasicaSaoLuis)
CestaBasicaSaoPaulo = PandasWrapper.wrap(dieese.CestaBasicaSaoPaulo)
CestaBasicaSudeste = PandasWrapper.wrap(dieese.CestaBasicaSudeste)
CestaBasicaSul = PandasWrapper.wrap(dieese.CestaBasicaSul)
CestaBasicaTeresina = PandasWrapper.wrap(dieese.CestaBasicaTeresina)
CestaBasicaVitoria = PandasWrapper.wrap(dieese.CestaBasicaVitoria)
Igpm = PandasWrapper.wrap(igpm.Igpm)
Inpc = PandasWrapper.wrap(ibge.Inpc)
Ipca = PandasWrapper.wrap(ibge.Ipca)
Ipca15 = PandasWrapper.wrap(ibge.Ipca15)
IpcaE = PandasWrapper.wrap(ibge.IpcaE)
Selic = PandasWrapper.wrap(selic.Selic)
