

from threading import Lock
from box.common.resources import Processor


class ProcDict():

    def __init__(self) -> None:
        self.rtt = {}
        self.proc_dict = {}
        self._modify_lock = Lock()
    
    
    def update(self, address, desc=None, usage=None, rtt=None):
        if not rtt is None:
            self.rtt[address] = rtt
        
        if not address in self.proc_dict:
            return
        if not desc is None or not usage is None:
            with self._modify_lock:
                if not desc is None:
                    self.proc_dict[address].desc = desc
                if not usage is None:
                    self.proc_dict[address].usage = usage

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

