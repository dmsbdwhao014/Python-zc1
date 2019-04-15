

# li = [11,22,33]
#
# ret = filter(lambda x:x>22,li)
#
# for line in ret:
#     print(line)

#
# def func():
#     yield 1
#     yield 2
#     yield 3
#
# ret = func()
#
# r1 = ret.__next__()
# print(r1)
#
# r2 = ret.__next__()
# print(r2)
#
# r3 = ret.__next__()
# print(r3)




def func1(args):
    n = 1
    while True:
        if n > args:
            return "more"
        yield n
        n += 1

r = func1(3)

for i in r:
    print(i)
