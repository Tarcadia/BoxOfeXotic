

from dataclasses import field
from typing import Any

from box.common.callclasses import callclass
from box.common.callclasses import respondedclass
from box.common.callclasses import respondingclass
from box.common.resources import get_url, url_to_host_port_path



@callclass
class CallResource():
    subject         : str
    object          : str
    provided        : dict
    method          : str
    args            : list                  = field(default_factory=list)
    kwargs          : dict                  = field(default_factory=dict)

    def __post_init__(self):
        self.subject = get_url(*url_to_host_port_path(self.subject))
        self.object = get_url(*url_to_host_port_path(self.object))


@respondedclass
class CallResourceResponded():
    pass

@respondingclass(to=[])
class CallResourceResponding():
    ret             : Any                   = ""

