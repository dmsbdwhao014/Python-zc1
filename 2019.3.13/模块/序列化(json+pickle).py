# import sys
#
# print(sys.path)
# sys.path.append
# import json
#
# s = {"k1":123}
# ret = json.dumps(s)
# print(ret,type(ret))
#
# s1 = '{"k1":456}'
# ret1 = json.loads(s1)
# print(ret1,type(ret1))
#
# import json,requests
#
# response = requests.get('http://wthrcdn.etouch.cn/weather_mini?city=广州')
# response.encoding='utf-8'
# ret = response.json()
# # ret = json.loads(response.text)
# print(ret)
#
# import  json
# # s = '["guangdongsheng","guangzhou"]'
# s = "['guangdongsheng','guangzhou']"
# ret = json.loads(s)
# # print(type(ret))
# import json
# # s = [11,22,33]
# # json.dump(s,open('test','w'))
# ret = json.load(open('test','r'))
# print(ret)


# import pickle
import json

l1 = '1,2,3,4,5,6'
r= json.dumps(l1)
print(r)

# r = pickle.dumps(l1)
# print(r)
#
# r1 = pickle.loads(r)
# print(r1)
# pickle.dump(l1,open('db.txt','wb'))
# r = pickle.load(open('db.txt','rb'))
# print(r)