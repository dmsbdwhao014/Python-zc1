
Login_User = {"is_login":False}

def outer(func):
    def inner(*args,**kwargs):
        if Login_User['is_login']:
            func()
        else:
            print("请登陆")
    return inner

@outer
def changepwd():
        print("欢迎%s登陆" % Login_User['connect_user'])

@outer
def manager():
        print("欢迎%s登陆" % Login_User['connect_user'])

def loggin(user,pwd):
    if user == 'admin' and pwd == '123':
        Login_User['is_login'] = True
        Login_User['connect_user'] = user
        manager()

def main():
    while True:
        i = input("1.后台管理;2.用户登陆>>")
        if i == '1':
            manager()
        elif i == '2':
            user = input("请输入用户:")
            pwd = input("请输入密码:")
            loggin(user,pwd)

main()