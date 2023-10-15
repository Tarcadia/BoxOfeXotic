

from dataclasses import dataclass
from dataclasses import field
from typing import List

from ..._session import session_id
from .._CallBase import CallBase


@dataclass
class ResReadCall(CallBase):
    resource        : str
    fields          : List[str]             = field(default_factory=list)
    session         : int                   = field(default_factory=session_id)


@dataclass
class ResWriteCall(CallBase):
    resource        : str
    fields          : dict                  = field(default_factory=dict)
    session         : int                   = field(default_factory=session_id)


@dataclass
class ResNackResp(CallBase):
    resp            : int
    exception       : str                   = ""


@dataclass
class ResReadResp(CallBase):
    resp            : int
    fields          : dict


@dataclass
class ResWriteResp(CallBase):
    resp            : int
    fields          : dict

