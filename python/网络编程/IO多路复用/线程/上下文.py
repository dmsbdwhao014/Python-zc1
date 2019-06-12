import queue
from contextlib import contextmanager


@contextmanager
def work_stat(anna, belle):
    anna.append(belle)
    try:
        yield 123
    finally:
        anna.remove(belle)


q = queue.Queue()
q.put("xxxx")
li = [111, 23412]
with work_stat(li, 1) as f:
    print("before")
    print(f)
    q.get()

print("after")
