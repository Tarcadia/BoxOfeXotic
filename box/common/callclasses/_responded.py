

from dataclasses import dataclass, field, is_dataclass, make_dataclass
from functools import wraps
from queue import Empty, Queue
from random import randrange

from ._callclass import callclass, is_callclass, impl
from ._callclass import _PARAM_FUNC, _PARAM_MAGIC__CALL__



_PARAM_RESPONSES = "__callclass_responses__"
_PARAM_RESP_SESSION = "__callclass_resp_session__"
_PARAM_RESP_BLOCK = "__callclass_resp_block__"
_PARAM_RESP_TIMEOUT = "__callclass_resp_timeout__"
_PARAM_RESP_FUNC_RESPONSE_CONTEXT = "__callclass_resp_func_response_context__"
_PARAM_RESP_FUNC_RESPONSE_GET = "__callclass_resp_func_response_get__"
_PARAM_RESP_FUNC_MAKESESSION = "__callclass_resp_func_makesession__"
_PARAM_RESP_CONTEXT_CLASS = "__callclass_resp_context_class__"

_PARAM_RESP_BLOCK_DEFAULT = True
_PARAM_RESP_TIMEOUT_DEFAULT = 3

_PARAM_FIELD_SESSION = "session_call"
_PARAM_FIELD_SESSION_TYPE = int
_PARAM_METHOD_RESPONSE_CONTEXT = "response_context"
_PARAM_METHOD_RESPONSE_GET = "get_response"
_PARAM_METHOD_MAKESESSION = "make_session"
_PARAM_METHOD_SETBLOCK = "set_block"
_PARAM_METHOD_SETTIMEOUT = "set_timeout"

_PARAM_MAGIC__ENTER__ = "__enter__"
_PARAM_MAGIC__EXIT__ = "__exit__"

def __callclass_responded_call(self, session=None, default=None):
    self_response_context = getattr(self, _PARAM_METHOD_RESPONSE_CONTEXT)
    self_response_get = getattr(self, _PARAM_METHOD_RESPONSE_GET)
    func = getattr(self, _PARAM_FUNC, None)
    with self_response_context(session) as context:
        _ret = None
        if func:
            _ret = func()
        return _ret, self_response_get(session, default=default)

def __callclass_response_context(obj, session=None):
    _session_field = getattr(obj, _PARAM_RESP_SESSION, _PARAM_FIELD_SESSION)
    _session = session if isinstance(obj, type) else getattr(obj, _session_field, None)
    if _session is None:
        raise ValueError("Session not specified.")
    _responses = getattr(obj, _PARAM_RESPONSES)

    def __enter__(self):
        _responses[_session] = self
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        _responses.pop(_session)

    _ContextClass = type(_PARAM_RESP_CONTEXT_CLASS, (Queue,), {
        _PARAM_MAGIC__ENTER__: __enter__,
        _PARAM_MAGIC__EXIT__: __exit__,
    })
    
    return _ContextClass()
    

def __callclass_response_get(obj, session=None, default=None):
    _session_field = getattr(obj, _PARAM_RESP_SESSION, _PARAM_FIELD_SESSION)
    _session = session if isinstance(obj, type) else getattr(obj, _session_field, None)
    if _session is None:
        raise ValueError("Session not specified.")
    _responses = getattr(obj, _PARAM_RESPONSES)
    _queue = _responses[_session]
    try:
        _resp = _queue.get(
            block=getattr(obj, _PARAM_RESP_BLOCK, _PARAM_RESP_BLOCK_DEFAULT),
            timeout=getattr(obj, _PARAM_RESP_TIMEOUT, _PARAM_RESP_TIMEOUT_DEFAULT),
        )
    except Empty:
        _resp = default
    return _resp

def __callclass_makesession(obj):
    _session = randrange(0, 65535)
    if not obj is None:
        _session_field = getattr(obj, _PARAM_RESP_SESSION, _PARAM_FIELD_SESSION)
        setattr(obj, _session_field, _session)
    return _session

def __callclass_setblock(obj, block):
    setattr(obj, _PARAM_RESP_BLOCK, block)

def __callclass_settimeout(obj, timeout):
    setattr(obj, _PARAM_RESP_TIMEOUT, timeout)


def _process_class(cls,
    session=None,
    session_type=None,
    block = None,
    timeout = None,
    func_response_context=None,
    func_response_get=None,
    func_make_session=None,
):
    _session = session if not session is None else _PARAM_FIELD_SESSION
    _session_type = session_type if not session_type is None else _PARAM_FIELD_SESSION_TYPE
    
    cls = dataclass(cls)
    cls = make_dataclass(
        cls.__name__,
        fields=[
            (_session, _session_type, field(default_factory=lambda:getattr(cls, _PARAM_METHOD_MAKESESSION)()))
        ],
        bases=(cls,),
        module=cls.__module__,
    )

    cls = callclass(cls, None)

    setattr(cls, _PARAM_RESPONSES, {})
    
    if not session is None:
        setattr(cls, _PARAM_RESP_SESSION, session)
    elif not hasattr(cls, _PARAM_RESP_SESSION):
        setattr(cls, _PARAM_RESP_SESSION, _PARAM_FIELD_SESSION)

    if not block is None:
        setattr(cls, _PARAM_RESP_BLOCK, block)
    elif not hasattr(cls, _PARAM_RESP_BLOCK):
        setattr(cls, _PARAM_RESP_BLOCK, _PARAM_RESP_BLOCK_DEFAULT)
    
    if not timeout is None:
        setattr(cls, _PARAM_RESP_TIMEOUT, block)
    elif not hasattr(cls, _PARAM_RESP_TIMEOUT):
        setattr(cls, _PARAM_RESP_TIMEOUT, _PARAM_RESP_TIMEOUT_DEFAULT)
    
    if not func_response_context is None:
        setattr(cls, _PARAM_RESP_FUNC_RESPONSE_CONTEXT, func_response_context)
    elif not hasattr(cls, _PARAM_RESP_FUNC_RESPONSE_CONTEXT):
        setattr(cls, _PARAM_RESP_FUNC_RESPONSE_CONTEXT, __callclass_response_context)
    
    if not func_response_get is None:
        setattr(cls, _PARAM_RESP_FUNC_RESPONSE_GET, func_response_get)
    elif not hasattr(cls, _PARAM_RESP_FUNC_RESPONSE_GET):
        setattr(cls, _PARAM_RESP_FUNC_RESPONSE_GET, __callclass_response_get)
    
    if not func_make_session is None:
        setattr(cls, _PARAM_RESP_FUNC_MAKESESSION, func_make_session)
    elif not hasattr(cls, _PARAM_RESP_FUNC_MAKESESSION):
        setattr(cls, _PARAM_RESP_FUNC_MAKESESSION, __callclass_makesession)
    
    setattr(cls, _PARAM_METHOD_RESPONSE_CONTEXT,
        lambda self=None, session=None: (
            getattr(cls, _PARAM_RESP_FUNC_RESPONSE_CONTEXT)(cls, session)
            if self is None
            else getattr(cls, _PARAM_RESP_FUNC_RESPONSE_CONTEXT)(self, session)
        )
    )
    
    setattr(cls, _PARAM_METHOD_RESPONSE_GET,
        lambda self=None, session=None, default=None: (
            getattr(cls, _PARAM_RESP_FUNC_RESPONSE_GET)(cls, session, default)
            if self is None
            else getattr(cls, _PARAM_RESP_FUNC_RESPONSE_GET)(self, session, default)
        )
    )
    
    setattr(cls, _PARAM_METHOD_MAKESESSION,
        lambda self=None: getattr(cls, _PARAM_RESP_FUNC_MAKESESSION)(self)
    )
    
    setattr(cls, _PARAM_METHOD_SETBLOCK,
        lambda self=None: (
            __callclass_setblock(cls)
            if self is None
            else __callclass_setblock(self)
        )
    )

    setattr(cls, _PARAM_METHOD_SETTIMEOUT,
        lambda self=None: (
            __callclass_settimeout(cls)
            if self is None
            else __callclass_settimeout(self)
        )
    )

    setattr(cls, _PARAM_MAGIC__CALL__, __callclass_responded_call)
    
    return cls


def is_respondedclass(obj):
    cls = obj if isinstance(obj, type) else type(obj)
    return is_callclass(cls) and hasattr(obj, _PARAM_RESPONSES)


def respondedclass(cls=None,
    session=None,
    session_type=None,
    block = None,
    timeout = None,
    func_response_context=None,
    func_response_get=None,
    func_make_session=None,
):
    def wrap(cls):
        return _process_class(cls,
            session,
            session_type,
            block,
            timeout,
            func_response_context,
            func_response_get,
            func_make_session,
        )
    
    if cls is None:
        return wrap
    
    return wrap(cls)

def respondedimpl(cls):
    def wrap(func):
        return respondedclass(impl(cls)(func))
    return wrap

@respondedclass
class Responded:
    pass

