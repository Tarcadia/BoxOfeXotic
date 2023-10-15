
from dataclasses import dataclass
from dataclasses import field
from math import nan
from time import time

from .._session import session_id
from .._Call import Call


@dataclass
class Ping(Call):
    session         : int                   = field(default_factory=session_id)
    timestamp       : float                 = field(default_factory=time)
    usage           : float                 = nan


@dataclass
class Pong(Call):
    resp            : int
    session         : int                   = field(default_factory=session_id)
    timestamp       : float                 = field(default_factory=time)


@dataclass
class Pang(Call):
    resp            : int
    timestamp       : float                 = field(default_factory=time)

