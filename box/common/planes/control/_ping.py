

from dataclasses import field
from math import nan
from time import time

from box.common.callclasses import respondedclass
from box.common.callclasses import respondingclass



@respondedclass
class Ping():
    address         : str
    t0              : float                 = field(default_factory=time)
    desc            : str                   = ""
    usage           : float                 = nan


@respondedclass
@respondingclass(to=[Ping])
class Pong():
    address         : str
    t0              : float
    t1              : float                 = field(default_factory=time)


@respondingclass(to=[Pong])
class Pang():
    address         : str
    t0              : float
    t1              : float
    t2              : float                 = field(default_factory=time)

