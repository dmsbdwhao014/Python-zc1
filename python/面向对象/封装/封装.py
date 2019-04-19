# 封装
class foo:
    def add(self):
        print(self.backend)

    def remove(self):
        print(self.backend)


obj1 = foo()
obj1.backend = "abcdefg"
obj1.add()

obj2 = foo()
obj2.backend = "123456789"
obj2.add()
