

from typing import Any


class Call():

    _callback = None

    @classmethod
    def onCall(cls, callback: callable):
        cls._callback = callback
        return callback

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        if self.__class__._callback:
            return self.__class__._callback(self, *args, **kwds)
