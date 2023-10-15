

from dataclasses import dataclass
from dataclasses import field
from math import nan
from time import time

from .._session import session_id
from .._CallBase import CallBase


@dataclass
class Ping(CallBase):
    session         : int                   = field(default_factory=session_id)
    timestamp       : float                 = field(default_factory=time)
    usage           : float                 = nan


@dataclass
class Pong(CallBase):
    resp            : int
    session         : int                   = field(default_factory=session_id)
    timestamp       : float                 = field(default_factory=time)


@dataclass
class Pang(CallBase):
    resp            : int
    timestamp       : float                 = field(default_factory=time)

