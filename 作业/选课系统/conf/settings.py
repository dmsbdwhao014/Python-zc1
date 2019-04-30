#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
tearch_db_dir = os.path.join(BASE_DIR, 'db', 'tearch' 'tearch_list')
course_db_dir = os.path.join(BASE_DIR, 'db', 'course', 'course_list')
admin_db_dir = os.path.join(BASE_DIR, 'db', 'admin/')
print(course_db_dir)
