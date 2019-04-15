import re
import socket
# s = "pas ds pythonasdfa pasx"
# r = re.search("(?P<n1>p)(\w+)", s)
# print(r)
# print(r.group())
# print(r.groups())
# print(r.groupdict())
# a = 'python'
#
# pattern1 = re.compile(a)
# print(pattern1.findall(s))
# matcher1 = re.search(pattern1,s)
# print(matcher1.group(0))
#
# r = re.match('python','pythonpythonpytton').span()
# print(r)
#
# s = 'ok i am fan thank you very am muach'
# a = re.split('am', 'ok i am fan thank you very am muach',1)
# print(a)

# s = '1 + 2 * (92+92/(9222 - 23 + (29+33*1000/19234+8234*234)/1024)-2) + (234+2-(32*2))'
# step1 = re.search('\(([^()]*)\)',s)
# step1_1 = re.search('\d*[*|\/]\d*',step1.group())
# print(step1.group().split())
# print(step1_1.group().split('*'))
# pattern1 = re.compile(r"\b(([01]?\d?\d|2[0-4]\d|25[0-5])\.){3}([01]?\d?\d|2[0-4]\d|25[0-5])\b")
# a = "192.179.23.1"
# w = pattern1.finditer("192.179.23.1")
# w


# w = re.findall(r"abc\b","X abc`a")
# print(w)
#
# pattern = re.compile(r'\w+\.\w+\.(?:com|cn)+')
# print(re.findall(pattern,'11.baidu.com'))

# print(re.findall(r'\d+\w\d+','a2b3c4d5f6'))

origin = 'ab bb cb db eb fb gb'
# print(origin.split(','))
print(re.split(r'b\b',origin,4))