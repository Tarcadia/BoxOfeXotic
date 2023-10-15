

from dataclasses import asdict
from json import loads as jloads
from json import dumps as jdumps

from .call import CallBase
from .call import control
from .call import p2c
from .call import p2p


ENCODING = "utf-8"
CALLS = [
    control.Ping,
    control.Pong,
    control.Pang,
    control.Hello,
    control.HelloResp,
    control.AccessPull,
    control.AccessPush,
    control.AccessPushOff,
    control.CommandCall,
    control.CommandResp,
    p2c.RegistCall,
    p2c.RegistResp,
    p2c.SeekCall,
    p2c.SeekResp,
    p2c.LoggingCall,
    p2p.ResReadCall,
    p2p.ResReadResp,
    p2p.ResWriteCall,
    p2p.ResWriteResp,
    p2p.ResRpcCall,
    p2p.ResRpcrCall,
    p2p.ResRpcrResp,
    p2p.ResNackResp,
]

CALL2IDX = {CALLS[_idx] : _idx for _idx in range(len(CALLS))}
IDX2CALL = {_idx : CALLS[_idx] for _idx in range(len(CALLS))}

IDX_BYTELEN = 2
LEN_BYTELEN = 8
BYTEORDER = "big"


class SerializeException(Exception):
    pass


class DeserializeException(Exception):
    pass


def serialize(call: CallBase) -> bytes:
    try:
        _bytes = jdumps(asdict(call)).encode(ENCODING)
        _idx = CALL2IDX[call.__class__].to_bytes(IDX_BYTELEN, BYTEORDER, signed=False)
        return _idx + _bytes
    except Exception as e:
        raise SerializeException(e)


def deserialize(serialized: bytes) -> CallBase:
    try:
        _idx = int.from_bytes(serialized[LEN_BYTELEN : LEN_BYTELEN + IDX_BYTELEN], BYTEORDER, signed=False)
        _bytes = serialized[LEN_BYTELEN + IDX_BYTELEN : ]
        return IDX2CALL[_idx](**jloads(_bytes.decode(ENCODING)))
    except Exception as e:
        raise DeserializeException(e)
