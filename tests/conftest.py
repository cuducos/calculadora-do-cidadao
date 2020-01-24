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


def get_fixture(name):
    return Path(__file__).parent / "fixtures" / name


@fixture
def ipca_fixture():
    return get_fixture("ipca.xls")


@fixture
def selic_fixture():
    return get_fixture("selic.html")


@fixture
def ipca15_fixture():
    return get_fixture("ipca15.xls")


@fixture
def inpc_fixture():
    return get_fixture("inpc.xls")
