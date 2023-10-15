

from dataclasses import dataclass
from dataclasses import field
from logging import DEBUG, INFO, WARNING, CRITICAL, ERROR
from time import time
from typing import List

from .._Call import Call


@dataclass
class Logging(Call):
    ts              : int                   = field(default_factory=time)   # Timestamp
    level           : int                   = INFO
    tag             : List[str]             = field(default_factory=list)
    msg             : str                   = ""

def Debug(*args, **kwargs):
    return Logging(*args, level=DEBUG, **kwargs)

def Info(*args, **kwargs):
    return Logging(*args, level=INFO, **kwargs)
    
def Warning(*args, **kwargs):
    return Logging(*args, level=WARNING, **kwargs)
    
def Critical(*args, **kwargs):
    return Logging(*args, level=CRITICAL, **kwargs)
    
def Error(*args, **kwargs):
    return Logging(*args, level=ERROR, **kwargs)

