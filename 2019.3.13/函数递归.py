
# def a():
#     return '123'
#
# def b():
#     r = a()
#     return r
#
# def c():
#     r = b()
#     return r
#
# def d():
#     r = c()
#     print(r)
#
#
# d()

#
# def func(n):
#     n += 1
#     if n >= 3:
#         return 'end'
#     return func(n)
#
# ret = func(1)
# print(ret)


# def think():
#     n = 1
#     m = 2
#     if n >= 10:
#         return 'end'
#     else:
#          m = n * m
#          n += 1
#          m += 1
#     return
#
# ret = think()
# print(ret)
#

def f1(num):
    if num == 1:
        return 1
    return num * f1(num-1)

print(f1(10))
print(1*2*3*4*5*6*7*8*9*10)
