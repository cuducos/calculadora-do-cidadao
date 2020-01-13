from abc import ABCMeta, abstractmethod
from datetime import date
from decimal import Decimal
from typing import Iterator, NamedTuple, Optional, Tuple, Union

from rows.plugins.xls import import_from_xls

from calculadora_do_cidadao.download import Download


class AdapterDateNotAvailableError(Exception):
    pass


class Adapter(metaclass=ABCMeta):
    def __init__(self) -> None:
        self.data = {key: value for key, value in self.download()}
        self.most_recent_date = max(self.data.keys())

    @property
    def import_kwargs(self) -> dict:
        return getattr(self, "IMPORT_KWARGS", {})

    @property
    @abstractmethod
    def url(self) -> str:
        pass  # pragma: no cover

    @abstractmethod
    def serialize(self, row: NamedTuple) -> Union[Tuple[date, Decimal], None]:
        pass  # pragma: no cover

    def invalid_date_error_message(self, wanted: date) -> str:
        first, last = min(self.data.keys()), max(self.data.keys())
        return (
            f"This adapter has data from {first.month:0>2d}/{first.year} "
            f"to {last.month:0>2d}/{last.year}. "
            f"{wanted.month:0>2d}/{wanted.year} is out of range."
        )

    def round_date(self, obj: date, validate: bool = False) -> date:
        output = date(obj.year, obj.month, 1)
        if validate and output not in self.data.keys():
            msg = self.invalid_date_error_message(output)
            raise AdapterDateNotAvailableError(msg)
        return output

    def adjust(
        self,
        original_date: date,
        value: Optional[Union[Decimal, float, int]] = 0,
        target_date: Optional[date] = None,
    ) -> Decimal:
        original = self.round_date(original_date, validate=True)
        target = self.most_recent_date
        if target_date:
            target = self.round_date(target_date, validate=True)

        value = Decimal(value or "1")
        percent = self.data[target] / self.data[original]
        return value * percent

    def download(self) -> Iterator[Tuple[date, Decimal]]:
        download = Download(self.url)
        with download() as path:
            table = import_from_xls(path, **self.import_kwargs)
            rows = (self.serialize(row) for row in table)
            yield from (row for row in rows if row)
