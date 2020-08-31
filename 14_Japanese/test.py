def get_full_count(num):
    x = str(num)
    for i in range(0, 4 - len(str(num))):
        x = '0' + x
    return x


# f = open('info.txt')
# lines = f.readlines()
# for line in lines:
#     item = list(filter(lambda s: s != '', line.split(' ')))
#     for i in range(0, 100):
#         card = item[0][0:-4] + get_full_count(i)
#         date_1 = item[1][0:2]
#         date_2 = item[1][2:]
#         code = item[2][0:-1]
#     print(item[1][0:2], item[1][2:],item[2][0:-1])
# f.close()

print(get_full_count(100))


# print('5210120056150387'[0:-4])
