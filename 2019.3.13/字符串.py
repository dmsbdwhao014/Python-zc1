"""
我只是一条注释
"""
#
# s1 = "=={name:s},{age:d}---{day:f}".format(name='cheng', age=10, day=2019)
#
# s2 = "---{:*^6s}===={:+d}___{:#x}>>>>>{:.2%}".format('cheng',123,1000,0.23452345234523)
# print(s2)

# t1 = "i am {} ,age {} , from {}".format('cheng',20,'hunan')

# t1 = "i am {} ,age {} , from {}".format(*['cheng',20,'hunan'])

# t1 = "i am {name} ,age {age} , from {city}".format(**{'name':'jone','age':19,'city':'hunan'})

# t1 = "i am {name} ,age {age} , from {city}".format(name='cheng',age=19,city='hunan')

t1 = "{0:b},{0:x},{0:o}".format(100)

print(t1)


