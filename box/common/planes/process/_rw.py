

from dataclasses import field
from typing import List

from box.common.callclasses import respondedclass
from box.common.callclasses import respondingclass



@respondedclass
class ReadResource():
    path            : str
    fields          : List[list]            = field(default_factory=list)

@respondingclass(to=[ReadResource])
class ReadResourceResp():
    fields          : dict



@respondedclass
class WriteResource():
    path            : str
    fields          : List[list]            = field(default_factory=dict)

@respondingclass(to=[WriteResource])
class WriteResourceResp():
    fields          : dict



@respondingclass(to=[ReadResource, WriteResource])
class ResourceNack():
    exception       : str                   = ""

