import time


class Timer:
    def __init__(self):
        self.now = time.time()
        self.last = self.now

    def __call__(self, title=''):
        print(title, f'{next(self):.3f}s')

    def __next__(self):
        self.last = self.now
        self.now = time.time()
        return self.now - self.last
