

from dataclasses import dataclass, field

from ._living import Living
from ._processor import Processor



@dataclass
class Resource(Living):
    path            : str
    owner           : Processor

    def __post_init__(self):
        self.owner = (
            Processor(**self.owner)
            if isinstance(self.owner, dict)
            else self.owner
        )


@dataclass
class ResourceNode():
    resource        : Resource
    nodes           : dict                  = field(default_factory=dict)

    def __post_init__(self):
        self.resource = (
            Processor(**self.resource)
            if isinstance(self.resource, dict)
            else self.resource
        )
        for key, node in self.nodes:
            self.nodes[key] = (
                ResourceNode(**node)
                if isinstance(node, dict)
                else node
            )

