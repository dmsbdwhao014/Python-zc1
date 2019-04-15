# 1.统计100-300 之前能被3，7 整除的数字的和
# l1 = range(301)
# l2 = []
# for i in l1:
#     if i >= 100:
#         l2.append(i)
#
# o = 0
# for i in l2:
#     if i % 3 == 0 or i % 7 == 0:
#         print('old i',i)
#         o += i
#         print(o)
# print(o)

# 2.定义一个函数统计字符串中的大小写字母与数字
# def count_str(str):
#     upper_cnt = 0
#     lower_cnt = 0
#     num_cnt = 0
#     for i in str:
#         if i.isdigit():
#             num_cnt += 1
#         elif i.isupper():
#             upper_cnt += 1
#         elif i.islower():
#             lower_cnt += 1
#     print("数字:",num_cnt,"大写字母:",upper_cnt,"小写字母:",lower_cnt)
#
# s = input("请输入:")
# count_str(s)

# 3.l1 和 l2 之间的合集
# l1 = [1,2,3,4,5]
# l2 = [2,3,4,5,6]
# print(set(l1).union(l2))
# print(set(l1).intersection(l2))

# 将字符串转换成utf8编码
# s = "老大"
# print(s.encode('utf-8'))
# print(bytes(s,encoding='utf-8'))

#计算数字的绝对值
# s = -1000
# print(abs(s))

# 列举为false的bool值,0,{},(),[],None
# print(bool([]))


