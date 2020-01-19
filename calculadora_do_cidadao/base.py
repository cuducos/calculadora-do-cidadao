from abc import ABCMeta, abstractmethod
from datetime import date
from decimal import Decimal
from typing import Iterable, NamedTuple, Optional, Union

from rows import import_from_html
from rows.plugins.xls import import_from_xls

from calculadora_do_cidadao.download import Download
from calculadora_do_cidadao.typing import IndexesGenerator, MaybeIndexesGenerator


class AdapterNoImportMethod(Exception):
    pass


class AdapterDateNotAvailableError(Exception):
    pass


class Adapter(metaclass=ABCMeta):
    def __init__(self) -> None:
        functions = {"html": import_from_html, "xls": import_from_xls}
        try:
            self.read_from = functions[self.file_type]
        except KeyError:
            msg = (
                f"Invalid file type {self.file_type}. "
                f"Valid file types are: {', '.join(functions)}."
            )
            raise AdapterNoImportMethod(msg)

        self.data = {key: value for key, value in self.download()}
        if self.data:
            self.most_recent_date = max(self.data.keys())
        if self.should_aggregate:
            self.aggregate()

    @property
    def import_kwargs(self) -> Iterable[dict]:
        value = getattr(self, "IMPORT_KWARGS", {})
        return (value,) if isinstance(value, dict) else value

    @property
    def cookies(self) -> dict:
        return getattr(self, "COOKIES", {})

    @property
    def should_unzip(self) -> bool:
        return getattr(self, "SHOULD_UNZIP", False)

    @property
    def should_aggregate(self) -> bool:
        return getattr(self, "SHOULD_AGGREGATE", False)

    @property
    @abstractmethod
    def url(self) -> str:
        pass  # pragma: no cover

    @property
    @abstractmethod
    def file_type(self) -> str:
        pass  # pragma: no cover

    @abstractmethod
    def serialize(self, row: NamedTuple) -> MaybeIndexesGenerator:
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

    def aggregate(self):
        accumulated = 1
        for key in sorted(self.data.keys()):
            self.data[key] = accumulated * (1 + self.data[key])
            accumulated = self.data[key]

    def adjust(
        self,
        original_date: date,
        value: Union[Decimal, float, int, None] = 0,
        target_date: Optional[date] = None,
    ) -> Decimal:
        original = self.round_date(original_date, validate=True)
        target = self.most_recent_date
        if target_date:
            target = self.round_date(target_date, validate=True)

        value = Decimal(value or "1")
        percent = self.data[target] / self.data[original]
        return value * percent

    def download(self) -> IndexesGenerator:
        download = Download(self.url, self.should_unzip, self.cookies)
        with download() as path:
            for kwargs in self.import_kwargs:
                for data in self.read_from(path, **kwargs):
                    yield from (row for row in self.serialize(data) if row)
