from pathlib import Path


def get_fixture(adapter):
    name = adapter if isinstance(adapter, str) else adapter.__name__.lower()
    directory = Path(__file__).parent / "fixtures"
    fixture, *_ = directory.glob(f"{name}.*")
    return fixture
