import time
from multiprocessing import Process, Manager


def FOO(i, dic):
    dic[i] = 100 + i
    print(dic.values())


if __name__ == "__main__":
    manager = Manager()
    dic = manager.dict()
    # dic={}
    for i in range(2):
        P = Process(target=FOO, args=(i, dic))
        P.start()
        # P.join(1)
    # 等待主线程完成
    time.sleep(1)
