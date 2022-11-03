from abc import ABCMeta, abstractmethod
from collections import namedtuple
from datetime import date
from decimal import Decimal
from itertools import chain
from json import load
from pathlib import Path
from typing import Any, Iterable, List, NamedTuple, Optional, Union

from calculadora_do_cidadao.download import Download
from calculadora_do_cidadao.fields import DateField
from calculadora_do_cidadao.rows.fields import DecimalField
from calculadora_do_cidadao.rows.plugins.dicts import import_from_dicts
from calculadora_do_cidadao.rows.plugins.plugin_csv import (
    export_to_csv,
    import_from_csv,
)
from calculadora_do_cidadao.rows.plugins.plugin_html import import_from_html
from calculadora_do_cidadao.rows.plugins.xls import import_from_xls
from calculadora_do_cidadao.typing import (
    Date,
    IndexDictionary,
    IndexesGenerator,
    MaybeIndexesGenerator,
)


def import_from_json(path: Path, json_path: List[str]) -> Iterable[NamedTuple]:
    """Imports data form a JSON file `path` creating an iterable of named
    tuples similar to the Rows's import functions.

    `json_path` is a sequence of keys or array indexes to get to the array with
    the desired data.
    """

    with path.open() as handler:
        data = load(handler)

    for key_or_index in json_path:
        data = data[key_or_index]

    if not data:
        return

    keys = tuple(str(key) for key in data[0].keys())
    Row = namedtuple("Row", keys)  # type: ignore
    yield from (Row(**row) for row in data)  # type: ignore


class AdapterNoImportMethod(Exception):
    """To be used when the adapter has no `rows` import method set."""

    pass


class AdapterDateNotAvailableError(Exception):
    """To be used when using a date outside of the range available."""

    pass


class Adapter(metaclass=ABCMeta):
    """This is the base adapter, all adapters should inherit from it. Its
    children require at least a `url` and `file_type` class variables."""

    def __init__(self, exported_csv: Path = None) -> None:
        """The initialization of the Adapter consists of four steps.

        First, it tries to infer the `rows` import method to use from the
        `file_type` class variable (which can be `html`, `xls` or `json`).

        Then it detects whether data will come from a download or from an
        exported CSV file.

        If it comes from a download, it uses the `Download` class to store
        index data.

        Finally, if the source data is disaggregated, it calls the `aggregate`
        method.
        """
        functions = {
            "html": import_from_html,
            "json": import_from_json,
            "xls": import_from_xls,
        }
        try:
            self.read_from = functions[self.file_type]
        except KeyError:
            msg = (
                f"Invalid file type {self.file_type}. "
                f"Valid file types are: {', '.join(functions)}."
            )
            raise AdapterNoImportMethod(msg)

        self.data: IndexDictionary = {}
        if exported_csv:
            self.data = {key: value for key, value in self.from_csv(exported_csv)}
        else:
            self.data = {key: value for key, value in self.download()}
            if self.should_aggregate:
                self.aggregate()

        if self.data:
            self.most_recent_date = max(self.data.keys())

    @property
    def import_kwargs(self) -> Iterable[dict]:
        """Wrapper to get IMPORT_KWARGS if set, avoiding error if not set."""
        value = getattr(self, "IMPORT_KWARGS", {})
        return (value,) if isinstance(value, dict) else value

    @property
    def cookies(self) -> dict:
        """Wrapper to get COOKIES if set, avoiding error if not set."""
        return getattr(self, "COOKIES", {})

    @property
    def post_data(self) -> Optional[dict]:
        """Wrapper to get POST_DATA if set, avoiding error if not set."""
        return getattr(self, "POST_DATA", None)

    @property
    def headers(self) -> Optional[dict]:
        """Wrapper to get HEADERS if set, avoiding error if not set."""
        return getattr(self, "HEADERS", None)

    @property
    def should_unzip(self) -> bool:
        """Wrapper to get SHOULD_UNZIP if set, avoiding error if not set."""
        return getattr(self, "SHOULD_UNZIP", False)

    @property
    def should_aggregate(self) -> bool:
        """Wrapper to get SHOULD_AGGREGATE if set, avoiding error if not set."""
        return getattr(self, "SHOULD_AGGREGATE", False)

    @property
    @abstractmethod
    def url(self) -> str:
        """The URL where to get data from."""
        pass  # pragma: no cover

    @property
    @abstractmethod
    def file_type(self) -> str:
        """File type of the response from the `url`, usually html or xls."""
        pass  # pragma: no cover

    @abstractmethod
    def serialize(self, row: NamedTuple) -> MaybeIndexesGenerator:
        """This method should be a generator that receives a row from `rows`
        (which is a `NamedTuple`) and yields `None` if the row does not hold
        any valid index data, or yields `calculadora_do_cidadao.typing.Index`
        type if the row has valid data. A row can yield more than one
        `calculadora_do_cidadao.typing.Index`.
        """
        pass  # pragma: no cover

    def invalid_date_error_message(self, wanted: date) -> str:
        """Helper to generate an error message usually used together with
        `AdapterDateNotAvailableError`."""
        first, last = min(self.data.keys()), max(self.data.keys())
        if first < wanted < last:
            msg = (
                f"This adapter has data from {first.month:0>2d}/{first.year} "
                f"to {last.month:0>2d}/{last.year}, but not for "
                f"{wanted.month:0>2d}/{wanted.year}. Available dates are:"
            )
            available = (f"    - {d.month:0>2d}/{d.year}" for d in self.data)
            return "\n".join(chain((msg,), available))

        return (
            f"This adapter has data from {first.month:0>2d}/{first.year} "
            f"to {last.month:0>2d}/{last.year}. "
            f"{wanted.month:0>2d}/{wanted.year} is out of range."
        )

    def round_date(self, obj: Date, validate: bool = False) -> date:
        """Method to round `Date` objects to hold `day = 1`, as indexes usually
        refers to monthly periods, not daily periods. It also validates if the
        intended date is valid and in the adapter data range."""
        parsed = DateField.deserialize(obj)
        output = parsed.replace(day=1)
        if validate and output not in self.data.keys():
            msg = self.invalid_date_error_message(output)
            raise AdapterDateNotAvailableError(msg)
        return output

    def aggregate(self):
        """Being disaggregated here means the index for each month is a
        percentage relative to the previous month. However the `adjust` method
        gets way simpler if the indexes as stored as the percentage of the
        month before the first month of the series. For example, if a given
        index starts at January 1994, and all values should be a percentage
        referring to December 1993."""
        accumulated = 1
        for key in sorted(self.data.keys()):
            self.data[key] = accumulated * (1 + self.data[key])
            accumulated = self.data[key]

    def adjust(
        self,
        original_date: Date,
        value: Union[Decimal, float, int, None] = 0,
        target_date: Optional[Date] = None,
    ) -> Decimal:
        """Main method of an adapter API, the one that actually makes the
        monetary correction using adapter's data. It requires a `datetime.date`
        used as the reference for the operation.

        If no `value` if given, it returns considering the value is
        `decimal.Decimal('1')`.

        If no `target_date` is given, it returns considering the target date is
        `datetime.date.today()`."""
        original = self.round_date(original_date, validate=True)
        target = self.most_recent_date
        if target_date:
            target = self.round_date(target_date, validate=True)

        value = Decimal(value or "1")
        percent = self.data[target] / self.data[original]
        return value * percent

    def download(self) -> IndexesGenerator:
        """Wrapper to use the `Download` class and pipe the result to `rows`
        imported method, yielding a series of rows parsed by `rows`."""
        post_processing = getattr(self, "post_processing", None)
        download = Download(
            url=self.url,
            should_unzip=self.should_unzip,
            headers=self.headers,
            cookies=self.cookies,
            post_data=self.post_data,
            post_processing=post_processing,
        )

        with download() as paths:
            for path in paths():
                for kwargs in self.import_kwargs:
                    for data in self.read_from(path, **kwargs):  # type: ignore
                        yield from (row for row in self.serialize(data) if row)

    def export_index(self, key, include_name: bool = False) -> dict:
        """Export a given index as a dictionary to be used with
        `rows.import_from_dicts`."""
        data = {"date": key, "value": self.data[key]}

        if include_name:
            data["serie"] = self.__class__.__name__.lower()

        return data

    def export(self, include_name: bool = False) -> Iterable[dict]:
        """Wraps adapter's data in a sequence of dictionaries to be used with
        `rows.import_from_dicts`."""
        keys = sorted(self.data)
        yield from (self.export_index(key, include_name) for key in keys)

    def to_csv(self, path: Path) -> Path:
        """Export the adapter's data to a CSV file."""
        table = import_from_dicts(self.export())
        export_to_csv(table, path)
        return path

    def from_csv(self, path: Path) -> IndexesGenerator:
        """Load adapter's data from a CSV file. If the CSV file has two columns
        it is assumed it was generated with the `to_csv` method. If it has 3
        columns, it is assumed it is a export of all adapters' data generated
        by the CLI."""
        fields = {"date": DateField, "value": DecimalField}
        table = import_from_csv(path, force_types=fields)
        if len(table.fields) == 2:  # generated via adapter's to_csv method
            yield from table
        else:  # 3 columns table, export of all adapters generated by CLI
            yield from (
                (row.date, row.value)
                for row in table
                if row.serie == self.__class__.__name__.lower()
            )
