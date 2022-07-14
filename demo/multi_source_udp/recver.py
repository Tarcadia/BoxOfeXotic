import random
import socket

import config

recver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
addr = ('', random.choice(config.RECVER_PORT_RANGE));
recver.bind(addr);
recver.sendto("This is a test.".encode(config.ENCODING), config.SERVER_ADDRESS);

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