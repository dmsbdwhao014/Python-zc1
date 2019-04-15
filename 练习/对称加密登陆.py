import hashlib

def md5(pwd):
    obj = hashlib.md5(bytes('ass123123243sdfgs43524gsdfgsdffas33dfgsdfgsdfg3333333333dsdgsdfgsdfgsdfgsdfasf', encoding='utf-8'))
    obj.update(bytes(pwd, encoding='utf-8'))
    return obj.hexdigest()

def regist(user,passwd):
    with open('db','a',encoding='utf-8') as f:
        s = "{username}|{password}".format(username=user,password=str(md5(passwd)))
        f.write(s)

def login(user,passwd):
    with open('db','r',encoding='utf-8') as f:
        for line in f:
            u,p = line.strip().split('|')
            if user == u and md5(passwd) == p:
                return True

while True:
    choose = input("1.登陆,2.注册>>")
    if choose.strip() == "1":
        user = input("用户:")
        passwd = input("密码:")
        ret = login(user,passwd)
        if ret:
            print("登陆成功")
        else:
            print("登陆失败")
    elif choose.strip() == "2":
        user = input("用户:")
        passwd = input("密码:")
        regist(user,passwd)
