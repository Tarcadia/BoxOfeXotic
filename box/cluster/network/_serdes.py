

from dataclasses import asdict
from json import loads as jloads
from json import dumps as jdumps


class Serdes():

    ENCODING = "utf-8"

    def __init__(self, encoding=None) -> None:
        self.classes = {}
        if not encoding is None:
            self.ENCODING = encoding

    def register(self, cls):
        self.classes[cls.__name__] = cls
        return cls
    
    def deregister(self, cls):
        name = cls.__name__ if isinstance(cls, type) else cls
        self.classes.pop(name, None)
        return cls
    
    def serialize(self, obj):
        try:
            _cls, _obj = obj.__class__.__name__, asdict(obj)
            _data = jdumps([_cls, _obj]).encode(self.ENCODING)
            return _data
        except Exception as e:
            raise SerializeException(e)
    
    def desirialize(self, bytes):
        try:
            _data = bytes.decode(self.ENCODING)
            _cls, _obj = jloads(_data)
            return self.classes[_cls](**_obj)
        except Exception as e:
            raise DeserializeException(e)


class SerdesException(Exception):
    pass


class SerializeException(SerdesException):
    pass


class DeserializeException(SerdesException):
    pass
