

from dataclasses import field
from math import nan
from time import time

from box.common.callclasses import respondedclass
from box.common.callclasses import respondingclass



@respondedclass
class Ping():
    timestamp       : float                 = field(default_factory=time)
    desc            : str                   = ""
    usage           : float                 = nan


@respondedclass
@respondingclass(to=[Ping])
class Pong():
    t0              : float
    timestamp       : float                 = field(default_factory=time)


@respondingclass(to=[Pong])
class Pang():
    t0              : float
    t1              : float
    timestamp       : float                 = field(default_factory=time)

