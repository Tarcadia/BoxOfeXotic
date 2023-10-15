

from time import time
from box.server.interface.call import CallBase
from box.server.interface.call.control import Hello, HelloResp
from box.server.interface.call.control import AccessPull, AccessPush, AccessPushOff
from box.server.interface.call.control import Ping, Pong, Pang
from box.server.interface.call.control import CommandCall, CommandResp
from box.server.interface.call.p2c import RegistCall, RegistResp
from box.server.interface.call.p2c import SeekCall, SeekResp
from box.server.interface.call.p2c import LoggingCall

from ._network import Server, Context


processor_list = {}
resource_list = {}



@Hello.onCall
def hello(self: Hello, ctx: Context):
    _session = self.session
    _processor = self.processor
    _token = self.token
    _timestamp = self.timestamp
    _ttl = self.ttl
    processor_list[_processor] = (_token, _timestamp, _ttl)
    _resp = HelloResp(_session)
    _resp(ctx)



@AccessPull.onCall
def access_pull(self:AccessPull, ctx: Context):
    _processor = self.processor
    _access = processor_list.get(_processor, None)
    if _access:
        if time() < _access[1] + _access[2]:
            _resp = AccessPush(_processor, *_access)
        else:
            processor_list.pop(_processor, None)
            _resp = AccessPushOff(_processor)
    else:
        _resp = AccessPushOff(_processor)
    _resp(ctx)



@Ping.onCall
def pong(self: Ping, ctx: Context):
    _session = self.session
    _ping = self
    _pong = Pong(resp=_session)
    _pong(ctx)
    _pang = ctx.sessions.get(_pong.session)
    _t1 = time() - _pong.timestamp
    _t0 = _pang.timestamp - _ping.timestamp
    print("Usage: %.1f%%." % (100 * _ping.usage))
    print("RTT: %.3fms." % (1000 * 0.5 * (_t0 + _t1)))



## This is a bad implementation, it will lead to an overflow when the system runs long time.
## Need to reimplement a data structure for resource_list for faster, stable and converging calls.

@RegistCall.onCall
def regist(self: RegistCall, ctx: Context):
    _session = self.session
    entries_ack = []
    for _entry in self.entries:
        _res = _entry.resource
        _path = resource_list
        for _dir in [_dir for _dir in _res.split("/") if _dir and dir != "@"]:
            if _dir in _path:
                _path = _path[_dir]
            else:
                _path[_dir] = {}
                _path = _path[_dir]
        if not "@" in _path:
            _path["@"] = _entry
            entries_ack.append(True)
        elif "@" in _path and time() > _path["@"].timestamp + _path["@"].ttl:
            _path["@"] = _entry
            entries_ack.append(True)
        else:
            entries_ack.append(False)
    _resp = RegistResp(_session, entries_ack)
    _resp(ctx)

@SeekCall.onCall
def seek(self: SeekCall, ctx: Context):
    _session = self.session
    entries = []
    for _res in self.resources:
        _path = resource_list
        _entry = None
        if "@" in _path:
            if time() < _path["@"].timestamp + _path["@"].ttl:
                _entry = _path["@"]
            else:
                _path.pop("@", None)
        for _dir in [_dir for _dir in _res.split("/") if _dir and dir != "@"]:
            if _dir in _path:
                _path = _path[_dir]
                if "@" in _path:
                    if time() < _path["@"].timestamp + _path["@"].ttl:
                        _entry = _path["@"]
                    else:
                        _path.pop("@", None)
            else:
                break
        entries.append(_entry)
    _resp = SeekResp(_session, entries)
    _resp(ctx)



@LoggingCall.onCall
def logging(self: LoggingCall, ctx: Context):
    pass



server = Server("127.0.0.1", 62222)
server.start()


