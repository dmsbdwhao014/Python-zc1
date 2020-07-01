ProductList = [
    ('tuoba',10),
    ('saoba',20),
    ('dengzi',10),
    ('zhuozi',20)
]
shop_car = []

salary = input("请输入工资:")

if salary.isdigit():
    salary = int(salary)
else:
    exit("不是数字")

welcome_msg = 'Welcome to Shopping maill'.center(50,'=')
print(welcome_msg)

exit_flag = False
while exit_flag is not True:
    print("商品列表".center(50,"="))
    for item in enumerate(ProductList):
        index = item[0]
        p_name = item[1][0]
        p_price = item[1][1]
        print(index,"商品名称:",p_name,"商品价格:",p_price)
    user_choice = input("[q=quit,c=check]What do you want to buy?:\n")
    if user_choice.isdigit():
        user_choice = int(user_choice)
        if user_choice < len(ProductList):
            p_item = ProductList[user_choice]
            if p_item[1] <= salary:
                shop_car.append(p_item)
                salary -= p_item[1]
                print("Added [%s] into shopcar,salary [%s]" % (p_item[0],salary))
            else:
                print("余额不足，剩余余额 [%s],需要 \033[31;1m[%s]" % (salary,p_item[1]))
                break
    else:
        if user_choice == 'q' or user_choice == 'quit':
            exit_flag = True
            print("以购买商品列表:".center(40,"="))
            for item in shop_car:
                print("商品名",item[0],"商品价格",item[1])
            print("END".center(50,"="))
            print("\033[0m 剩余工资：",salary)
        elif  user_choice == 'c' or user_choice == 'check':
                print("以购买商品列表:".center(40, "="))
                for item in shop_car:
                    print("商品名", item[0], "商品价格", item[1])
                print("END".center(50, "="))
                print("\033[0m 剩余工资：", salary)