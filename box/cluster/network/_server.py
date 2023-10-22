

from concurrent.futures import ThreadPoolExecutor
from ipaddress import ip_address
from socket import SOCK_STREAM, socket
from threading import Thread


class Server():

    LEN_BYTELEN = 8
    BYTEORDER = "big"

    def __init__(self, inet, host, port, max_connections=16, thread_pool_workers=None, max_workers=32) -> None:
        if isinstance(address, str):
            address = ip_address(address)
        self._socket = socket(inet, SOCK_STREAM)
        self._socket.bind((host, port))
        self._max_connections = max_connections
        self._thread_pool_connection = []
        self._thread_pool_worker = (
            thread_pool_workers if not thread_pool_workers is None
            else ThreadPoolExecutor(max_workers=max_workers)
        )
        self._func_on_packet = None
        self._running = False
    
    def _run_connection(self):
        while self._running:
            conn, addr = self._socket.accept()
            try:
                while self._running:
                    _len = int.from_bytes(conn.recv(self.LEN_BYTELEN), self.BYTEORDER, signed=False)
                    _packet = conn.recv(_len)
                    if not self._func_run_connection is None:
                        self._thread_pool.submit(self._run_on_packet, conn, addr, _packet)
            except Exception as e:
                conn.close()
                continue

    def _run_on_packet(self, conn, addr, packet):
        _resp = self._func_run_connection(addr, packet)
        if _resp:
            _len = len(_resp).to_bytes(self.LEN_BYTELEN, self.BYTEORDER, signed=False)
            conn.send(_len + _resp)

    def on_packet(self, func):
        self._func_on_packet = func
        return func
    

    def start(self):
        self._socket.listen()
        self._running = True
        for _iconn in range(self._max_connections):
            _thread = Thread(target=self._run_connection, name=f"Server Connection #{_iconn}")
            self._thread_pool_connection.append(_thread)
            _thread.start()



