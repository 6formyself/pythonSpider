lines = open('user.txt', 'r').readlines()
with open('phone.txt', 'a') as f:
    for line in lines:
        array = line.split(',')
        if len(array) == 4:
            f.write(array[2] + ',')

# print('3,果冻君,18259141611,2019-12-26 11:11'.split(','))