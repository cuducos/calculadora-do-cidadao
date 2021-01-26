from datetime import date
from decimal import Decimal
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

from calculadora_do_cidadao.adapters import Adapter, AdapterNoImportMethod
from tests import get_fixture


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


class PostAdapter(GoodAdapter):
    POST_DATA = {"test": 42}


class ProcessingAdapter(GoodAdapter):
    @staticmethod
    def post_processing(body: bytes) -> bytes:
        return b"<table>" + body


def test_file_types():
    msg = r"Invalid file type dummy\. Valid file types are: html, xls\."
    with pytest.raises(AdapterNoImportMethod, match=msg):
        DummyAdapter()


def test_export_index(mocker):
    download = mocker.patch.object(GoodAdapter, "download")
    download.return_value = (
        (date(2014, 7, 8), Decimal("7.1")),
        (date(1998, 7, 12), Decimal("3.0")),
    )
    adapter = GoodAdapter()

    assert adapter.export_index(date(2014, 7, 8)) == {
        "date": date(2014, 7, 8),
        "value": Decimal("7.1"),
    }
    assert adapter.export_index(date(2014, 7, 8), include_name=True) == {
        "date": date(2014, 7, 8),
        "value": Decimal("7.1"),
        "serie": "goodadapter",
    }


def test_export(mocker):
    download = mocker.patch.object(GoodAdapter, "download")
    download.return_value = (
        (date(2014, 7, 8), Decimal("7.1")),
        (date(1998, 7, 12), Decimal("3.0")),
    )
    adapter = GoodAdapter()
    assert tuple(adapter.export()) == (
        {"date": date(1998, 7, 12), "value": Decimal("3.0")},
        {"date": date(2014, 7, 8), "value": Decimal("7.1")},
    )
    assert tuple(adapter.export(include_name=True)) == (
        {"date": date(1998, 7, 12), "value": Decimal("3.0"), "serie": "goodadapter"},
        {"date": date(2014, 7, 8), "value": Decimal("7.1"), "serie": "goodadapter"},
    )


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
    all_data = get_fixture("calculadora-do-cidadao")

    adapter1 = GoodAdapter(exported)
    assert adapter1.data == {
        date(2014, 7, 8): Decimal("7.1"),
        date(1998, 7, 12): Decimal("3.0"),
    }

    adapter2 = GoodAdapter(all_data)
    assert adapter2.data == {date(1998, 7, 12): Decimal("3.0")}


def test_download_does_not_receive_post_data(mocker):
    download = mocker.patch("calculadora_do_cidadao.adapters.Download")
    import_from_html = mocker.patch("calculadora_do_cidadao.adapters.import_from_html")
    import_from_html.return_value = tuple()
    GoodAdapter()
    download.assert_called_once_with(
        url="https://here.comes/a/fancy.url",
        should_unzip=False,
        cookies={},
        post_data=None,
        post_processing=None,
    )


def test_download_receives_post_data(mocker):
    download = mocker.patch("calculadora_do_cidadao.adapters.Download")
    import_from_html = mocker.patch("calculadora_do_cidadao.adapters.import_from_html")
    import_from_html.return_value = tuple()
    PostAdapter()
    download.assert_called_once_with(
        url="https://here.comes/a/fancy.url",
        should_unzip=False,
        cookies={},
        post_data={"test": 42},
        post_processing=None,
    )


def test_post_processing(mocker):
    download = mocker.patch("calculadora_do_cidadao.adapters.Download")
    import_from_html = mocker.patch("calculadora_do_cidadao.adapters.import_from_html")
    import_from_html.return_value = tuple()
    adapter = ProcessingAdapter()
    download.assert_called_once_with(
        url="https://here.comes/a/fancy.url",
        should_unzip=False,
        cookies={},
        post_data=None,
        post_processing=adapter.post_processing,
    )
