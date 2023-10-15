

from dataclasses import dataclass
from dataclasses import field
from time import time
from typing import List

from .._session import session_id
from .._Call import Call


@dataclass
class RegistEntry:
    resource        : str
    host            : str
    port            : int
    timestamp       : float                 = field(default_factory=time)
    ttl             : int                   = 60
    token           : str                   = ""


@dataclass
class Regist(Call):
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
class RegistResp(Call):
    resp            : int
    entries_ack     : List[bool]


