class normal:
    def __init__(self, name):
        self.name = name

    def eat(self):
        print(self.name + " eat")

    def durink(self):
        print(self.name + " during")

    def sleep(self):
        print(self.name + " hart sleep")

class like:
    def lookbook(self):
        print("like look book")

    def singlesong(self):
        print("like singlesong")

    def sleep(self):
        print(self.name + " like sleep")


class popel(normal,like):
    def __init__(self, name):
        self.name = name

    def sleep(self):
        print(self.name + " like sleep")


obj = popel("xiaomi")
obj.eat()
obj.sleep()
obj.singlesong()
