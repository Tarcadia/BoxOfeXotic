

from dataclasses import dataclass
from math import nan

from ._living import Living



@dataclass
class Processor(Living):
    address         : str
    token           : str                   = ""
    desc            : str                   = ""
    usage           : float                 = nan
