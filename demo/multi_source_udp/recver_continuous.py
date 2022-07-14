import random
import socket
import time

import config

recver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
addr = ('', random.choice(config.RECVER_PORT_RANGE));
recver.bind(addr);

recv_count = 0;
match_count = 0;

while recv_count < config.SEND_REPEAT:
    time.sleep(0.33);
    recver.sendto("This is a test.".encode(config.ENCODING), config.SERVER_ADDRESS);
    try:
        data, addr = recver.recvfrom(config.RECV_SIZE);
    except ConnectionResetError as e:
        recver.close();
        recver.bind(addr);
        print("ERROR: CONNECTION RESET");
        continue;
    
    recv_count += 1;
    if data == config.SEND_DATA:
        print("#%s %s:%s MATCH" % (recv_count, *addr));
        match_count += 1;
    else:
        _l = len(data.decode(config.ENCODING));
        if _l > 100:
            _s = ("... CHARS LEN %s" % _l);
        else:
            _s = (data.decode(config.ENCODING));
        print("#%s %s:%s RECV >> %s" % (recv_count, *addr, _s));

print("MATCH %s / %s" % (match_count, recv_count));