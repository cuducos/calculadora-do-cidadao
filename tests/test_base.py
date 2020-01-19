import pytest

from calculadora_do_cidadao.base import Adapter, AdapterNoImportMethod


class DummyAdapter(Adapter):
    url = "https://here.comes/a/fancy.url"
    file_type = "dummy"

    def serialize(self, row):
        yield row


def test_file_types():
    msg = r"Invalid file type dummy\. Valid file types are: html, xls\."
    with pytest.raises(AdapterNoImportMethod, match=msg):
        DummyAdapter()
