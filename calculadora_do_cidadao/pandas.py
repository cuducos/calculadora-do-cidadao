from calculadora_do_cidadao.adapters import ibge


class PandasWrapper:
    def __init__(self, adapter):
        self.adapter = adapter()
        adapter.adjust = self.adjust

    def adjust(self, original_date, value=None, target_date=None):
        raise NotImplementedError

    @classmethod
    def wrap(cls, adapter):
        def wrapper():
            return cls(adapter)

        return wrapper


# TODO: do this for all adapters
Ipca = PandasWrapper.wrap(ibge.Ipca)
Inpc = PandasWrapper.wrap(ibge.Inpc)
Ipca15 = PandasWrapper.wrap(ibge.Ipca15)
IpcaE = PandasWrapper.wrap(ibge.IpcaE)
