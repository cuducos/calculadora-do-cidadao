from pathlib import Path
from inspect import isclass
from typing import Iterator

from rows import export_to_csv, import_from_dicts

import calculadora_do_cidadao
from calculadora_do_cidadao.adapters import Adapter


def data() -> Iterator[dict]:
    """Iterate over every adapter available, yielding their data row by row as
    a dictionary, ready for `rows.import_from_dict`."""
    for _obj in dir(calculadora_do_cidadao):
        obj = getattr(calculadora_do_cidadao, _obj)
        if not isclass(obj) or not issubclass(obj, Adapter):  # discard non-adapters
            continue

        adapter = obj()
        for key in sorted(adapter.data):
            yield {
                "date": key,
                "value": adapter.data[key],
                "serie": obj.__name__.lower(),
            }


def main(path: Path) -> None:
    """Export all data to CSV."""
    table = import_from_dicts(data())
    export_to_csv(table, path)


if __name__ == "__main__":
    path = Path("calculadora-do-cidadao.csv")
    main(path)
