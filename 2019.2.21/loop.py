
count = 0
while True:
    count += 1
    if count > 2 and count < 99:
        continue
    print("上车上车",count)
    if count == 100:
        print("黑车")
        break