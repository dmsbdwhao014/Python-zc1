# abs() 绝对值
# print(abs(-100))
#
# bool() 判断真假
# 0 ,None ,"",(),{},[]  为假
# print(bool(()))
#
# all() 判断所有元素是否为真，否则为假
# print(all([1,2,3,4,[]]))
# any() 判断所有元素任意一个则为真，否则为假
# print(any([0,{},]))
#
# print(ascii('s'))
#
# bin() 是10进制转 2 进制
# print(bin(256))
# oct() 是10进制转 8 进制
# print(oct(256))
# hex() 是10进制转 16 进制
# print(hex(15))
#
# 中文在utf8 编码需要3位， gbk需要2位
# bytes() 字符串转换字节
# bytearray() 字符串转元组
# str() 字节转换字符串
# s = "轴承"
# print(bytes(s,encoding='utf-8'))
# print(bytes(s,encoding='gbk'))
# print(bytearray(s,encoding='gbk'))
# print(str(bytes(s,encoding='utf-8'),encoding='gbk'))
#
# callable() 测试是否能被执行
# def f1():
#     pass
#
# f2=100
# print(callable(f1))

# chr(),ord() 将 Ascii与字符互相转换
# print(chr(66))
# print(ord('B'))

# compile() #编译字符串为python代码，3种模式(single,eval,exec
# eval() # 有返回值，通常用作表达式运算
# exec()  # 接收代码或字符串，执行python代码或字符串，没有返回值
# s = "print(123)"
# r = compile(s,"<string>","exec")
# exec(r)
# exec('7+9-23')
# ret = eval('7*27+923-121234')
# print(ret)

# dir() #查看对象提供的功能
# print(dir(list))
# help(list)

# divmod分页内置函数
# print(divmod(99,10))
# enumerate() #为列表添加下标
# isinstance() #判断对象是类的实例
# str #
# s  = "cheng" #实例
# print(isinstance(s,str))
# def f1(args):
#     result = []
#     for item in args:
#         if item > 22:
#             result.append()
#     return result
####################################################
# filter() ：#函数返回True ,将元素添加到结果中
# map()：#将函数返回值添加到结果中
# -----------------filter()------------------
# filter(函数，可迭代对象) 内部循环，参数比较
# def f2(a):
#     if a < 22:
#         return True
# l1 = [1,2,3,45,6,7,8,9]
# ret = filter(f2,l1)
# print(list(ret))
# ______________________V2
# l1 = [1,2,3,4,5,6,7]
# print(list(filter(lambda a:a > 1 ,l1)))
# -------------------map()----------------------
# map(函数，可迭代对象) 内部循环
# l1 = [1,2,3,45,6,7,8,9]
# print(list(map(lambda a:a+100,l1)))

##########################locals(),globals() 打印全局与局部变量###########
# NAME = 'jone'
#
# def f1():
#     a= 123
#     print(locals())
#     print(globals())
#
# f1()

# s = '2ijsq9w9erqwjer12341eqwfqwa'
# print(hash(s))
#############################len##########
# s = "中盛"
# print(len(bytes(s,encoding='utf-8')))
#
# s = (1,2,34,2,341,23,41,234123,41,23,412,341)
# n = ['A','B','C','D','a','b','c','d']
# print(sum(n))
# print(ord('b'))

# print(pow(2,8))

# l1 = [1,2,3,234,51]
# print(l1.sort())
# sorted(l1)
# l2 = l1.reverse()
# print(l2)
# print(reversed(l1))

# s  = '12341234123qweras'
# print(s[1:10:2])

# l1 = ['aaa',1,123,3234]
# l2 = ['bbb',1,123,3234]
# l3 = ['ccc',1,123]

# r = list(zip(l1,l2,l3))
# temp = r[0]
# s = " ".join(temp)
# print(s)



