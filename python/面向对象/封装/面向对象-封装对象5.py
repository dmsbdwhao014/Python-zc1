class game:
    def __init__(self, name, age, weight):
        self.Name = name
        self.Age = age
        self.Weigh = weight

    def eat(self):
        self.Weigh = self.Weigh + 2

    def keepfitwith(self):
        self.Weigh = self.Weigh - 1


user = game('aaaa', 19, 100)
user.eat()
user.eat()
user.keepfitwith()
print(user.Weigh)
