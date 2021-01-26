from contextlib import contextmanager
from dataclasses import dataclass
from ftplib import FTP
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Callable, Iterator, Optional
from urllib.parse import ParseResult, urlparse
from zipfile import ZipFile

from requests import Session
from requests.utils import cookiejar_from_dict


class DownloadMethodNotImplementedError(Exception):
    """To be used when the `Download` class does not have a method implemented
    to download a file using the protocol specified in the `url` argument."""

    pass


@dataclass
class Download:
    """Abstraction for the download of data from the source.

    It can be initialized informing that the resulting file is a Zip archive
    that should be unarchived.

    Cookies are just relevant if the URL uses HTTP (and, surely cookies are
    optional).

    The `post_data` dictionary is used to send an HTTP POST request (instead of
    the default GET).

    The `post_processing` as a bytes to bytes function that is able to edit the
    contents before saving it locally, allowing adapter to fix malformed
    documents."""

    url: str
    should_unzip: bool = False
    cookies: Optional[dict] = None
    post_data: Optional[dict] = None
    post_processing: Optional[Callable[[bytes], bytes]] = None

    def __post_init__(self) -> None:
        """The initialization of this class defines the proper method to be
        called for download based on the protocol of the URL."""
        self.parsed_url: ParseResult = urlparse(self.url)
        self.file_name: str = Path(self.parsed_url.path).name
        self.https = self.http  # maps HTTPS requests to HTTP method

        try:
            self.download_to = getattr(self, self.parsed_url.scheme)
        except AttributeError:
            error = f"No method implemented for {self.parsed_url.scheme}."
            raise DownloadMethodNotImplementedError(error)

    @staticmethod
    def unzip(path: Path) -> Path:
        """Unzips the first file of an archive and returns its path."""
        with ZipFile(path) as archive:
            first_file, *_ = archive.namelist()
            target = path.parent / first_file
            target.write_bytes(archive.read(first_file))

        return target

    def http(self, path: Path) -> Path:
        """Download the source file using HTTP."""
        session = Session()

        if self.cookies:
            session.cookies = cookiejar_from_dict(self.cookies)

        if self.post_data:
            response = session.post(self.url, data=self.post_data)
        else:
            response = session.get(self.url)

        path.write_bytes(response.content)
        return path

    def ftp(self, path: Path) -> Path:
        """Download the source file using FTP."""
        with FTP(self.parsed_url.netloc) as conn:
            conn.login()
            with path.open("wb") as fobj:
                conn.retrbinary(f"RETR {self.parsed_url.path}", fobj.write)
        return path

    @contextmanager
    def __call__(self) -> Iterator[Path]:
        """Downloads the source file to a temporary directory and yields a
        `pathlib.Path` with the path for the proper data file (which can be the
        downloaded file or the file unarchived from the downloaded one)."""
        with TemporaryDirectory() as tmp:
            path = self.download_to(Path(tmp) / self.file_name)
            if self.should_unzip:
                path = self.unzip(path)

            if self.post_processing:
                path.write_bytes(self.post_processing(path.read_bytes()))

            yield path
