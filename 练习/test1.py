import  time
class HiDecorate:
    def show_call_time(selfs,func,format):
        def wrap(*args,**kwargs):
            call_time=''
            if format=='y':
                call_time=time.strftime('%y-%m-%d',time.localtime())
            elif format=='Y':
                call_time = time.strftime('%y-%m', time.localtime())
            print(args[1])
            print('func name:{},args:{},call_time:{}'.format(func.__name__,args,call_time))
            func(*args)
        return wrap

    def info(self,format):
        def foo(func):
            print('format:', format)
            return self.show_call_time(func,format)
        return foo

decorate=HiDecorate()

@decorate.info('Y')
def f1(A,B,C):
    print('Hi Decorate')

f1(1,2,3)

















