class Person:
    def __init__(self):
        print("person")
        self.name = "jone"
        self.age = "24"


class son(Person):
    def __init__(self):
        print("son")
        self.From = "hunan"
        super(son, self).__init__()
        # Person.__init__(self)

# obj = son()
# print(obj.__dict__)
