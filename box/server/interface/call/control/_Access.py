

from dataclasses import dataclass
from dataclasses import field
from time import time

from ..._session import session_id
from .._CallBase import CallBase
from ._Hello import Processor


@dataclass
class AccessPull(CallBase):
    processor       : Processor

    def __post_init__(self):
        self.processor =(
            Processor(**self.processor)
            if isinstance(self.processor, dict)
            else self.processor
        )


@dataclass
class AccessPush(CallBase):
    processor       : Processor
    token           : str                   = ""
    timestamp       : float                 = field(default_factory=time)
    ttl             : int                   = 3600
    session         : int                   = field(default_factory=session_id)

    def __post_init__(self):
        self.processor =(
            Processor(**self.processor)
            if isinstance(self.processor, dict)
            else self.processor
        )


@dataclass
class AccessPushOff(CallBase):
    processor       : Processor

    def __post_init__(self):
        self.processor =(
            Processor(**self.processor)
            if isinstance(self.processor, dict)
            else self.processor
        )

