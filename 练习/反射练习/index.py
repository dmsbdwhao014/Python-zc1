def run():
    inp = input("打开页面:")
    modules,functions = inp.split('/')
    mod = __import__('lib.'+ modules,fromlist=True)
    if hasattr(mod,functions):
        func = getattr(mod,functions)
        func()
    else:
        print("404")

if __name__ == '__main__':
    run()

