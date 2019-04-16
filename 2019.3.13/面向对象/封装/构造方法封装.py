# 构造方法封装
class foo:
    def __init__(self, bk):
        self.backend = bk

    def add(self):
        print(self.backend)


obj = foo("abcd")
obj.add()
obj1 = foo("12345")
obj1.add()
