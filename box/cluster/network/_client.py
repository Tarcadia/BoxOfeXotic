

from socket import create_connection, socket
from threading import Lock
from time import time

from box.common.resources import address_to_host_port


def access(address: str) -> socket:
    host, port = address_to_host_port(address)
    _conn = create_connection((host, port))
    return _conn


class Client():

    CONNECTION_LIFE = 5

    def __init__(self, connection_life = None) -> None:
        self._addr_time = {}
        self._addr_conn = {}
        self._lock = Lock()
        if not connection_life is None:
            self.CONNECTION_LIFE = connection_life
    
    def update(self):
        _living = time() - self.CONNECTION_LIFE
        _queue = self._addr_time.items()
        _idx = 0
        while _queue[_idx][1] < _living:
            _idx += 1
        _updating = [_queue[_idx][0] for _idx in range(_idx)]
        with self._lock:
            for _addr in _updating:
                if _addr in self._addr_time and self._addr_time[_addr] < _living:
                    _time = self._addr_time.pop(_addr)
                    _conn = self._addr_conn.pop(_addr)
                    _conn.close()
    
    def access(self, address):
        with self._lock:
            self._addr_time.pop(address, None)
            self._addr_time[address] = time()
            _conn = self._addr_conn.get(address, None)
            if _conn is None:
                _conn = access(address)
                self._addr_conn[address] = _conn
        return _conn

