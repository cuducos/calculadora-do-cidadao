from pathlib import Path


def get_fixture(adapter):
    name = adapter if isinstance(adapter, str) else adapter.__name__.lower()
    if name.startswith("cestabasica"):  # DIEESE adapters use the same fixture
        name = "cestabasica"
    directory = Path(__file__).parent / "fixtures"
    fixture, *_ = directory.glob(f"{name}.*")
    return fixture
