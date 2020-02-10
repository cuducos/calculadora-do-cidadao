from datetime import date
from decimal import Decimal
from pathlib import Path
from tempfile import TemporaryDirectory

from calculadora_do_cidadao import (
    AllUrbanCityAverage,
    Igpm,
    Inpc,
    Ipca,
    Ipca15,
    IpcaE,
    Selic,
)
from calculadora_do_cidadao.__main__ import data, export, get_adapters


ADAPTERS = (AllUrbanCityAverage, Igpm, Inpc, Ipca, Ipca15, IpcaE, Selic)


def test_get_adapters():
    assert set(get_adapters()) == set(ADAPTERS)


def test_data(mocker):
    for count, Adapter in enumerate(ADAPTERS, 1):
        download = mocker.patch.object(Adapter, "download")
        download.return_value = (
            (date(2019, 12, 1), Decimal(count)),
            (date(2020, 1, 1), Decimal(count * 1.5)),
        )

    result = tuple(data())
    assert len(result) == 2 * len(ADAPTERS)
    for dictionary in result:
        assert len(dictionary) == 3


def test_export(mocker):
    for count, Adapter in enumerate(ADAPTERS, 1):
        download = mocker.patch.object(Adapter, "download")
        download.return_value = (
            (date(2019, 12, 1), Decimal(count)),
            (date(2020, 1, 1), Decimal(count * 1.5)),
        )

    with TemporaryDirectory() as _tmp:
        path = Path(_tmp) / "calculadora-do-cidadao.csv"
        export(path)
        content = path.read_text()

    for Adapter in ADAPTERS:
        assert Adapter.__name__.lower() in content

    assert len(content.split()) == len(ADAPTERS * 2) + 1  # plus 1 for header
