

from concurrent.futures import ThreadPoolExecutor
from socket import create_connection, socket
from threading import Lock, Thread
from time import time

from box.common.resources import address_to_host_port, get_address



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
            except TimeoutError:
                continue
            except Exception as e:
                self._run_on_packet.close()
                break

    def _run_on_packet(self, conn, addr, packet):
        _resp = self._func_run_connection(addr, packet)
        if _resp:
            _len = len(_resp).to_bytes(self.LEN_BYTELEN, self.BYTEORDER, signed=False)
            conn.send(_len + _resp)

    def send(self, bytes):
        _len = len(bytes).to_bytes(self.LEN_BYTELEN, self.BYTEORDER, signed=False)
        self._socket.send(_len + bytes)

    def on_packet(self, func):
        self._func_on_packet = func
        return func


    def start(self):
        self._running = True
        self._thread_connection.start()
    
    def stop(self):
        self._running = False
        self._socket.close()



class ClientPool():

    LEN_BYTELEN = 8
    BYTEORDER = "big"
    TTL = 10
    LRU = 32
    UPDATE_MAX_WORKERS = 4
    THREAD_POOL_UPDATE = ThreadPoolExecutor(max_workers=UPDATE_MAX_WORKERS)

    def __init__(self, thread_pool_workers=None, max_workers=32, _ttl = None, _lru = None) -> None:
        self._addr2time = {}
        self._addr2conn = {}
        self._addr2thread = {}
        self._lock = Lock()

        self._thread_pool_worker = (
            thread_pool_workers if not thread_pool_workers is None
            else ThreadPoolExecutor(max_workers=max_workers)
        )
        self._func_on_packet = None

        if not _ttl is None:
            self.TTL = _ttl
        if not _lru is None:
            self.LRU = _lru
    
    def _run_connection(self, conn, addr):
        while self._running:
            try:
                _len = int.from_bytes(conn.recv(self.LEN_BYTELEN), self.BYTEORDER, signed=False)
                _packet = conn.recv(_len)
                if not self._func_run_connection is None:
                    self._thread_pool_worker.submit(self._run_on_packet, conn, addr, _packet)
            except TimeoutError:
                continue
            except Exception as e:
                conn.close()
                break
        self._kill(get_address(*addr))

    def _run_on_packet(self, conn, addr, packet):
        _resp = self._func_run_connection(addr, packet)
        if _resp:
            _len = len(_resp).to_bytes(self.LEN_BYTELEN, self.BYTEORDER, signed=False)
            conn.send(_len + _resp)

    def _update(self):
        _living = time() - self.TTL
        _queue = self._addr2time.items()
        _idx = max(len(_queue) - self.LRU, 0)
        while _queue[_idx][1] < _living:
            _idx += 1
        _updating = [_queue[_idx][0] for _idx in range(_idx)]
        with self._lock:
            for _addr in _updating:
                if _addr in self._addr2time and self._addr2time[_addr] < _living:
                    _time = self._addr2time.pop(_addr)
                    _conn = self._addr2conn.pop(_addr)
                    _thread = self._addr2thread.pop(_addr)
                    _conn.stop()
    
    def _access(self, address: str):
        with self._lock:
            self._addr2time.pop(address, None)
            self._addr2time[address] = time()
            _conn = self._addr2conn.get(address, None)
            if _conn is None:
                _conn = create_connection(*address_to_host_port(address))
                _thread = Thread(
                    target=self._run_connection,
                    name=f"Client Connection @{address}",
                    args=(_conn, address_to_host_port(address))
                )
                self._addr2conn[address] = _conn
                self._addr2thread[address] = _thread
                _thread.start()
        ClientPool.THREAD_POOL_UPDATE.submit(self._update)
        return _conn

    def _kill(self, address: str):
        with self._lock:
            _time = self._addr2time.pop(address, None)
            _conn = self._addr2conn.pop(address, None)
            _thread = self._addr2thread.pop(address, None)
            if not _conn is None:
                _conn.stop()


    def send(self, address: str, bytes: bytes):
        _c = self._access(address)
        _len = len(bytes).to_bytes(self.LEN_BYTELEN, self.BYTEORDER, signed=False)
        _c.send(_len + bytes)

    def on_packet(self, func):
        self._func_on_packet = func
        return func


    def start(self):
        self._running = True

    def stop(self):
        self._running = False

