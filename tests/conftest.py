from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile

from pytest import fixture


@fixture(scope="session")
def zip_file():
    """Returns a path to a temporary zip file. Its content is a single file.
    The contents of this single file is `42` in bytes."""
    with TemporaryDirectory() as _tmp:
        tmp = Path(_tmp)
        fixture = tmp / "fixture"
        fixture.write_bytes(b"42")

        path = Path(tmp) / "fixture.zip"
        with ZipFile(path, "w") as archive:
            archive.write(fixture, arcname=fixture.name)

        yield path
