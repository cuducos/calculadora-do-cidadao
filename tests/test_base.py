from datetime import date
from decimal import Decimal
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

from calculadora_do_cidadao.adapters import Adapter, AdapterNoImportMethod
from tests.test_adapters import get_fixture


class DummyAdapter(Adapter):
    url = "https://here.comes/a/fancy.url"
    file_type = "dummy"

    def serialize(self, row):
        yield row


class GoodAdapter(Adapter):
    url = "https://here.comes/a/fancy.url"
    file_type = "html"

    def serialize(self, row):
        yield row


def test_file_types():
    msg = r"Invalid file type dummy\. Valid file types are: html, xls\."
    with pytest.raises(AdapterNoImportMethod, match=msg):
        DummyAdapter()


def test_to_csv(mocker):
    download = mocker.patch.object(GoodAdapter, "download")
    download.return_value = (
        (date(2014, 7, 8), Decimal("7.1")),
        (date(1998, 7, 12), Decimal("3.0")),
    )
    adapter = GoodAdapter()

    with TemporaryDirectory() as _tmp:
        tmp = Path(_tmp) / "file"
        adapter.to_csv(tmp)
        assert tmp.read_text() == get_fixture(GoodAdapter).read_text()


def test_from_csv():
    exported = get_fixture(GoodAdapter)
    adapter = GoodAdapter(exported)
    assert adapter.data == {
        date(2014, 7, 8): Decimal("7.1"),
        date(1998, 7, 12): Decimal("3.0"),
    }
