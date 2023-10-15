

from random import randint
from queue import Empty, Queue
from typing import Any


def session_id() -> int:
    return randint(1, 0xFFFFFFFFFFFFFFFF)


class Sessions():

    def __init__(self, max_session = 0xFFFFFFFFFFFFFFFF) -> None:
        self._max_session = max_session
        self._sessions = {}

    def session_id(self) -> int:
        return randint(1, self._max_session)

    def get(self, session: int, block: bool = False, timeout: float = 0) -> Any:
        _q = Queue(1)
        self._sessions[session] = _q
        try:
            _get = _q.get(block=block, timeout=timeout)
            return _get
        except Empty:
            return None
        finally:
            self._sessions.pop(session)

    def put(self, session: int, obj) -> None:
        _q = self._sessions.get(session, None)
        if _q:
            _q.put(obj)
