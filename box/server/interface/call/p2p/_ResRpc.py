

from dataclasses import dataclass
from dataclasses import field
from typing import Any

from .._session import session_id
from .._CallBase import CallBase


@dataclass
class RpcSubject():
    resource        : str
    data            : dict

@dataclass
class RpcObject():
    resource        : str
    method          : str
    args            : list                  = field(default_factory=list)
    kwargs          : dict                  = field(default_factory=dict)


@dataclass
class ResRpcCall(CallBase):
    subject         : RpcSubject
    object          : RpcObject

    def __post_init__(self):
        self.subject = (
            RpcSubject(**self.subject)
            if isinstance(self.subject, dict)
            else self.subject
        )
        self.object = (
            RpcObject(**self.object)
            if isinstance(self.object, dict)
            else self.object
        )


@dataclass
class ResRpcrCall(ResRpcCall):
    session         : int                   = field(default_factory=session_id)


@dataclass
class ResRpcrResp(CallBase):
    resp            : int
    ret             : Any                   = ""



