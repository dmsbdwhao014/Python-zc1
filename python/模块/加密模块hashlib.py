import hashlib


obj = hashlib.md5(bytes('ass123123243sdfgs43524gsdfgsdffas33dfgsdfgsdfg3333333333dsdgsdfgsdfgsdfgsdfasf',encoding='utf-8'))
obj.update(bytes('123',encoding='utf-8'))
ret = obj.hexdigest()
print(obj)
print(ret)
