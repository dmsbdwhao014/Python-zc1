#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 导入模块
obj = __import__("基类构造方法", fromlist=True)

class_name = getattr(obj, "Person")

obj = class_name()

r = hasattr(obj, "name")
print(r)
