
userlist = 'zhoucheng'
passwd = 'zhoucheng'

username=input("username:")
password = input("password:")

###V1
# if username == userlist:
#     if password == passwd:
#         print("hello : "+username)
#     else:
#         print("用户名或密码错误")
# else:
#     print("用户名或密码错误")

####V2
if username == userlist and password ==passwd:
    print("欢迎登陆")
else:
    print("用户名或密码错")