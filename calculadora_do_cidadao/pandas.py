from decimal import Decimal

from pandas import Series

from calculadora_do_cidadao.adapters import ibge


class PandasWrapper:
    def __init__(self, adapter):
        self.adapter = adapter()

    def adjust(self, original_date, value=None, target_date=None):
        # TODO: check if Pandas has a decimal/precision type
        return original_date.apply(self.adapter.adjust)

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
