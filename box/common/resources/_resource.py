

from dataclasses import dataclass
from time import time

from ._living import Living
from ._protocol import address_to_host_port, get_address



EMPTY_RESOURCE_TTL = 1

@dataclass
class Resource(Living):
    path            : str
    owner           : str

    def __post_init__(self):
        if self.owner is None:
            return
        self.owner = get_address(*address_to_host_port(self.owner))


@dataclass
class EmptyResource(Resource):
    ttl             : float                 = 0
    timestamp       : float                 = 0
    path            : str                   = ""
    owner           : str                   = None

    @property
    def ttl(self):
        return EMPTY_RESOURCE_TTL
    
    @ttl.setter
    def ttl(self, _ttl):
        return _ttl

    @property
    def timestamp(self):
        return time()
    
    @timestamp.setter
    def timestamp(self, _timestamp):
        return _timestamp
