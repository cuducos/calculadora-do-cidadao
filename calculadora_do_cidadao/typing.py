from datetime import date, datetime
from decimal import Decimal
from typing import Dict, Iterable, Optional, Tuple, Union


Index = Tuple[date, Decimal]
MaybeIndex = Optional[Index]

IndexDictionary = Dict[date, Decimal]

IndexesGenerator = Iterable[Index]
MaybeIndexesGenerator = Iterable[MaybeIndex]

Date = Union[date, datetime, int, float, str]  # parsed by fields.DateField
