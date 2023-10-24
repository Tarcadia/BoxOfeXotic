

from dataclasses import field
from math import nan
from time import time

from box.common.callclasses import respondedclass
from box.common.callclasses import respondingclass
from box.common.resources import address_to_host_port, get_address



@respondedclass
class Ping():
    address         : str
    t0              : float                 = field(default_factory=time)
    desc            : str                   = ""
    usage           : float                 = nan

    def __post_init__(self):
        self.address = get_address(*address_to_host_port(self.address))



@respondedclass
@respondingclass(to=[Ping])
class Pong():
    address         : str
    t0              : float
    t1              : float                 = field(default_factory=time)

    def __post_init__(self):
        self.address = get_address(*address_to_host_port(self.address))


@respondingclass(to=[Pong])
class Pang():
    address         : str
    t0              : float
    t1              : float
    t2              : float                 = field(default_factory=time)

    def __post_init__(self):
        self.address = get_address(*address_to_host_port(self.address))

