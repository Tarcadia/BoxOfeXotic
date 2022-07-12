import random
import socket
import threading
import time

import config

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
server.bind(config.SERVER_ADDRESS);
server.listen();

queue = [];

def server_thread():
    while True:
        connect, address = server.accept();
        recv = connect.recv(2);
        port = int.from_bytes(recv, byteorder='big', signed=False);
        queue.append([config.SEND_REPEAT, (address[0], port)]);
        print("START: %s:%s" % (address[0], port));
        connect.close();

def sender_thread():
    sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
    addr = (config.SENDER_HOST, random.choice(range(*config.SENDER_PORT_RANGE)));
    sender.bind(addr);
    while True:
        try:
            target = queue.pop(0);
        except IndexError as err:
            time.sleep(0.1);
            continue;
        sender.sendto(config.SEND_DATA, target[1]);
        print("SEND: %s:%s by %s:%s" % (*target[1], *addr));
        target[0] -= 1;
        if (target[0] > 0):
            queue.append(target);
        else:
            print("END: %s:%s" % target[1]);
        time.sleep(0.1);

th_server = threading.Thread(target=server_thread);
th_server.start();
th_sender = [threading.Thread(target=sender_thread) for _ in range(config.SEND_PARALLEL)];
for th in th_sender:
    th.start();
