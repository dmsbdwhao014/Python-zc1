

import time
import datetime

# print(time.time())
# print(time.ctime())
# print(time.ctime(time.time()-86400))
# print(time.gmtime(time.time()-86400))
time_obj = time.gmtime()
print(time_obj.tm_year)
# print(time.localtime())
# print(time.mktime(time.localtime()))
# print(time.sleep(3))
# print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()))
# print(time.strptime('2019-03-15 14:25:30',"%Y-%m-%d %H:%M:%S"))
# print(time.mktime(time.strptime('2019-03-15 14:25:30',"%Y-%m-%d %H:%M:%S")))
# print(datetime.date.today())
# print(datetime.datetime.now())
# print(datetime.datetime.now().timetuple())
# print(time.localtime())
# print(datetime.datetime.now() - datetime.timedelta(days=10))
# print(datetime.datetime.now().replace(2018))
