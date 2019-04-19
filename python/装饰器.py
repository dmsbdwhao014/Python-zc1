
#
# def outer(func):
#     def inner():
#         print("log")
#         ret  = func()
#         print('after')
#         return ret
#     return inner()
#
#
# @outer
# def f1():
#     print("F1")


def outer(func):
    def inner(*args,**kwargs):
        print("开始")
        r = func(*args,**kwargs)
        print("结束")
        return r
    return inner

@outer
def a1(a,b):
    print(a,b)
    # return "AAAA"
