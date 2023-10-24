

from concurrent.futures import ThreadPoolExecutor
from socket import create_connection, socket
from threading import Lock, Thread
from time import time

from box.common.resources import address_to_host_port



class Client():

    LEN_BYTELEN = 8
    BYTEORDER = "big"

    def __init__(self, address, thread_pool_workers=None, max_workers=32) -> None:
        self._address = address_to_host_port(address) if isinstance(address, str) else address
        self._socket = create_connection(self._address)
        self._thread_connection = Thread(target=self._run_connection, name=f"Client Connection")
        self._thread_pool_worker = (
            thread_pool_workers if not thread_pool_workers is None
            else ThreadPoolExecutor(max_workers=max_workers)
        )
        self._func_on_packet = None
        self._running = False

    def _run_connection(self):
        while self._running:
            try:
                _len = int.from_bytes(self._socket.recv(self.LEN_BYTELEN), self.BYTEORDER, signed=False)
                _packet = self._socket.recv(_len)
                if not self._func_run_connection is None:
                    self._thread_pool_worker.submit(self._run_on_packet, self._socket, self._addr, _packet)
            except Exception as e:
                self._run_on_packet.close()
                break

    def _run_on_packet(self, conn, addr, packet):
        _resp = self._func_run_connection(addr, packet)
        if _resp:
            _len = len(_resp).to_bytes(self.LEN_BYTELEN, self.BYTEORDER, signed=False)
            conn.send(_len + _resp)

    def on_packet(self, func):
        self._func_on_packet = func
        return func


    def start(self):
        self._running = True
        self._thread_connection.start()





class ClientPool():

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

