import threading
from queue import Queue


class FrameReader(threading.Thread):
    queues = []
    _running = True

    def __init__(self):
        threading.Thread.__init__(self)
        self.frame = None

    def run(self):
        while self.queues:
            queue = self.queues.pop()
            queue.put(self.frame)

    def addQueue(self, queue):
        self.queues.append(queue)

    def getFrame(self, timeout=None):
        queue = Queue(1)
        self.addQueue(queue)
        return queue.get(timeout=timeout)

    def stop(self):
        self._running = False
