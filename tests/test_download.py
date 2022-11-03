from pathlib import Path
from tempfile import NamedTemporaryFile

from pytest import raises

from calculadora_do_cidadao.download import Download, DownloadMethodNotImplementedError


def test_unzip(zip_file):
    with NamedTemporaryFile() as tmp:
        assert Download.unzip(zip_file, Path(tmp.name)).read_bytes() == b"42"


def test_http_get(mocker):
    session = mocker.patch("calculadora_do_cidadao.download.Session")
    session.return_value.get.return_value.content = b"42"
    jar = mocker.patch("calculadora_do_cidadao.download.cookiejar_from_dict")
    jar.return_value = "my-cookie-jar"

    download = Download("https://here.comes/a/fancy.url", cookies={"test": 42})
    for contents in download.http():
        assert contents == b"42"

    jar.assert_called_once_with({"test": 42})
    assert session.return_value.cookies == "my-cookie-jar"

    session.assert_called_once_with()
    session.return_value.get.assert_called_once_with(
        url="https://here.comes/a/fancy.url"
    )


def test_http_get_zip_file(mocker, zip_file):
    session = mocker.patch("calculadora_do_cidadao.download.Session")
    session.return_value.get.return_value.content = zip_file.read_bytes()

    download = Download("https://here.comes/a/fancy.url", should_unzip=True)
    with download() as paths:
        for path in paths():
            assert path.read_bytes() == b"42"

    session.assert_called_once_with()
    session.return_value.get.assert_called_once_with(
        url="https://here.comes/a/fancy.url"
    )


def test_http_post(mocker):
    session = mocker.patch("calculadora_do_cidadao.download.Session")
    session.return_value.post.return_value.content = b"42"

    download = Download("https://here.comes/a/fancy.url", post_data={"test": 42})
    for contents in download.http():
        assert contents == b"42"

    session.assert_called_once_with()
    session.return_value.post.assert_called_once_with(
        url="https://here.comes/a/fancy.url", data={"test": 42}
    )


def test_multiple_http_post(mocker):
    session = mocker.patch("calculadora_do_cidadao.download.Session")
    session.return_value.post.return_value.content = b"42"

    download = Download(
        "https://here.comes/a/fancy.url", post_data=({"answer": 42}, {"test": 42})
    )
    for contents in download.http():
        assert contents == b"42"

    session.assert_called_once_with()
    session.return_value.post.assert_any_call(
        url="https://here.comes/a/fancy.url", data={"answer": 42}
    )
    session.return_value.post.assert_any_call(
        url="https://here.comes/a/fancy.url", data={"test": 42}
    )


def test_http_post_as_json(mocker):
    session = mocker.patch("calculadora_do_cidadao.download.Session")
    session.return_value.post.return_value.content = b"42"

    download = Download(
        "https://here.comes/a/fancy.url",
        post_data={"test": 42},
        headers={"Accept": "application/json"},
    )
    for contents in download.http():
        assert contents == b"42"

    session.assert_called_once_with()
    session.return_value.post.assert_called_once_with(
        url="https://here.comes/a/fancy.url",
        json={"test": 42},
        headers={"Accept": "application/json"},
    )


def test_download(mocker):
    mocker.patch.object(Download, "http", return_value=(b for b in (b"42",)))
    download = Download("http://here.comes/a/fancy/url.zip")
    with download() as paths:
        for path in paths():
            assert path.read_bytes() == b"42"
        download.http.assert_called_once_with()


def test_download_not_implemented():
    expected = r"No method implemented for tcp\."  # this is a regex
    with raises(DownloadMethodNotImplementedError, match=expected):
        Download("tcp://here.comes/a/fancy/url.zip")


def test_post_procesing(mocker, broken_table):
    mocker.patch.object(
        Download, "http", return_value=(b for b in (broken_table.read_bytes(),))
    )
    download = Download(
        "http://here.comes/a/fancy/url.zip", post_processing=lambda b: b"<table>" + b
    )
    with download() as paths:
        for path in paths():
            assert path.read_text().startswith("<table>")
            assert path.read_text().endswith("</table>\n")
        download.http.assert_called_once()
