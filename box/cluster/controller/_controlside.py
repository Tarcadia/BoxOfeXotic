

from concurrent.futures import ThreadPoolExecutor
from time import time

from box.cluster.network import Server
from box.cluster.network import Serdes
from box.common.callclasses import impl, respondedimpl, respondingimpl
from box.common.callclasses import respondedclass, is_respondedclass
from box.common.planes.control import Ping, Pong, Pang
from box.common.planes.control import ProcessorRegister, ProcessorRegisterResp
from box.common.planes.control import ProcessorRegistryPull, ProcessorRegistryPullResp
from box.common.planes.control import ProcessorRegistryPush
from box.common.planes.control import ResourceRegister, ResourceRegisterResp
from box.common.planes.control import ResourceRegistryPull, ResourceRegistryPullResp
from box.common.planes.control import ResourceRegistryPush
from box.common.resources import EmptyProcessor, EmptyResource
from box.common.resources import BOX_NULL_URL

from box.cluster.util import LutNode
from box.cluster.util import ProcDict



ADDRESS = "box://127.0.0.1:62222"
MAX_WORKERS = 32

EMPTY_PROCESSOR = EmptyProcessor(address=BOX_NULL_URL)
EMPTY_RESOURCE = EmptyResource(path="/")

serdes              : Serdes                = Serdes()
res_lut             : LutNode               = LutNode(None)
proc_dict           : ProcDict              = ProcDict()

thread_pool         : ThreadPoolExecutor    = None
server              : Server                = None
_initialized        : bool                  = False

def _on_packet(addr, packet):
    _obj = serdes.desirialize(packet)
    if is_respondedclass(_obj):
        _ret, _resp = _obj()
        return serdes.serialize(_resp)
    else:
        _ret = _obj()
        return

def init(address = ADDRESS, _thread_pool = None, _max_workers=MAX_WORKERS):
    global thread_pool
    global server
    thread_pool = (
        ThreadPoolExecutor(max_workers=_max_workers)
        if _thread_pool is None
        else _thread_pool
    )
    server = Server(address, thread_pool_workers=thread_pool)
    server.on_packet(_on_packet)

    global _initialized
    _initialized = True

def start():
    if _initialized:
        server.start()
    else:
        raise RuntimeError("Module not initialized, call init() to initialize.")



## Ping

@serdes.register
@respondedimpl(Ping)
def Ping(self: Ping):
    pong = Pong.make_response(self, address=self.address, t0=self.t0)
    thread_pool.submit(pong)
    proc_dict.update(self.address, desc=self.desc, usage=self.usage)

@serdes.register
@respondedclass
@respondingimpl(Pong, to=[Ping])
def Pong(self: Pong):
    pang = self.get_response()
    rtt = 0.5 * (time() + pang.t2 - pang.t1 - pang.t0)
    proc_dict.update(self.address, rtt=rtt)

@serdes.register
@respondingimpl(Pang, to=[Pong])
def Pang(self: Pang):
    proc_dict.update(self.address, self.t2)



## Processor

@serdes.register
@respondedimpl(ProcessorRegister)
def ProcessorRegister(self: ProcessorRegister):
    ack = proc_dict.insert(self.processor)
    resp = ProcessorRegisterResp.make_response(self, ack=ack)
    thread_pool.submit(resp)
    
@serdes.register
@respondingimpl(ProcessorRegisterResp, to=[ProcessorRegister])
def ProcessorRegisterResp(self: ProcessorRegisterResp):
    pass

@serdes.register
@respondedimpl(ProcessorRegistryPull)
def ProcessorRegistryPull(self: ProcessorRegistryPull):
    processors = {}
    for address in set(self.addresses):
        _processor = proc_dict.query(address)
        processors[address] = (
            _processor
            if _processor
            else EMPTY_PROCESSOR
        )
    ProcessorRegistryPullResp.make_response(self, processors=processors)

@serdes.register
@respondingimpl(ProcessorRegistryPullResp, to=[ProcessorRegistryPull])
def ProcessorRegistryPullResp(self: ProcessorRegistryPullResp):
    pass

@serdes.register
@impl(ProcessorRegistryPush)
def ProcessorRegistryPush(self: ProcessorRegistryPush):
    pass



# Resource

@serdes.register
@respondedimpl(ResourceRegister)
def ResourceRegister(self: ResourceRegister):
    acks = [res_lut.insert(res.path, res) for res in self.resources]
    ResourceRegisterResp.make_response(self, acks=acks)

@serdes.register
@respondingimpl(ResourceRegisterResp, to=[ResourceRegister])
def ResourceRegisterResp(self: ResourceRegisterResp):
    pass

@serdes.register
@respondedimpl(ResourceRegistryPull)
def ResourceRegistryPull(self: ResourceRegistryPull):
    resources = {}
    for path in set(self.paths):
        _resource_line = res_lut.query(path)
        resources[path] = (
            _resource_line[-1]
            if _resource_line
            else EMPTY_RESOURCE
        )
    ResourceRegistryPullResp.make_response(self, resources=resources)

@serdes.register
@respondingimpl(ResourceRegistryPullResp, to=[ResourceRegistryPull])
def ResourceRegistryPullResp(self: ResourceRegistryPullResp):
    pass

@serdes.register
@respondedimpl(ResourceRegistryPush)
def ResourceRegistryPush(self: ResourceRegistryPush):
    pass

