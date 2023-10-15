

from dataclasses import dataclass
from socket import AF_INET, SOCK_STREAM, socket
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from typing import Any

from box.server.interface import serialize, deserialize, Sessions
from box.server.interface._serdes import ENCODING, LEN_BYTELEN, BYTEORDER

from box.server.interface.call import CallBase
from box.server.interface.call.control import Hello, HelloResp
from box.server.interface.call.control import AccessPull, AccessPush, AccessPushOff
from box.server.interface.call.control import Ping, Pong, Pang
from box.server.interface.call.control import CommandCall, CommandResp
from box.server.interface.call.p2c import RegistCall, RegistResp
from box.server.interface.call.p2c import SeekCall, SeekResp
from box.server.interface.call.p2c import LoggingCall


@dataclass
class Context():
    conn            : socket
    addr            : Any
    sessions        : Sessions


class Server():

    def __init__(self, host, port, max_users = 4, max_workers = 16) -> None:
        self._socket = socket(AF_INET, SOCK_STREAM)
        self._socket.bind((host, port))
        self._thread_pool = ThreadPoolExecutor(max_workers=max_workers)
        self._users = [Thread(target=self._user) for _ in range(max_users)]
        
    def _user(self):
        while True:
            conn, addr = self._socket.accept()
            ctx = Context(conn=conn, addr=addr, sessions=Sessions())
            try:
                while True:
                    _len = int.from_bytes(ctx.conn.recv(LEN_BYTELEN), BYTEORDER, signed=False)
                    _packet = ctx.conn.recv(_len)
                    _call = deserialize(_packet)
                    self._thread_pool.submit(_call, ctx)
            except Exception as e:
                continue

    def start(self):
        self._socket.listen()
        for _user in self._users:
            _user.start()


@HelloResp.onCall
@AccessPush.onCall
@AccessPushOff.onCall
@Pong.onCall
@RegistResp.onCall
@SeekResp.onCall
@CommandCall.onCall
def send(self: CallBase, ctx: Context):
    _packet = serialize(self)
    _len = len(_packet).to_bytes(LEN_BYTELEN, BYTEORDER, signed=False)
    ctx.conn.send(_len + _packet)


@Pang.onCall
@CommandResp.onCall
def resp(self: CallBase, ctx: Context):
    ctx.sessions.put(self.resp, self)
