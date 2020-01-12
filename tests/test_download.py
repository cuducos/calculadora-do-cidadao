from pytest import raises

from calculadora_do_cidadao.download import Download, DownloadMethodNotImplementedError


def test_unzip(zip_file):
    assert Download.unzip(zip_file).read_bytes() == b"42"


def test_ftp(mocker):
    ftp = mocker.patch("calculadora_do_cidadao.download.FTP")
    path = mocker.MagicMock()

    download = Download("ftp://here.comes/a/fancy/url")
    download.ftp(path)

    ftp.assert_called_once_with("here.comes")
    ftp.return_value.__enter__.return_value.login.assert_called_once_with()
    ftp.return_value.__enter__.return_value.retrbinary.assert_called_once_with(
        "RETR /a/fancy/url", path.open.return_value.__enter__.return_value.write
    )


def test_download(zip_file, mocker):
    mocker.patch.object(Download, "ftp", return_value=zip_file)
    download = Download("ftp://here.comes/a/fancy/url.zip")
    with download() as path:
        download.ftp.assert_called_once()
        assert path.read_bytes() == b"42"


def test_download_not_implemented():
    expected = r"No method implemented for https\."  # this is a regex
    with raises(DownloadMethodNotImplementedError, match=expected):
        Download("https://here.comes/a/fancy/url.zip")
