import multiprocessing
import time


def do(a1):
    time.sleep(2)
    print(a1)


if __name__ == "__main__":
    t = multiprocessing.Process(target=do, args=(11,))
    t.daemon = True
    t.start()
    t.join(1)
    t1 = multiprocessing.Process(target=do, args=(22,))
    t1.daemon = True
    t1.start()
    print('end')
