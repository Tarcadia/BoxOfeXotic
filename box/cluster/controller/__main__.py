

from concurrent.futures import ThreadPoolExecutor
from socket import AF_INET, AF_INET6
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

from ._lut import LutNode
from ._proc import ProcDict



MAX_WORKERS = 32
NET_CONFS = [
    {
        "inet": AF_INET,
        "host": "127.0.0.1",
        "port": "62222",
    },
    {
        "inet": AF_INET6,
        "host": "::1",
        "port": "62222",
    },
]



thread_pool         = ThreadPoolExecutor(max_workers=MAX_WORKERS)
server4             = Server(**NET_CONFS[0], thread_pool_workers=thread_pool)
server6             = Server(**NET_CONFS[1], thread_pool_workers=thread_pool)
serdes              = Serdes()

res_lut             = LutNode(None, 0)
proc_dict           = ProcDict()



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



## Server

@server4.on_packet
@server6.on_packet
def on_packet(addr, packet):
    _obj = serdes.desirialize(packet)
    if is_respondedclass(_obj):
        _ret, _resp = _obj()
        return serdes.serialize(_resp)
    else:
        _ret = _obj()
        return

server4.start()
server6.start()

while True:
    pass