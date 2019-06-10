import time
from multiprocessing import Pool


def f1(a):
    time.sleep(1)
    print(a)
    return 111


def f2(a):
    print(a)


if __name__ == '__main__':
    pool = Pool(5)
    for i in range(40):
        # pool.apply_asnyc(func=f1,args=(i,),callback=f2)
        pool.apply(func=f1, args=(i,))
        print("==========")
    pool.close()
    pool.join()
