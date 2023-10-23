

from dataclasses import dataclass
from math import nan

from ._living import Living
from ._protocol import address_to_host_port, get_address



@dataclass
class Processor(Living):
    address         : str
    token           : str                   = ""
    desc            : str                   = ""
    usage           : float                 = nan

    def __post_init__(self):
        self.address = get_address(*address_to_host_port(self.address))