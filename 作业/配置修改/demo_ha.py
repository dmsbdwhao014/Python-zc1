import json

def fetct(backend):
    result = []
    with open('ha.conf','r',encoding='utf-8') as f:
        # 添加标签位
        flag = False
        for line in f:
            # 判断和目标行一致
            if line.strip().startswith("backend") and line.strip() == 'backend ' + backend:
                flag = True
                continue
            if flag and line.strip().startswith("backend"):
                flag = False
                break
            if flag and line.strip():
                result.append(line.strip())
    return  result


def add(backend,record):
# """
# 3种情况
# 1.rd存在，bd存在
# 2.rd存在，bd不存在
# 3.bd存在,rd不存在
# 2种思路
# 1.变成列表全部找一遍，如果找到就新增
# 2.同时打开2个文件一边读一遍写，如果bd存在就新增，不在就增加到末尾
# """
    record_list = fetct(backend)
    if not record_list:
        # backend不存在
        with open('ha.conf','r',encoding='utf-8') as old , open('new.conf','w',encoding='utf-8') as new:
            for line in old:
                new.write(line)
            new.write("\n\nbackend " + backend + "\n")
            new.write(" " * 8 + record + "\n")
    else:
        # backend存在,record不存在 与 存在 的情况
        if record in record_list:
            #record存在
            pass
        else:
            #record不存在
            record_list.append(record)
            with open('ha.conf', 'r', encoding='utf-8') as old, open('new.conf', 'w', encoding='utf-8') as new:
                flag = False
                for line in old:
                    if line.strip().startswith('backend') and line.strip() == 'backend ' + backend:
                        flag = True
                        new.write(line)
                        for new_line in record_list:
                            new.write(" "*8 + new_line + "\n")
                    if flag and line.strip().startswith('backend'):
                        flag = False
                        new.write(line)
                        continue
                    if line.strip() and not flag:
                       new.write(line)

def dl():
    pass


bk = "test.oldboy.org"
rd = "server 100.222.227.9 100.222.7.9 weight 20 maxconn 3000"

print(add(bk,rd))
#
# r = input("input:")
# n = json.loads(r)
# bd = n['backend']
# rd = n['record']
#
# rd1 = "service %s %s weight %d maxconn %d" %(rd['server'],
#                                              rd['server'],
#                                              int(rd['weight']),
#                                              int(rd['maxconn']))
# print(rd1)
#
# {"backend":"www.oldboy.org","record":{"server":"100.1.7.9","weight":"20","maxconn":"3000"}}
# with open('ha.conf','r',encoding='utf-8') as f:
#     result = []
#     flag = False
#     for line in f:
#         if line.strip().startswith('backend') and line.strip() == 'backend '+'buy.oldboy.org':
#             flag = True
#             continue
#         elif flag and line.strip():
#             result.append(line.strip())
#         elif flag and line.strip().startswith('backend'):
#             flag = False
#     print(result)