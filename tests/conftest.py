from pathlib import Path
from tempfile import NamedTemporaryFile, TemporaryDirectory
from zipfile import ZipFile

from pytest import fixture

from tests import get_fixture


@fixture
def broken_table():
    """This fixtures provide a copy of the broken table file because post
    processing it (to fix the borken table) overwrites the orignal file."""
    with NamedTemporaryFile() as _tmp:
        tmp = Path(_tmp.name)
        tmp.write_bytes(get_fixture("broken-table").read_bytes())
        yield tmp


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
