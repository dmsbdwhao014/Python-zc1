
# 打开文件
# with open('test',mode='rb') as f:
#     data1 = f.readline()
#     print(data1,type(data1))

#如果不是二进制模式打开，以字符串方式读取
f = open('test','r+',encoding='utf8')
# data = f.read()
# print(data)
#seek 调整指针的位置
# f.seek(1)
#tell 当前所在的位置(字节)
# print(f.tell())
# 当前指针位置向后覆盖
# f.write('9999')
# f.close()north    21841 21776  0 11:40 ?        00:00:00 sh /app/bighead/scripts/north/logloader-ForResthbase/bin/logloader-ontime.sh

# 操作文件

# read() #无参数，全部读取; 2进制读取
# write() #写数据 ，字符或者字节
# close() #关闭文件
# flush() #强制写入数据到文件
# readline() #游标读取一行
# truncate() #seek指定游标后，截断之后的记录
# 通过with打开文件，执行完操作自动关闭
# with open('test','r+') as f:
#     for line in f:
#         print(line)

#适合跨平台
# f = open('test','ab')
# f.write(bytes('\n'+'hello',encoding='utf8'))
# f.close()
# 关闭文件
#
# with open('test','r',encoding='utf8') as f,open('test2','w',encoding='utf8') as f1:
#     rec = 0
#     for line in f:
#         rec += 1
#         if rec <=10:
#             f1.write()
#         else:
#             break

# with open('test','r',encoding='utf8') as f1,open('test1','w',encoding='utf8') as f2:
#     for line in f1:
#         new_line = line.replace('aaaa','bbbb')
#         f2.write(new_line)

