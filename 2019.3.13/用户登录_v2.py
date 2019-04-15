def CHK(user):
    """
    判断用户是否存在
    :param user: 注册时输入的用户名
    :return: 如果存在返回True，如果不存在返回False
    """
    f = open('users','r')
    for user1 in f:
        if  user1.split('|')[0] == user :
            return True
    return False


def LOGIN(user,password):
    """
    用户登陆函数
    :param user: 登陆时输入的用户
    :param password: 登陆时输入的密码
    :return: 如果一直返回True，失败返回False
    """
    f = open('users','r')
    for user1 in f:
        user_list = user1.strip().split('|')
        if  user == user_list[0] and  password  == user_list[1]:
            return True
    #         return True
    # return False
    return False

def REGISTER(user,password):
    """
    用于用户注册
    :param user: 注册时输入的用户名
    :param password: 注册时输入的密码
    :return: 注册成功返回True，失败返回False
    """
    ret = CHK(user)
    if ret:
        return False
    else:
        f = open('users', 'a')
        temp = '\n' + user + '|' + password
        f.write(temp)
        f.close()
    return True

def MAIN():
    choose = input("请输入需要的功能,1:注册，2:登陆:")
    if choose == '1':
        user = input("请输入用户名:")
        passwd = input("请输入密码:")
        res = REGISTER(user,passwd)
        if res:
            print("注册成功")
        else:
            print("注册失败,用户名已经存在")
    elif choose == '2':
        user = input("请输入用户名:")
        passwd = input("请输入密码:")
        res = LOGIN(user,passwd)
        if res:
            print("登陆成功")
        else:
            print("账号或密码错")

MAIN()


