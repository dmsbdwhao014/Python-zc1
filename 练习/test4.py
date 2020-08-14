def Work(args1,args2):

    class foo:
        def __init__(self,args1,args2):
            self.para1=args1
            self.para2=args2
        def run2(self):
            print(self.para1,self.para2)
        def run1(self,args1):
            print(args1)

    A = foo(1,2)
    print(A)



RUN = Work(1,2)
