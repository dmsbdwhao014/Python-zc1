User_Info = {}

def check_login(func):
    def inner(*args,**kwargs):
        if User_Info.get('is_login'):
            ret = func(*args,**kwargs)
            return ret
        else:
            print("请登陆")
    return inner

def check_admin(func):
    def inner(*args,**kwargs):
        if  User_Info.get('user_type') == 1:
            ret = func(*args,**kwargs)
            return ret
        else:
            print("无权限查看")
    return inner


@check_login
@check_admin
def index():
    """
    管理员功能
    :return:
    """
    print("Index")


@check_login
def home():
    """
    普通用户功能
    :return:
    """
    print(User_Info['is_login'],User_Info['user_type'])


def login():
    r = input("请输入用户名:")
    if r == "admin":
        User_Info['is_login'] = True
        User_Info['user_type'] = 1
    else:
        User_Info['is_login'] = r
        User_Info['user_type'] = 2


def main():
    while True:
        r = input("1.登陆,2.查看信息，3.超级管理员: ")
        if r == "1":
            login()
        elif r == "2":
            home()
        elif r == "3":
            index()


main()
