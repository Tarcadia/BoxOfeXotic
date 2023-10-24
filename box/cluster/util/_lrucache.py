

from threading import Lock


class LRUCache():

    SIZE = 1024

    def __init__(self, size=None) -> None:
        if not size is None:
            self.SIZE = size
        self._cache = {}
        self._lock = Lock()
    
    def put(self, key, value):
        with self._lock:
            self._cache.pop(key, None)
            self._cache[key] = value
            _keys = self._cache.keys
            for _idx in range(len(self._cache) - self.SIZE):
                self._cache.pop(_keys[_idx], None)
    
    def get(self, key):
        _ret = self._cache.get(key, None)
        if _ret is None:
            return _ret
        with self._lock:
            _ret = self._cache.pop(key, None)
            if _ret is None:
                return _ret
            self._cache[key] = _ret
        return _ret
    
    def die(self, key):
        with self._lock:
            _ret = self._cache.pop(key, None)
    