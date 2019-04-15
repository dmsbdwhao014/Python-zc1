# def send(name,content):
#     print(name,content)
#     return True
#
# while True:
#     em = input("请输入邮箱:")
#     ret = send(content='xx',name=em)
#     if ret == True:
#         print("发送成功")
#     else:
#         print("发送失败")

# l1 = ['cheng',199]
# l2 = [1,2,3,4,5,6,7,8]
# s1 = 'string'
#
# dic = {1:{'name':'zhou','age':199},2:{'name':'cheng','age':333}}

# def f1(*args):
#     print(args,type(args))

# def f1(**args):
#     print(args,type(args))
#
# f1(kk1=dic,kk2=dic)
# f1(**dic)
#
# def f1(*args,**kwargs):
#     print(args)
#     print(kwargs)
#
# f1(*l1,**dic,k3='v3',k4='v4')


# str.format()  #格式化输出
# for key in dic:
#     s = 'i am {name},age {age}'.format(**dic[key])  #占位符
#     print(s)

# 参数的引用
'''
def f1(a1,a2):
    return a1+a2

def f1(a1,a2):
    return a1*a2

ret = f1(1,1)
print(ret)

name = 'zhou'
name = 'cheng'
print(name)

def f1(a1):
    a1.append(222)
    print(a1)

l1 = [1,2,3,4,5]
f1([1,2,3,4,5])

print(l1)
'''


#局部变量
'''
def f1():
    user = 'zhou'
    print(user)
    
def f2():
    user = 'cheng'
    print(user)
'''

#全局变量,所有域都可读
# 对全局变量重新赋值，需要global
# 特殊: 列表字典， 可修改，不可重新赋值
# name = 'cheng'
NAME = [1,2,3,4,5]

def f1():
    age = 19
    global NAME
    # name = 'zhou'
    NAME.append(23423423)
    print(NAME)

def f2():
    age = 20
    print(NAME,age)

f1()
f2()
