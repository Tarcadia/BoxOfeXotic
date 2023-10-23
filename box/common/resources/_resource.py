

from dataclasses import dataclass

from ._living import Living
from ._protocol import address_to_host_port, get_address



@dataclass
class Resource(Living):
    path            : str
    owner           : str

    def __post_init__(self):
        self.owner = get_address(*address_to_host_port(self.owner))
