import contextlib
import queue
import threading
import time

StopEvent = object()


class ThreadPool(object):
    def __init__(self, max_num):
        # 队列
        self.q = queue.Queue()
        # 线程最大数
        self.max_num = max_num
        self.cancel = False
        self.terminal = False
        # 真实创建的线程
        self.generate_list = []
        # 空闲的线程
        self.free_list = []

    def run(self, fun, args, callback=None):

        if self.cancel:
            return
        if len(self.free_list) == 0 and len(self.generate_list) < self.max_num:
            self.generate_thread()
        w = (fun, args, callback,)
        self.q.put(w)

    def generate_thread(self):
        t = threading.Thread(target=self.call)
        t.start()

    def call(self):
        current_threading = threading.current_thread()
        self.generate_list.append(current_threading)

        event = self.q.get()
        while event != StopEvent:

            fun, args, callback = event
            try:
                result = fun(*args)
                success = True
            except Exception as e:
                success = False
                result = None

            if callback is not None:
                try:
                    callback(success, result)
                except Exception as e:
                    pass

            with  self.worker_state(self.free_list, current_threading):
                if self.terminal:
                    event = StopEvent
                else:
                    event = self.q.get()
        else:
            self.generate_list.remove(current_threading)

    def close(self):
        self.cancel = True
        full_size = len(self.generate_list)
        while full_size:
            self.q.put(StopEvent)
            full_size -= 1

    def terminate(self):
        self.terminal = True
        while self.generate_list:
            self.q.put(StopEvent)

        self.q.queue.clear()

    @contextlib.contextmanager
    def worker_state(self, state_list, worker_thread):
        state_list.append(worker_thread)
        try:
            yield
        finally:
            state_list.remove(worker_thread)


pool = ThreadPool(5)


def callback(status, result):
    pass


def action(i):
    print(i)


for i in range(10):
    ret = pool.run(action, (i,), callback)

time.sleep(2)

print(len(pool.generate_list), len(pool.free_list))
print(len(pool.generate_list), len(pool.free_list))

pool.terminal
