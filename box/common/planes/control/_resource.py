

from dataclasses import field
from typing import List

from box.common.callclasses import callclass
from box.common.callclasses import respondedclass
from box.common.callclasses import respondingclass
from box.common.resources import Resource



@respondedclass
class ResourceRegister():
    resources       : List[Resource]
    
    def __post_init__(self):
        for idx, resource in enumerate(self.resources):
            self.resources[idx] = (
                Resource(**resource)
                if isinstance(resource, dict)
                else resource
            )

@respondingclass(to=[ResourceRegister])
class ResourceRegisterResp():
    acks            : List[bool]



@respondedclass
class ResourceRegistryPull():
    paths           : List[str]             = field(default_factory=list)

@respondingclass(to=[ResourceRegistryPull])
class ResourceRegistryPullResp():
    resources       : dict                  = field(default_factory=dict)
    
    def __post_init__(self):
        for key, resource in self.resources.items():
            self.resources[key] = (
                Resource(**resource)
                if isinstance(resource, dict)
                else resource
            )



@callclass
class ResourceRegistryPush():
    resources       : List[Resource]        = field(default_factory=list)
    
    def __post_init__(self):
        for idx, resource in enumerate(self.resources):
            self.resources[idx] = (
                Resource(**resource)
                if isinstance(resource, dict)
                else resource
            )

