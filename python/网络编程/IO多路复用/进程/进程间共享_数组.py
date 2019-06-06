from multiprocessing import Process, Array


def FOO(i, temp):
    temp[i] = 100 + i
    for item in temp:
        print(i, "--->", item)


if __name__ == '__main__':
    temp = Array('i', [11, 22, 33, ])
    for i in range(3):
        P = Process(target=FOO, args=(i, temp,))
        P.start()
