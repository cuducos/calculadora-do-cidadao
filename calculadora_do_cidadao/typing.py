from datetime import date
from decimal import Decimal
from typing import Dict, Iterable, NamedTuple, Optional, Tuple


Index = Tuple[date, Decimal]
MaybeIndex = Optional[Index]

IndexDictionary = Dict[date, Decimal]

IndexesGenerator = Iterable[Index]
MaybeIndexesGenerator = Iterable[MaybeIndex]
