

from concurrent.futures import ThreadPoolExecutor
from time import sleep

from ._controlcallside import init as controlcallside_init
from ._controlcallside import start as controlcallside_start
from ._controlcallside import register_processor, register_resource
from ._controlcallside import query_processor, query_resource
from ._controlcallside import ping



ADDRESS = "box://127.0.0.2:62222"
CONTROLLER_ADDRESS = "box://127.0.0.1:62222"
MAX_WORKERS = 64
thread_pool = ThreadPoolExecutor(max_workers=MAX_WORKERS)

controlcallside_init(CONTROLLER_ADDRESS, thread_pool)
controlcallside_start()

register_processor(ADDRESS, ttl=300)

while True:
    sleep(60)
    ping(ADDRESS)