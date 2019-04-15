import random

# v1
# l1 = []
#
# for i in range(4):
#     s1 = random.randrange(65, 90)
#     s2 = random.randrange(97, 122)
#     c = chr(s1)
#     l1.append(c)
#
# result = "".join(l1)
# print(result)


l1 = []

for i in range(4):
    r = random.randrange(0,5)
    if r==2 or r == 0 :
        num1 = random.randrange(0,10)
        l1.append(str(num1))
    else:
        s2 = random.randrange(97, 122)
        c = chr(s2)
        l1.append(c)

result = "".join(l1)
print(result)
