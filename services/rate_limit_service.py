
import time

class RateLimiter:
    def __init__(self,interval=1):
        self.interval=interval
        self.last=0

    def wait(self):
        now=time.time()
        if now-self.last<self.interval:
            time.sleep(self.interval-(now-self.last))
        self.last=time.time()
