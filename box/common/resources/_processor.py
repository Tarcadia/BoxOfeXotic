

from dataclasses import dataclass
from math import nan
from time import time

from ._living import Living
from ._protocol import address_to_host_port, get_address



EMPTY_PROCESSOR_TTL = 1

@dataclass
class Processor(Living):
    address         : str
    token           : str                   = ""
    desc            : str                   = ""
    usage           : float                 = nan

    def __post_init__(self):
        self.address = get_address(*address_to_host_port(self.address))


@dataclass
class EmptyProcessor(Processor):
    ttl             : float                 = 0
    timestamp       : float                 = 0
    address         : str                   = ""
    token           : str                   = ""
    desc            : str                   = ""
    usage           : float                 = nan

    @property
    def ttl(self):
        return EMPTY_PROCESSOR_TTL
    
    @ttl.setter
    def ttl(self, _ttl):
        return _ttl

    @property
    def timestamp(self):
        return time()
    
    @timestamp.setter
    def timestamp(self, _timestamp):
        return _timestamp
