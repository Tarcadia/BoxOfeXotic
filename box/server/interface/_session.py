

from random import randint
from queue import Empty, Queue
from typing import Any


def session_id() -> int:
    return randint(0, 0xFFFFFFFFFFFFFFFF)



_sessions = {}

def session_get(session: int, block: bool = False, timeout: float = 0) -> Any:
    _q = Queue(1)
    _sessions[session] = _q
    try:
        _get = _q.get(block=block, timeout=timeout)
        return _get
    except Empty:
        return None
    finally:
        _sessions.pop(session)

def session_put(session: int, obj) -> None:
    _q = _sessions.get(session, None)
    if _q:
        _q.put(obj)
