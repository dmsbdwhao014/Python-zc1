# -*- coding: utf-8 -*-
__author__ = 'am_mm_NO.1'
import re
memu = {
    "东北":{
        "吉林省":{
            "吉林市":['吉林市1','吉林市2'],
            "长春":['长春1','长春2'],},
        "辽宁省":{
            "沈阳":['沈阳1','沈阳2','沈阳3'],
            "大连":['大连1','大连2'],
                },
            },
    '华北':{
        '河北省':{
            '廊坊':['廊坊1','廊坊2'],
            '保定':['保定1','保定2'],
                },
        '内蒙古':{
            '呼和浩特':['呼和浩特1','呼和浩特2','呼和浩特3'],
            '包头':['包头1','包头2']
                },

        },
    }
flag = True
while flag: # 全局变量，设置跳出整个循环
    for i,v in enumerate(memu.keys()): #遍历第一层字典
        print(i,v) #打印出第一层key,value
    num_1=input("请输入一级菜单号,按q退出：").strip()  #接受键盘输入
    if num_1 == 'q':
        flag = False
        break
    if num_1.isdigit():
        num_1=int(num_1)
        if num_1<= len(memu):
            key_1 = memu.keys()[num_1]
            while flag:
                for i1,v1 in enumerate(memu[key_1]):
                    print(i1,v1)
                num_2 = input("请输入二级菜单号,按q退出,b返回：").strip()
                if num_2 == 'q':
                    flag = False
                    break
                if num_2 == 'b':
                    break
                if num_2.isdigit():
                    num_2 = int(num_2)
                    if num_2 <= len(memu[key_1]):
                        key_2 = memu[key_1].keys()[num_2]
                        while flag:
                            for i2,v2 in enumerate(memu[key_1][key_2]):
                                print(i2 ,v2)
                            num_3 = input("请输入三级菜单号,按q退出,b返回：").strip()
                            if num_3 == 'q':
                                flag = False
                                break
                            if num_3 == 'b':
                                break
                            if num_3.isdigit():
                                num_3 = int(num_3)
                                if num_3 <= len(memu[key_1][key_2]):
                                    key_3 = memu[key_1][key_2].keys()[num_3]
                                    while flag:
                                        for i3,v3 in enumerate(memu[key_1][key_2][key_3]):
                                            print(i3,v3)
                                        num_4 = input("按q退出,b返回：").strip()
                                        if num_4 == 'q':
                                            flag = False
                                            break
                                        if num_4 == 'b':
                                            break