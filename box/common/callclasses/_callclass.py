

from dataclasses import dataclass, is_dataclass
from functools import wraps
from inspect import isgenerator, isgeneratorfunction
from typing import Callable


class _CallBase():
    def __callclass_init__(self, func: Callable, interface: dataclass) -> None:
        self.__callclass_func__ = func
        self.__callclass_interface__ = interface
        if self.__callclass_func__ and isgeneratorfunction(self.__callclass_func__):
            self.__callclass_generator__ = self.__callclass_func__(self)
        elif self.__callclass_func__:
            def __genfunc__():
                yield from tuple(self.__callclass_func__(self))
            self.__callclass_generator__ = __genfunc__()
        else:
            def __genfunc__():
                yield from ()
            self.__callclass_generator__ = __genfunc__()
    
    def __callclass_resp__(self, send = None) -> None:
        if isgenerator(self.__callclass_generator__):
            return self.__callclass_generator__.send(send)


def is_callclass(obj):
    cls = obj if isinstance(obj, type) else type(obj)
    return issubclass(cls, _CallBase)


def callclass(interface: dataclass):
    if not is_dataclass(interface):
        raise TypeError("Can only create call class from a dataclass interface.")
    def wrapper(func: Callable) -> type:
        def __post_init__(self):
            _CallBase.__callclass_init__(self, func, interface)
        _wrapped = type(
            interface.__name__,
            (interface, _CallBase),
            {
                "__post_init__": __post_init__,
                "__module__": func.__module__,
            },
        )
        return dataclass(_wrapped)
    return wrapper



def as_function(call: callclass):
    @wraps(call)
    def wrapped(*args, **kwargs):
        return next(call(*args, **kwargs))
    return wrapped
