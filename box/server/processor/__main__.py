

from dataclasses import dataclass
from itertools import repeat
from socket import AF_INET, SOCK_STREAM, socket
from concurrent.futures import ThreadPoolExecutor
from time import sleep
from typing import Any

from box.server.interface.serdes import serialize, deserialize
from box.server.interface.serdes import LEN_BYTELEN, BYTEORDER
from box.server.interface.call import CallBase, Ping, Pong, Pang
from box.server.interface.call import Sessions

@dataclass
class Context():
    conn            : socket
    addr            : Any
    sessions        : Sessions

socket = socket(AF_INET, SOCK_STREAM)
sessions = Sessions()
context = Context(conn=socket, addr=None, sessions=sessions)
thread_pool = ThreadPoolExecutor(max_workers=16)

@Ping.onCall
@Pang.onCall
def send(self: CallBase):
    _packet = serialize(self)
    _len = len(_packet).to_bytes(LEN_BYTELEN, BYTEORDER, signed=False)
    socket.send(_len + _packet)

@Pong.onCall
def pong(self: Pong, ctx):
    _pang = Pang(self.session)
    _pang()
    print("Pong!")

socket.connect(("127.0.0.1", 62222))
result = thread_pool.submit(
    lambda : [
        thread_pool.submit(
            deserialize(
                context.conn.recv(
                    int.from_bytes(
                        context.conn.recv(LEN_BYTELEN),
                        BYTEORDER,
                        signed=False
                    )
                )
            ),
            context
        )
        for _ in repeat(None)
    ]
)

sleep(1)
Ping(usage=0.1)()
sleep(1)
Ping(usage=0.2)()
sleep(1)
Ping(usage=0.3)()
sleep(3)
