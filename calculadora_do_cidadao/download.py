from contextlib import contextmanager
from dataclasses import dataclass
from ftplib import FTP
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Iterator
from zipfile import ZipFile
from urllib.parse import ParseResult, urlparse


class DownloadMethodNotImplementedError(Exception):
    pass


@dataclass
class Download:
    url: str

    def __post_init__(self) -> None:
        self.parsed_url: ParseResult = urlparse(self.url)
        self.file_name: str = Path(self.parsed_url.path).name

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

    def ftp(self, path: Path) -> Path:
        with FTP(self.parsed_url.netloc) as conn:
            conn.login()
            with path.open("wb") as fobj:
                conn.retrbinary(f"RETR {self.parsed_url.path}", fobj.write)
        return path

    @contextmanager
    def __call__(self) -> Iterator[Path]:
        with TemporaryDirectory() as tmp:
            path = self.download_to(Path(tmp) / self.file_name)
            yield self.unzip(path)
