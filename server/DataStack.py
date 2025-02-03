import threading

class DataStack():
    def __init__(self):
        self.stack = []
        self.lock = threading.Lock()

    def push(self, item):
        with self.lock:
            self.data.append(item)

    def pop(self):
        with self.lock:
            return self.data.pop()

    def size(self):
        with self.lock:
            return len(self.data)

    def empty(self):
        with self.lock:
            return len(self.data) == 0

    def top(self):
        with self.lock:
            return self.data[-1]

    def clear(self):
        with self.lock:
            self.data = []

    def __str__(self):
        with self.lock:
            return str(self.data)