import requests
from xml.etree import ElementTree

# response = requests.get('http://www.baidu.com')
# response.encoding='utf-8'
# result = response.text
# print(result)

# 判断QQ在线
"""
strg = input('qq号:')
response = requests.get('http://ws.webxml.com.cn/webservices/qqOnlineWebService.asmx/qqCheckOnline?qqCode='+strg)
r = response.text
r1 = ElementTree.XML(r)

if r1.text == 'Y':
    print("在线")
elif r1.text == 'N':
    print('离线')
# print(r1.text)
"""
# 列车时刻表
response = requests.get('http://ws.webxml.com.cn/WebServices/TrainTimeWebService.asmx/getDetailInfoByTrainCode?TrainCode=G1103&UserID=')
r = response.text
root = ElementTree.XML(r)

for node in root:
    for node_node in node:
        for node_node_node in node_node:
            for node_node_node_node in node_node_node:
                print(node_node_node_node)
# for node in root.iter('TrainDetailInfo'):
    # print(node.find("TrainStation").text,node.find("ArriveTime").text,node.find("StartTime").text)
    # print(node)