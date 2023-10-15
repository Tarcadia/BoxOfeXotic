

from dataclasses import dataclass
from dataclasses import field
from typing import List

from .._session import session_id
from .._Call import Call


@dataclass
class ResRead(Call):
    resource        : str
    fields          : List[str]             = field(default_factory=list)
    session         : int                   = field(default_factory=session_id)


@dataclass
class ResWrite(Call):
    resource        : str
    fields          : dict                  = field(default_factory=dict)
    session         : int                   = field(default_factory=session_id)


@dataclass
class ResNackResp(Call):
    resp            : int
    exception       : str                   = ""


@dataclass
class ResReadResp(Call):
    resp            : int
    fields          : dict


@dataclass
class ResWriteResp(Call):
    resp            : int
    fields          : dict

