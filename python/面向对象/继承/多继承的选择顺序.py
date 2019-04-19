class Zxx:
    def z1(self):
        print("z1")

    def xxx(self):
        print("Zxx")


class Axx(Zxx):
    def a1(self):
        print("a1")

    def xxx(self):
        print("Axx")


class Bxx(Zxx):
    def b1(self):
        print("b1")

    def xxx(self):
        print("Bxx")


class Cxx(Axx):
    def c1(self):
        print("c1")

    def xxx(self):
        print("Cxx")


class Dxx(Bxx):
    def D1(self):
        print("D1")

    def xxx(self):
        print("Dxx")


class Exx(Cxx, Dxx):
    def E1(self):
        print("E1")

    def xxx(self):
        print("Exx")


obj = Exx()
obj.xxx()
