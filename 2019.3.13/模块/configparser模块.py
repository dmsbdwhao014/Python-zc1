import configparser as CP

con = CP.ConfigParser()
con.read("ini",encoding='utf-8')

result = con.sections()
print(result)

result1 = con.options("beita")
print(result1)

result2 = con.items("beita")
print(result2)

result3 = con.get("beita","age")
# result3 = con.getint("beita","age")
# result3 = con.getfloat("beita","age")
# result3 = con.getboolean("beita","age")
print(result3)

has_opt = con.has_option("beita","age")
print(has_opt,type(has_opt))