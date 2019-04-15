import re

def get(s):
    s = re.sub(" ","",s)
    ret = s.replace("++", "+").replace("+-", "-").replace("--", "-").replace("-+", "-")
    ret = re.split("\(([^()]+)\)",s,1)
    return ret


s = '1 + 2 * (92+92/(9222 - 23 + (29+33*-1000/19234++(-8234.22*-234+122.23/322))/1024)-2) + (234+2-(32*2))'
print(get(s))
# print(re.search('\d+\.?\d*([*/]|\*\*)\d+\.?\d*',get(s)))