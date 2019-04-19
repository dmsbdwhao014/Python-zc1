class nomar:
    def __init__(self, name):
        self.name = name

    def eat(self):
        print(self.name + " eat")

    def durink(self):
        print(self.name + " during")

    def sleep(self):
        print(self.name + " hart sleep")


class popel(nomar):
    def __init__(self, name):
        self.name = name

    def sleep(self):
        print(self.name + " like sleep")


obj = popel("xiaomi")
obj.eat()
obj.sleep()
obj1 = nomar("xi")
obj1.sleep()
