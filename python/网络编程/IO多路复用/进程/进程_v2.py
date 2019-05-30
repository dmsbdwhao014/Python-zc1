import multiprocessing

l1 = []


def do1(i):
    l1.append(i)
    print('say hi', l1)


if __name__ == "__main__":
    for i in range(10):
        p = multiprocessing.Process(target=do1, args=(i,))
        p.start()

        # print('end',l1)
