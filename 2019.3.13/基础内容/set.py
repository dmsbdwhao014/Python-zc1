

s1 = {1,2,3,4,99,100,1}
s2 = {2,3,4,5,6,7,8}
l1 = (1,2,3,4,5,6,6,7)
t1 = [7,8,9,10,11,12]

# print(s1.difference(s2))
# print(s1.symmetric_difference(s2))
# print(s1.difference_update(s2))
# print(s2.difference_update(s1))
# s1.discard(1)   #不存在不报错
# s1.remove(1111)   #不存在报错
# print(s1.pop())   #随机移除

# s3 = s1.intersection(s2)
# s1.intersection_update(s2)
# print(s1.union(s2))
# s1.update(t1) #批量更新
# print(s1)
# print(s2)

olddict = {
    "#1":8,
    "#2":4,
    "#4":2
}

newdict = {
    "#1":4,
    "#2":4,
    "#3":2
}


#old存在，new不存在的key
oldset = set(olddict.keys())
newset  = set(newdict.keys())
remove_set = oldset.difference(newset)
add_set = newset.difference(oldset)
update_set = oldset.intersection(newset)

print(oldset,newset)
print(remove_set,add_set,update_set)