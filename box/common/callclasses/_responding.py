

from dataclasses import dataclass, is_dataclass, make_dataclass
from ._callclass import callclass, is_callclass
from ._responded import is_respondedclass

from ._callclass import _PARAM_MAGIC__MODULE__
from ._responded import _PARAM_RESPONSES, _PARAM_RESP_SESSION
from ._responded import _PARAM_FIELD_SESSION_TYPE



_PARAM_RESPOND_TO = "__callclass_respond_to__"
_PARAM_RESP_RSESSION = "__callclass_resp_rsession__"

_PARAM_FIELD_RSESSION = "session_resp"
_PARAM_FIELD_RSESSION_TYPE = _PARAM_FIELD_SESSION_TYPE
_PARAM_METHOD_RESPONDING = "responding"
_PARAM_METHOD_DORESPOND = "do_respond"
_PARAM_CLASSMETHOD_MAKERESPONSE = "make_response"

def __callclass_makeresponse(cls, obj, *args, **kwargs):
    if not type(obj) in getattr(cls, _PARAM_RESPOND_TO):
        raise ValueError("Can only respond to a responded class.")
    return cls(
        *args, **kwargs,
        **{
            getattr(cls, _PARAM_RESP_RSESSION):
            getattr(obj, getattr(obj, _PARAM_RESP_SESSION))
        }
    )

def __callclass_dorespond(self):
    _rsession_field = getattr(self, _PARAM_RESP_RSESSION, _PARAM_FIELD_RSESSION)
    _rsession = getattr(self, _rsession_field)
    _responding = getattr(self, _PARAM_RESPOND_TO)
    for _iresponding in _responding:
        _responses = getattr(_iresponding, _PARAM_RESPONSES)
        _queue = _responses.get(_rsession, None)
        if _queue is None:
            continue
        _queue.put_nowait(self)

def __callclass_regresponding(obj, responded):
    if not is_respondedclass(responded):
        raise ValueError("Can only respond to a responded class.")
    _respond_to = getattr(obj, _PARAM_RESPOND_TO)
    setattr(obj, _PARAM_RESPOND_TO, [*_respond_to, responded])


def _process_class(cls,
    to=None,
    rsession=None,
    rsession_type=None,
    func=__callclass_dorespond,
):
    _rsession = rsession if not rsession is None else _PARAM_FIELD_RSESSION
    _rsession_type = rsession_type if not rsession_type is None else _PARAM_FIELD_RSESSION_TYPE
    
    cls = dataclass(cls)
    cls = make_dataclass(cls.__name__, 
        fields=[(_rsession, _rsession_type, None)],
        bases=(cls,),
        module=cls.__module__,
    )
    
    cls = callclass(cls, func)

    if not to is None:
        setattr(cls, _PARAM_RESPOND_TO, to)
    elif not hasattr(cls, _PARAM_RESPOND_TO):
        setattr(cls, _PARAM_RESPOND_TO, [])

    if not rsession is None:
        setattr(cls, _PARAM_RESP_RSESSION, rsession)
    elif not hasattr(cls, _PARAM_RESP_RSESSION):
        setattr(cls, _PARAM_RESP_RSESSION, _PARAM_FIELD_RSESSION)
    
    setattr(cls, _PARAM_METHOD_RESPONDING,
        lambda self=None, responded=None: (
            __callclass_regresponding(cls, responded)
            if self is None
            else __callclass_regresponding(self, responded)
        )
    )

    setattr(cls, _PARAM_METHOD_DORESPOND, __callclass_dorespond)
    setattr(cls, _PARAM_CLASSMETHOD_MAKERESPONSE, classmethod(__callclass_makeresponse))

    return cls


def is_respondingclass(obj):
    cls = obj if isinstance(obj, type) else type(obj)
    return is_callclass(cls) and hasattr(obj, _PARAM_RESPOND_TO)


def respondingclass(to,
    rsession=None,
    rsession_type=None,
    func=__callclass_dorespond,
):
    def wrap(cls):
        return _process_class(cls, to, rsession, rsession_type, func)
    
    return wrap

def responding(cls, to):
    def wrap(func):
        if not func.__name__ == cls.__name__:
            raise SyntaxWarning("Suggested to create a callclass implementation with the same name of the base class.")
        wrapped = type.new_class(
            cls.__name__,
            (cls),
            { _PARAM_MAGIC__MODULE__: func.__module__ }
        )
        return _process_class(wrapped, to=to, func=func)
    
    if not isinstance(cls, type) or not is_dataclass(cls):
        raise TypeError("Can only create callclass from a dataclass.")
    
    return wrap(cls)

@respondingclass(to=[])
class Responding:
    pass

