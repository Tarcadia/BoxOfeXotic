

from concurrent.futures import ThreadPoolExecutor
from math import inf
from time import time

from box.cluster.network import Server
from box.cluster.network import Serdes
from box.common.callclasses import callclass
from box.common.callclasses import respondedclass, is_respondedclass
from box.common.callclasses import respondingclass
from box.common.planes.control import Ping, Pong, Pang
from box.common.planes.control import ProcessorRegister, ProcessorRegisterResp
from box.common.planes.control import ProcessorRegistryPull, ProcessorRegistryPullResp
from box.common.planes.control import ProcessorRegistryPush
from box.common.planes.control import ResourceRegister, ResourceRegisterResp
from box.common.planes.control import ResourceRegistryPull, ResourceRegistryPullResp
from box.common.planes.control import ResourceRegistryPush
from box.common.resources import EmptyResource
from box.common.resources import address_to_host_port

from ._lut import LutNode
from ._proc import ProcDict



ADDRESS = "box://127.0.0.1:62222"
MAX_WORKERS = 32


serdes             : Serdes                = Serdes()
res_lut            : LutNode               = LutNode(EmptyResource(), inf)
proc_dict          : ProcDict              = ProcDict()

thread_pool         : ThreadPoolExecutor    = None
server              : Server                = None

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

def start():
    server.start()



## Ping

@serdes.register
@respondedclass
@Ping.impl
def Ping(self: Ping):
    pong = Pong.make_response(self, t0=self.t0)
    thread_pool.submit(pong)
    proc_dict.update(self.address, desc=self.desc, usage=self.usage)

@serdes.register
@respondedclass
@respondingclass(to=[Ping])
@Pong.impl
def Pong(self: Pong):
    self.do_respond()
    pang = self.get_response()
    rtt = 0.5 * (time() + pang.t2 - pang.t1 - pang.t0)
    proc_dict.update(self.address, rtt=rtt)

@serdes.register
@respondingclass(to=[Pong])
@Pang.impl
def Pang(self: Pang):
    self.do_respond()



## Processor

@serdes.register
@respondedclass
@ProcessorRegister.impl
def ProcessorRegister(self: ProcessorRegister):
    ack = proc_dict.insert(self.processor)
    resp = ProcessorRegisterResp.make_response(self, ack=ack)
    thread_pool.submit(resp)
    
@serdes.register
@respondingclass(to=[ProcessorRegister])
@ProcessorRegisterResp.impl
def ProcessorRegisterResp(self: ProcessorRegisterResp):
    self.do_respond()

@serdes.register
@respondedclass
@ProcessorRegistryPull.impl
def ProcessorRegistryPull(self: ProcessorRegistryPull):
    processors = [proc_dict.query(address) for address in self.addresses]
    ProcessorRegistryPullResp.make_response(self, processors=processors)

@serdes.register
@respondingclass(to=[ProcessorRegistryPull])
@ProcessorRegistryPullResp.impl
def ProcessorRegistryPullResp(self: ProcessorRegistryPullResp):
    self.do_respond()

@serdes.register
@callclass
@ProcessorRegistryPush.impl
def ProcessorRegistryPush(self: ProcessorRegistryPush):
    # for processor in self.processors:
    #     proc_dict.insert(processor)
    pass



# Resource

@serdes.register
@respondedclass
@ResourceRegister.impl
def ResourceRegister(self: ResourceRegister):
    acks = [res_lut.insert(res.path, res) for res in self.resources]
    ResourceRegisterResp.make_response(self, acks=acks)

@serdes.register
@respondingclass(to=[ResourceRegister])
@ResourceRegisterResp.impl
def ResourceRegisterResp(self: ResourceRegisterResp):
    self.do_respond()

@serdes.register
@respondedclass
@ResourceRegistryPull.impl
def ResourceRegistryPull(self: ResourceRegistryPull):
    resources = [res_lut.query(path)[-1] for path in self.paths]
    ResourceRegistryPullResp.make_response(self, resources=resources)

@serdes.register
@respondingclass(to=[ResourceRegistryPull])
@ResourceRegistryPullResp.impl
def ResourceRegistryPullResp(self: ResourceRegistryPullResp):
    self.do_respond()

@serdes.register
@respondedclass
@ResourceRegistryPush.impl
def ResourceRegistryPush(self: ResourceRegistryPush):
    pass
