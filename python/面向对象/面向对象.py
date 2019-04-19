class foo:
    def add(self, backend):
        print(backend, self)

    def remove(self, backed):
        print(backed, self)


obj1 = foo()
obj1.add("abc")
print(obj1)

obj2 = foo()
obj2.add("abc")
print(obj2)
