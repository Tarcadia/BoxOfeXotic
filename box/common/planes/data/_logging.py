

from dataclasses import field
from logging import CRITICAL, DEBUG, ERROR, INFO, WARNING
from time import time
from typing import List

from box.common.callclasses import callclass



@callclass
class Logging():
    Timestamp       : int                   = field(default_factory=time)
    level           : int                   = INFO
    tag             : List[str]             = field(default_factory=list)
    msg             : str                   = ""

def DebugCall(*args, **kwargs):
    return Logging(*args, level=DEBUG, **kwargs)

def InfoCall(*args, **kwargs):
    return Logging(*args, level=INFO, **kwargs)
    
def WarningCall(*args, **kwargs):
    return Logging(*args, level=WARNING, **kwargs)
    
def Critical(*args, **kwargs):
    return Logging(*args, level=CRITICAL, **kwargs)
    
def Error(*args, **kwargs):
    return Logging(*args, level=ERROR, **kwargs)

