age = 21

guess_age = int(input("input your guess age:"))


# if guess_age == age:
#     print("Success! you go it!!!")
# elif guess_age > age:
#     print("Think smaller!!")
# else:
#     print("Think big!!")

###v2
# for i in range(10):
#     if i < 3:
#         guess_age = int(input("input your guess age:"))
#         if guess_age == age:
#             print("Success! you go it!!!")
#             break
#         elif guess_age > age:
#             print("Think smaller!!")
#         else:
#             print("Think big!!")
#     else:
#         print("too many attempts...bye")
#         break


###V3
cnt = 0
for i in range(10):
    print("cnt:",cnt)
    if cnt < 3:
        guess_age = int(input("input your guess age:"))
        if guess_age == age:
            print("Success! you go it!!!")
            break
        elif guess_age > age:
            print("Think smaller!!")
        else:
            print("Think big!!")
    else:
        continue_confirm = input("Do you want to continue ?:")
        if continue_confirm == 'y':
            cnt = 0
            continue ###V4  跳过本次循环
        else:
            print("bye")
            break
    cnt += 1