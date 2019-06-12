import queue
from multiprocessing import Process


def f(i, q):
    print(i, "===", q)


if __name__ == "__main__":
    q = queue.Queue(2)

    q.put("h1")
    q.put("h2")
    q.put("h3")

    for i in range(10):
        p = Process(target=f, args=(i, q,))
        p.start()
