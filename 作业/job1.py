User_Login = {'is_login' : False}
User_Modu = {'is_admin' : False}

def chkuser(func):
    def inner(*args,**kwargs):
        with open('userlist','r',encoding='utf-8') as f:
            for line in f:
                user_list = line.strip().split(',')
                if user_list[0] == User_Login['connect_user'] and user_list[1] == User_Login['password']:
                    User_Login['is_login'] = True
                    func(*args,**kwargs)
                    return True
                else:
                    func(*args, **kwargs)
                return False
    return inner

def chkmod(func):
    def inner(*args,**kwargs):
        with open('userlist', 'r', encoding='utf-8') as f:
            for line in f:
                user_modu = line.strip().split(',')
                if user_modu == '1001':
                    User_Modu['is_admin'] = True
                    func(*args, **kwargs)
                else:
                    func(*args, **kwargs)
                return False
    return inner

@chkuser
def login(user,pwd):
    if User_Login['is_login']:
        print("欢迎%s登陆" % User_Login['connect_user'])
    elif not User_Login['is_login']:
        print("登陆失败,请注册")

@chkuser
def regiter(user,pwd,pwd1,mail,phonenumber):
    if not User_Login['is_login']:
        info = "%s,%s,%s,%s\n" %(user,pwd,mail,phonenumber)
        with open('userlist','a',encoding='utf-8') as f:
            f.write(info)
            print("注册成功")
    else:
        print("已存在的用户")

@chkmod
def changepwd():
    pass

@chkmod
def listuser():
    pass

@chkmod
def deluser():
    pass

@chkmod
def chguser():
    pass

def search():
    pass

def main():
    inp = input("1.用户登陆;2.管理员登陆;3.用户注册;4.修改密码>>")
    if inp == '1' or inp == '2':
        user = input("请输入用户:")
        pwd = input("请输入密码:")
        User_Login['connect_user'] = user
        User_Login['password'] = pwd
        login(user,pwd)
    elif inp == '3':
        name = input("请输入注册用户名:")
        passwd = input("请输入密码:")
        passwd2 = input("请再次输入密码:")
        mail = input("请输入邮箱：")
        phonenum = input("请输入电话号码:")
        if passwd == passwd2:
            User_Login['connect_user'] = name
            User_Login['password'] = passwd
            regiter(name,passwd,passwd2,mail,phonenum)
        else:
            print("两次输入的密码不一样")
    elif inp == '4':
        changepwd()

main()