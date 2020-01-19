from datetime import date
from decimal import Decimal
from typing import Iterable, NamedTuple, Optional, Tuple


Index = Tuple[date, Decimal]
MaybeIndex = Optional[Index]

IndexesGenerator = Iterable[Index]
MaybeIndexesGenerator = Iterable[MaybeIndex]
