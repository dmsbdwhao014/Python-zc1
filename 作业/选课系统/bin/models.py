#!/usr/bin/env python
# -*- coding:utf-8 -*-
import pickle
import time


class Constarint:
    def Check(self, name):
        result = pickle.load(open('db', 'rb'))
        if name in result:
            return False
        else:
            return True


class Teacher:
    def Add_Teacher(self, name, age, sale, created_time, course, role):
        self.Name, self.Age, self.Sale, self.Create_time, self.Course, self.Role = name, age, sale, created_time, course, role
        # r = Constarint.Check(name)
        msg = "{Name},{Age},{Sale},{Create_Time},{Course},{Role}\n".format(Name=self.Name, Age=self.Age,
                                                                         Sale=self.Sale,
                                                                         Create_Time=self.Create_time,
                                                                         Course=self.Course, Role=self.Role)
        pickle.dump(msg, open('db', 'wb+'))



r = Teacher()
r.Add_Teacher('chen1g1',1626,20000,time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()),'数学','老师')
result = pickle.load(open('db', 'rb'))
print(result)