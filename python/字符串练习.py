user,passwd = 'zhoucheng','zhoucheng'


msg = '''
Infomation of below person:
NAME : %s
AGE : %d
job : %s
''' %(name ,age ,job)

name = 'jone'
age = '18'
job = 'DBA'


import sys,os

res = os.popen('ipconfig').read()

