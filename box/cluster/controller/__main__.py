

from concurrent.futures import ThreadPoolExecutor
from time import sleep

from ._controlside import init as controlside_init
from ._controlside import start as controlside_start



MAX_WORKERS = 32
thread_pool = ThreadPoolExecutor(max_workers=MAX_WORKERS)

controlside_init("box://127.0.0.1:62222", thread_pool)
controlside_start()

while True:
    sleep(60)