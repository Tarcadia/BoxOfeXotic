

from dataclasses import asdict
from json import loads as jloads
from json import dumps as jdumps

from box.server.interface.call import CallBase
from box.server.interface import call

ENCODING = "utf-8"

CALLS = [
    getattr(call, _key)
    for _key in dir(call)
    if isinstance(getattr(call, _key), type)
    and issubclass(getattr(call, _key), CallBase)
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
        _idx = int.from_bytes(serialized[ : IDX_BYTELEN], BYTEORDER, signed=False)
        _bytes = serialized[IDX_BYTELEN : ]
        return IDX2CALL[_idx](**jloads(_bytes.decode(ENCODING)))
    except Exception as e:
        raise DeserializeException(e)
