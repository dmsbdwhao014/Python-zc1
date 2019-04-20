#!/usr/bin/env python
# -*- coding:utf-8 -*-

#
# inp = '34232sada'
# try:
#     num = int(inp)
#     print(num)
# except Exception as e:
#     print("数据转换失败，请重新输入")
#


class Anna:
    def __init__(self, args):
        self.name = args

    def __str__(self):
        return self.name


obj = Anna('cheng')
print(obj)

try:
    print("123")
    raise Exception("有问题")
except Exception as e:
    print(e)
else:
    pass
finally:
    pass
