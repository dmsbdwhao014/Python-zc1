class Person:
    def __init__(self):
        self.name = "jone"

    def show(self):
        print("show")


class son(Person):
    def __init__(self):
        self.name = "jone"

    def like(self):
        print("show")


obj = son()

print(obj.__dict__)
r = hasattr(obj, "show")
print(r)
