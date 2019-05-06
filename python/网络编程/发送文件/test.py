#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os

ret = os.stat('d4.png').st_size
print(ret)
