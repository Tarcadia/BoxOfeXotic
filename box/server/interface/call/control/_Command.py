

from dataclasses import dataclass
from dataclasses import field
from typing import Any

from .._session import session_id
from .._CallBase import CallBase


@dataclass
class CommandCall(CallBase):
    command         : str
    args            : list                  = field(default_factory=list)
    kwargs          : dict                  = field(default_factory=dict)
    session         : int                   = field(default_factory=session_id)


@dataclass
class CommandResp(CallBase):
    resp            : int
    ret             : Any                   = ""

