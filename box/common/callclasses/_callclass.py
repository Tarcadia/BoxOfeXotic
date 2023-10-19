

from dataclasses import dataclass, is_dataclass
from functools import wraps



_PARAM_FUNC = "__callclass_func__"

_PARAM_CLASSMETHOD_IMPL = "impl"
_PARAM_MAGIC__MODULE__ = "__module__"
_PARAM_MAGIC__CALL__ = "__call__"

def __callclass_impl(cls, func):
    setattr(cls, _PARAM_FUNC, func)
    return func

def __callclass_call(self):
    func = getattr(self, _PARAM_FUNC, None)
    if func:
        return func()


def _process_class(cls, func=None):
    if not is_dataclass(cls):
        cls = dataclass(cls)
    
    if not func is None:
        setattr(cls, _PARAM_FUNC, func)
    elif not hasattr(cls, _PARAM_FUNC):
        setattr(cls, _PARAM_FUNC, None)

    if not hasattr(cls, _PARAM_CLASSMETHOD_IMPL):
        setattr(cls, _PARAM_CLASSMETHOD_IMPL, classmethod(__callclass_impl))
    
    setattr(cls, _PARAM_MAGIC__CALL__, __callclass_call)
    
    return cls


def is_callclass(obj):
    cls = obj if isinstance(obj, type) else type(obj)
    return is_dataclass(cls) and hasattr(obj, _PARAM_FUNC)


def callclass(cls=None, func=None):
    def wrap(cls):
        return _process_class(cls, func)
    
    if cls is None:
        return wrap
    
    return wrap(cls)


def impl(cls):
    def wrap(func):
        if not func.__name__ == cls.__name__:
            raise SyntaxWarning("Suggested to create a callclass implementation with the same name of the base class.")
        wrapped = type(
            cls.__name__,
            (cls,),
            { _PARAM_MAGIC__MODULE__: func.__module__ }
        )
        return _process_class(wrapped, func)
    
    if not isinstance(cls, type) or not is_dataclass(cls):
        raise TypeError("Can only create callclass from a dataclass.")
    
    return wrap


def as_function(cls):
    @wraps(cls)
    def wrapped(*args, **kwargs):
        return cls(*args, **kwargs)()
    return wrapped

