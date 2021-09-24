from pytest import raises

from calculadora_do_cidadao.download import Download, DownloadMethodNotImplementedError


def test_unzip(zip_file):
    assert Download.unzip(zip_file).read_bytes() == b"42"


def test_http_get(mocker):
    session = mocker.patch("calculadora_do_cidadao.download.Session")
    session.return_value.get.return_value.content = b"42"
    jar = mocker.patch("calculadora_do_cidadao.download.cookiejar_from_dict")
    jar.return_value = "my-cookie-jar"
    path = mocker.MagicMock()

    download = Download("https://here.comes/a/fancy.url", cookies={"test": 42})
    download.http(path)

    jar.assert_called_once_with({"test": 42})
    assert session.return_value.cookies == "my-cookie-jar"

    session.assert_called_once_with()
    session.return_value.get.assert_called_once_with("https://here.comes/a/fancy.url")
    path.write_bytes.assert_called_once_with(b"42")


def test_http_post(mocker):
    session = mocker.patch("calculadora_do_cidadao.download.Session")
    session.return_value.post.return_value.content = b"42"
    path = mocker.MagicMock()

    download = Download("https://here.comes/a/fancy.url", post_data={"test": 42})
    download.http(path)

    session.assert_called_once_with()
    session.return_value.post.assert_called_once_with(
        "https://here.comes/a/fancy.url", data={"test": 42}
    )
    path.write_bytes.assert_called_once_with(b"42")


def test_download(zip_file, mocker):
    mocker.patch.object(Download, "http", return_value=zip_file)
    download = Download("http://here.comes/a/fancy/url.zip", should_unzip=True)
    with download() as path:
        download.http.assert_called_once()
        assert path.read_bytes() == b"42"


def test_download_not_implemented():
    expected = r"No method implemented for tcp\."  # this is a regex
    with raises(DownloadMethodNotImplementedError, match=expected):
        Download("tcp://here.comes/a/fancy/url.zip")


def test_post_procesing(mocker, broken_table):
    mocker.patch.object(Download, "http", return_value=broken_table)
    download = Download(
        "http://here.comes/a/fancy/url.zip", post_processing=lambda b: b"<table>" + b
    )
    with download() as path:
        download.http.assert_called_once()
        assert path.read_text().startswith("<table>")
        assert path.read_text().endswith("</table>\n")
