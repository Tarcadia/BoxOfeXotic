

from dataclasses import dataclass
from dataclasses import field
from typing import Any

from .._session import session_id
from .._Call import Call


@dataclass
class Command(Call):
    command         : str
    args            : list                  = field(default_factory=list)
    kwargs          : dict                  = field(default_factory=dict)
    session         : int                   = field(default_factory=session_id)


@dataclass
class CommandResp(Call):
    resp            : int
    ret             : Any                   = ""

