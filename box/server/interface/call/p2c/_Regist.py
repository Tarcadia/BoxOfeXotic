

from dataclasses import dataclass
from dataclasses import field
from time import time
from typing import List

from ..._session import session_id
from ..control import Processor
from .._CallBase import CallBase


@dataclass
class RegistEntry:
    resource        : str
    processor       : Processor
    timestamp       : float                 = field(default_factory=time)
    ttl             : int                   = 60

    def __post_init__(self):
        self.processor =(
            Processor(**self.processor)
            if isinstance(self.processor, dict)
            else self.processor
        )


@dataclass
class RegistCall(CallBase):
    session         : int                   = field(default_factory=session_id)
    entries         : List[RegistEntry]     = field(default_factory=list)

    def __post_init__(self):
        self.entries = [
            RegistEntry(**_entry)
            if isinstance(_entry, dict)
            else _entry
            for _entry in self.entries
        ]


@dataclass
class RegistResp(CallBase):
    resp            : int
    entries_ack     : List[bool]


