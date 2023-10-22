

from dataclasses import dataclass
from time import time



@dataclass
class Living():
    
    timestamp       : float
    ttl             : float

    def live(self):
        return self.timestamp + self.ttl
    
    def is_alive(self):
        return self.live() < time()