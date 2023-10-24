

from concurrent.futures import ThreadPoolExecutor
from math import nan
from time import time
from typing import List

from box.cluster.network import Serdes
from box.cluster.network import Client
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
from box.common.resources import Processor, Resource
from box.common.resources import is_null_url, BOX_NULL_URL
from box.common.resources import url_to_host_port_path, get_address

from box.cluster.util import LRUCache



CONTROLLER_ADDRESS = "box://127.0.0.1:62222"
MAX_WORKERS = 64
MAX_RES_CACHE = 1024
MAX_PROC_CACHE = 1024


serdes              : Serdes                = Serdes()
res_cache           : LRUCache              = LRUCache(size=MAX_RES_CACHE)
proc_cache          : LRUCache              = LRUCache(size=MAX_PROC_CACHE)

thread_pool         : ThreadPoolExecutor    = None
controller_client   : Client                = None
_initialized        : bool                  = False

def _on_packet(addr, packet):
    _obj = serdes.desirialize(packet)
    _obj()

def init(address = CONTROLLER_ADDRESS, _thread_pool = None, _max_workers=MAX_WORKERS):
    global thread_pool
    global controller_client
    thread_pool = (
        ThreadPoolExecutor(max_workers=_max_workers)
        if _thread_pool is None
        else _thread_pool
    )
    controller_client = Client(address, thread_pool_workers=thread_pool)
    controller_client.on_packet(_on_packet)

    global _initialized
    _initialized = True

def start():
    if _initialized:
        controller_client.start()
    else:
        raise RuntimeError("Module not initialized, call init() to initialize.")



## Ping

@serdes.register
@respondedclass
@Ping.impl
def Ping(self: Ping):
    controller_client.send(
        serdes.serialize(self)
    )

@serdes.register
@respondedclass
@respondingclass(to=[Ping])
@Pong.impl
def Pong(self: Pong):
    self.do_respond()
    pang = Pang.make_response(self, address=self.address, t0=self.t0, t1=self.t1)
    thread_pool.submit(pang)

@serdes.register
@respondingclass(to=[Pong])
@Pang.impl
def Pang(self: Pang):
    self.do_respond()
    controller_client.send(
        serdes.serialize(self)
    )



## Processor

@serdes.register
@respondedclass
@ProcessorRegister.impl
def ProcessorRegister(self: ProcessorRegister):
    controller_client.send(
        serdes.serialize(self)
    )
    
@serdes.register
@respondingclass(to=[ProcessorRegister])
@ProcessorRegisterResp.impl
def ProcessorRegisterResp(self: ProcessorRegisterResp):
    self.do_respond()
    return self.ack

@serdes.register
@respondedclass
@ProcessorRegistryPull.impl
def ProcessorRegistryPull(self: ProcessorRegistryPull):
    controller_client.send(
        serdes.serialize(self)
    )

@serdes.register
@respondingclass(to=[ProcessorRegistryPull])
@ProcessorRegistryPullResp.impl
def ProcessorRegistryPullResp(self: ProcessorRegistryPullResp):
    self.do_respond()
    for address, processor in self.processors.items():
        if is_null_url(processor.address):
            processor.address = BOX_NULL_URL
        if not is_null_url(address):
            proc_cache.put(address, processor)

@serdes.register
@callclass
@ProcessorRegistryPush.impl
def ProcessorRegistryPush(self: ProcessorRegistryPush):
    for processor in self.processors:
        if is_null_url(processor.address):
            processor.address = BOX_NULL_URL
        if not is_null_url(processor.address):
            proc_cache.put(processor.address, processor)



# Resource

@serdes.register
@respondedclass
@ResourceRegister.impl
def ResourceRegister(self: ResourceRegister):
    controller_client.send(
        serdes.serialize(self)
    )

@serdes.register
@respondingclass(to=[ResourceRegister])
@ResourceRegisterResp.impl
def ResourceRegisterResp(self: ResourceRegisterResp):
    self.do_respond()
    return all(self.acks)

@serdes.register
@respondedclass
@ResourceRegistryPull.impl
def ResourceRegistryPull(self: ResourceRegistryPull):
    controller_client.send(
        serdes.serialize(self)
    )

@serdes.register
@respondingclass(to=[ResourceRegistryPull])
@ResourceRegistryPullResp.impl
def ResourceRegistryPullResp(self: ResourceRegistryPullResp):
    self.do_respond()
    for path, resource in self.resources.items():
        if resource.path == "":
            resource.path = "/"
        if path == "":
            path = "/"
        res_cache.put(path, resource)

@serdes.register
@respondedclass
@ResourceRegistryPush.impl
def ResourceRegistryPush(self: ResourceRegistryPush):
    for resource in self.resources:
        if resource.path == "":
            resource.path = "/"
        res_cache.put(resource.path, resource)



def register_processor(address: str, token: str = "", desc: str = "", usage: float = nan, ttl: float = 5):
    _processor = Processor(timestamp=time(), ttl=ttl, address=address, token=token, desc=desc, usage=usage)
    _call = ProcessorRegister(_processor)
    _resp, _ret = _call()
    return _ret

def register_resource(address: str, paths: List[str], ttl: float = 5):
    _resources = []
    if is_null_url(address):
        raise ValueError("Cannot accept a null address.")
    for _path in paths:
        if not _path:
            _path = "/"
        _resources.append(Resource(path=_path, owner=address, ttl=ttl))
    _call = ResourceRegister(resources=_resources)
    _resp, _ret = _call()
    return _ret

def ping(address: str, desc: str = "", usage: float = nan):
    _call = Ping(address=address, desc=desc, usage=usage)
    _pong, _ret = _call()
    if _pong is None:
        return None
    _rtt = (time() - _pong.t0)
    return _rtt

def query_processor(address: str):
    pass

def query_resource(path: str):
    pass

