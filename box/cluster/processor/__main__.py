

from concurrent.futures import ThreadPoolExecutor
from time import sleep

from ._controlcallside import init as controlcallside_init
from ._controlcallside import start as controlcallside_start



ADDRESS = "box://127.0.0.2:62222"
CONTROLLER_ADDRESS = "box://127.0.0.1:62222"
MAX_WORKERS = 64
thread_pool = ThreadPoolExecutor(max_workers=MAX_WORKERS)

controlcallside_init(CONTROLLER_ADDRESS, thread_pool)
controlcallside_start()

while True:
    sleep(60)