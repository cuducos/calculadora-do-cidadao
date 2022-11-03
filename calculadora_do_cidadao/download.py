from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Callable, Iterable, Iterator, Optional, Union
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

    Cookies  and headers are just relevant if the URL uses HTTP (and, surely
    both are optional).

    The `post_data` dictionary is used to send an HTTP POST request (instead of
    the default GET). If this field is a sequence of dictionaries, it will
    result in one request per dictionary.

    The `post_processing` as a bytes to bytes function that is able to edit the
    contents before saving it locally, allowing adapter to fix malformed
    documents."""

    url: str
    should_unzip: bool = False
    headers: Optional[dict] = None
    cookies: Optional[dict] = None
    post_data: Optional[Union[dict, Iterable[dict]]] = None
    post_processing: Optional[Callable[[bytes], bytes]] = None

    def __post_init__(self) -> None:
        """The initialization of this class defines the proper method to be
        called for download based on the protocol of the URL."""
        self.parsed_url: ParseResult = urlparse(self.url)
        self.file_name: str = Path(self.parsed_url.path).name
        self.https = self.http  # maps HTTPS requests to HTTP method

        try:
            self.download = getattr(self, self.parsed_url.scheme)
        except AttributeError:
            error = f"No method implemented for {self.parsed_url.scheme}."
            raise DownloadMethodNotImplementedError(error)

    @staticmethod
    def unzip(path: Path, target: Path) -> Path:
        """Unzips the first file of an archive and returns its path."""
        with ZipFile(path) as archive:
            first_file, *_ = archive.namelist()
            target.write_bytes(archive.read(first_file))

        return target

    def http(self) -> Iterable[bytes]:
        """Download the source file(s) using HTTP."""
        session = Session()

        if self.cookies:
            session.cookies = cookiejar_from_dict(self.cookies)

        if isinstance(self.post_data, dict):
            self.post_data = (self.post_data,)

        def request_generator(method, kwargs=None):
            if kwargs is None:
                kwargs = ({},)

            for kw in kwargs:
                kw["url"] = self.url
                if self.headers:
                    kw["headers"] = self.headers

                yield method(**kw)

        if self.post_data:
            send_as_json = False
            if self.headers:
                send_as_json = any("json" in v.lower() for v in self.headers.values())

            data_key = "json" if send_as_json else "data"
            params = ({data_key: data} for data in self.post_data)
            responses = request_generator(session.post, params)
        else:
            responses = request_generator(session.get)

        yield from (response.content for response in responses)

    @contextmanager
    def __call__(self) -> Iterator[Callable[[], Iterable[Path]]]:
        """Downloads the source file to a temporary directory and yields a
        generator of `pathlib.Path` with the path for the proper data file
        (which can be the downloaded file or the file unarchived from the
        downloaded one)."""

        def generator() -> Iterable[Path]:
            for contents in self.download():
                with NamedTemporaryFile() as tmp:
                    path = Path(tmp.name)
                    path.write_bytes(contents)

                    with NamedTemporaryFile() as _unzipped:
                        unzipped = Path(_unzipped.name)
                        if self.should_unzip:
                            path = self.unzip(path, unzipped)

                        if self.post_processing:
                            path.write_bytes(self.post_processing(path.read_bytes()))

                        yield path

        yield generator
