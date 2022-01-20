from pathlib import Path
from inspect import isclass
from typing import Iterable, Type

from typer import Typer, echo

import calculadora_do_cidadao
from calculadora_do_cidadao.adapters import Adapter
from calculadora_do_cidadao.rows.plugins.plugin_csv import export_to_csv
from calculadora_do_cidadao.rows.plugins.dicts import import_from_dicts


DEFAULT_EXPORT_FILE = Path("calculadora-do-cidadao.csv")
cli = Typer()


def get_adapters() -> Iterable[Type[Adapter]]:
    """Generator with all adapters available in this module."""
    for _obj in dir(calculadora_do_cidadao):
        obj = getattr(calculadora_do_cidadao, _obj)

        # discard non-adapters
        if isclass(obj) and issubclass(obj, Adapter):
            yield obj


def data() -> Iterable[dict]:
    """Generator to get all export data from adapters in this module."""
    adapters = tuple(get_adapters())
    total = len(adapters)
    for count, adapter in enumerate(adapters, 1):
        name = adapter.__name__.upper()
        echo(f"[{count} of {total}] Exporting {name} data…")
        yield from adapter().export(include_name=True)


@cli.command()
def export(path: Path = DEFAULT_EXPORT_FILE) -> None:
    """Export all data to CSV."""
    table = import_from_dicts(data())
    export_to_csv(table, path)


if __name__ == "__main__":
    cli()
