

from threading import Lock
from box.common.resources import Processor


class ProcDict():

    ## TODO: Introduce TTL feature for entries.

    def __init__(self) -> None:
        self.rtt = {}
        self.proc_dict = {}
        self._modify_lock = Lock()
    
    
    def update(self, address, timestamp=None, desc=None, usage=None, rtt=None):
        _processor = self.proc_dict.get(address, None)
        if _processor is None:
            return
        if not rtt is None:
            self.rtt[address] = rtt
        if not timestamp is None:
            _processor.timestamp = timestamp
        if not desc is None:
            _processor.desc = desc
        if not usage is None:
            _processor.usage = usage

    def insert(self, processor: Processor):
        with self._modify_lock:
            if not processor.address in self.proc_dict:
                self.proc_dict[processor.address] = processor
                return True
            else:
                if (
                    self.proc_dict[processor.address].life() < processor.life()
                    and self.proc_dict[processor.address].timestamp < processor.timestamp
                ):
                    self.proc_dict[processor.address] = processor
                    return True
                else:
                    return False
    
    def query(self, address: str):
        if address in self.proc_dict:
            return self.proc_dict[address]
        else:
            return None

