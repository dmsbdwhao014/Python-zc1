# id_db = {
#     1234123:{'name':'zhangsan','age':22,'addr':'guangdong'},
#     9837223:{'name':'wangwu','age':24,'addr':'shanghai'},
#     9837523:{'name':'lisi','age':99,'addr':'shanghai'}
# }
#
# print(id_db[9837223])
#
# id_db[9837223]['name'] = 'liumazi'
# id_db[9837223]['mail'] = 'liumazi@root.com'
#
# print(id_db[9837223])
#
# del id_db[9837223]['mail']
# print(id_db[9837223])
# id_db[9837223].pop('mail')
# print(id_db[9837223])
# id_db.get(9837223)

id_db = {
    'name':'cheng',
    211234123412:{'name':'zohou','age':22,'addr':'guangdongsheng'},
    211234123414:{'name':'zohou','age':22,'addr':'guangdongsheng'},
    211234123415: {'name': 'zohou', 'age': 22, 'addr': 'guangdongsheng'}
}
# id_db2 = {
#     211234123412:{'name11':'zohou','age':22,'addr':'guangdongsheng'}
# }
# id_db2 = {
#     211234123412:{'name11':'zohou','addr':'guangdongsheng'}
# }
# print(id_db)
# id_db.update(id_db2)   #替换原key:value
# print(id_db)
#
# print(id_db)
# print(id_db.items())
# print(id_db.values())
# print(id_db.keys())
#
# print(211232224123412 in id_db)

# print(id_db.setdefault(2112324123412,"hhhh"))  #取Key ，如不存在，设置默认值
# print(id_db.fromkeys([1,2,34,5,6,7,],'aaaa'))  #不要用

# print(id_db.popitem()) #随机删除
#
# for k,v in id_db.items():  #效率低
#     print(k,v)

for key in id_db:           #效率高
    print(key,id_db[key])

# print(id_db)



