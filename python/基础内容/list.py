import copy


name = ['jone1','jone2','jone3','jone4','jone5','jone6']
name2 = ['zhangsan','lisi','wangwu']

name.insert(-1,'jone7')
name.insert(-1,'jone8')
name.insert(-1,'jone8')
name.insert(-1,'jone8')
del name[1]
name.remove('jone1')
name[::2]

print(name)

name.extend(name2)
print(name)

if 'jone8' in name:
    num_of_ele = name.count('jone8')
    posistion_of_ele = name.index('jone8')
    name[posistion_of_ele] = 'jone999999'
    print("[%s] jone8 in name,posistion:[%s]" % (num_of_ele,posistion_of_ele))
    print(name)


for i in range(name.count('jone8')):
    ele_index = name.index('jone8')
    name[ele_index] = '99999'
    print(name)