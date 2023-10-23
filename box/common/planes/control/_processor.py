

from dataclasses import field
from typing import List

from box.common.callclasses import callclass
from box.common.callclasses import respondedclass
from box.common.callclasses import respondingclass
from box.common.resources import get_address, address_to_host_port
from box.common.resources import Processor



@respondedclass
class ProcessorRegister():
    processor       : Processor
    
    def __post_init__(self):
        self.processor = (
            Processor(**self.processor)
            if isinstance(self.processor, dict)
            else self.processor
        )

@respondingclass(to=[ProcessorRegister])
class ProcessorRegisterResp():
    ack             : bool                  = True



@respondedclass
class ProcessorRegistryPull():
    addresses       : List[str]             = field(default_factory=list)

    def __post_init__(self):
        self.addresses = [
            get_address(*address_to_host_port(address))
            for address in self.addresses
        ]

@respondingclass(to=[ProcessorRegistryPull])
class ProcessorRegistryPullResp():
    processors      : List[Processor]       = field(default_factory=list)
    
    def __post_init__(self):
        for idx, processor in enumerate(self.processors):
            self.processors[idx] = (
                Processor(**processor)
                if isinstance(processor, dict)
                else processor
            )



@callclass
class ProcessorRegistryPush():
    processors      : List[Processor]       = field(default_factory=list)
    
    def __post_init__(self):
        for idx, processor in enumerate(self.processors):
            self.processors[idx] = (
                Processor(**processor)
                if isinstance(processor, dict)
                else processor
            )

