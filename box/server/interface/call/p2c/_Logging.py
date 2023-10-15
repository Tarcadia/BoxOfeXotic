

from dataclasses import dataclass
from dataclasses import field
from logging import DEBUG, INFO, WARNING, CRITICAL, ERROR
from time import time
from typing import List

from .._CallBase import CallBase


@dataclass
class LoggingCall(CallBase):
    ts              : int                   = field(default_factory=time)   # Timestamp
    level           : int                   = INFO
    tag             : List[str]             = field(default_factory=list)
    msg             : str                   = ""

def DebugCall(*args, **kwargs):
    return LoggingCall(*args, level=DEBUG, **kwargs)

def InfoCall(*args, **kwargs):
    return LoggingCall(*args, level=INFO, **kwargs)
    
def WarningCall(*args, **kwargs):
    return LoggingCall(*args, level=WARNING, **kwargs)
    
def Critical(*args, **kwargs):
    return LoggingCall(*args, level=CRITICAL, **kwargs)
    
def Error(*args, **kwargs):
    return LoggingCall(*args, level=ERROR, **kwargs)

