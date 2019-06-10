import queue
import threading
import time


class ThreadPool(object):
    def __init__(self, max_num=20):
        self.queue = queue.Queue(max_num)
        for i in range(max_num):
            self.queue.put(threading.Thread)

    def get_thread(self):
        return self.queue.get()

    def add_thread(self):
        self.queue.put(threading.Thread)


def func(pool, a):
    time.sleep(1)
    print("=" * 10)
    print(a)
    print("=" * 10)
    pool.add_thread()


p = ThreadPool()

if __name__ == "__main__":
    for i in range(10):
        thread = p.get_thread()
        t = thread(target=func, args=(p, i,))
        t.start()
