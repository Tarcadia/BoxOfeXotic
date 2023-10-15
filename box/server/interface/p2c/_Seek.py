

from dataclasses import dataclass
from dataclasses import field
from typing import List

from .._session import session_id
from .._Call import Call
from ._Regist import RegistEntry


@dataclass
class Seek(Call):
    session         : int                   = field(default_factory=session_id)
    resources       : List[str]             = field(default_factory=list)


@dataclass
class SeekResp(Call):
    resp            : int
    entries         : List[RegistEntry]

    def __post_init__(self):
        self.entries = [
            RegistEntry(**_entry)
            if isinstance(_entry, dict)
            else _entry
            for _entry in self.entries
        ]
