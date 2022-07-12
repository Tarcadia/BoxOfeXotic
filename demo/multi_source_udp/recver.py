import random
import socket
import threading
import time

import config

recver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
addr = ('127.0.0.1', random.choice(range(30000, 40000)));
recver.bind(addr);

connect = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
connect.connect(config.SERVER_ADDRESS);
connect.send(addr[1].to_bytes(length=2, byteorder='big', signed=False));
connect.close();

recv_count = 0;
match_count = 0;
while recv_count < config.SEND_REPEAT:
    try:
        data, addr = recver.recvfrom(config.RECV_SIZE);
    except Exception as e:
        continue;
    match = (data == config.SEND_DATA);
    recv_count += 1;
    print("#%s %s:%s (%s)" % (recv_count, *addr, match));
    if not match:
        print(config.SEND_DATA.decode(config.ENCODING));
        print(data.decode(config.ENCODING));
    else:
        match_count += 1;

print("PASS");