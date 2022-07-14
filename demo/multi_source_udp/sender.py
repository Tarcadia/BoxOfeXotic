import random
import socket
import threading
import time

import config

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
server.bind(config.SERVER_ADDRESS);

queue = [];

def server_thread():
    while True:
        recv, addr = server.recvfrom(1500);
        info = recv.decode(config.ENCODING);
        queue.append([config.SEND_REPEAT, addr]);
        print("REQ FROM %s:%s >> %s" % (*addr, info));
        server.sendto(recv, addr);
        print("ECHO TO %s:%s" % addr);
        server.sendto(config.SEND_DATA, addr);
        print("SEND TO %s:%s FROM SERVER" % addr);

def sender_thread():
    sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
    addr = (config.SERVER_HOST, random.choice(config.SENDER_PORT_RANGE));
    try:
        sender.bind(addr);
        print("SENDER: %s:%s" % addr);
    except OSError as err:
        print("SENDER: NOT BOUND");
        return;
    while True:
        try:
            target = queue.pop(0);
        except IndexError as err:
            continue;
        sender.sendto(config.SEND_DATA, target[1]);
        print("SEND TO %s:%s FROM %s:%s" % (*target[1], *addr));
        target[0] -= 1;
        if (target[0] > 0):
            time.sleep(0.1);
            queue.append(target);

th_server = threading.Thread(target=server_thread);
th_server.start();
th_sender = [threading.Thread(target=sender_thread) for _ in range(config.SEND_PARALLEL)];
for th in th_sender:
    th.start();
