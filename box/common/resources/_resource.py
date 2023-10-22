

from dataclasses import dataclass

from ._living import Living



@dataclass
class Resource(Living):
    path            : str
    owner           : str

