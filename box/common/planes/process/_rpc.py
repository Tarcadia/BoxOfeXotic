

from dataclasses import field
from typing import Any

from box.common.callclasses import callclass
from box.common.callclasses import respondedclass
from box.common.callclasses import respondingclass



@callclass
class CallResource():
    subject         : str
    object          : str
    provided        : dict
    method          : str
    args            : list                  = field(default_factory=list)
    kwargs          : dict                  = field(default_factory=dict)



@respondedclass
class CallResourceResponded():
    pass

@respondingclass(to=[])
class CallResourceResponding():
    ret             : Any                   = ""

